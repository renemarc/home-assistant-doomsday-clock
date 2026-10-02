"""Sensor regressions against an explicitly MOCKED Home Assistant contract.

These are not Home Assistant integration tests. Minimal module stubs supply
SensorEntity's _attr_* properties, constants, a voluptuous platform schema,
config validators, TemplateError, and the shared-session helper. The executor
mock invokes the real parser; template rendering and HA entity registration
are mocked rather than recreating HA's lifecycle, executor, or template engine.
The HTTP session mocks aiohttp's get() asynchronous context-manager contract.
Real aiohttp, voluptuous, and BeautifulSoup remain required dependencies.

HA stubs exist in sys.modules only inside patch.dict during sensor loading.
The private sensor module is executed without registering it in sys.modules,
so neither its stubs nor a stub-bound production sensor import leak globally.
"""

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import aiohttp
import voluptuous as vol

from custom_components.doomsday_clock import clock


class MockSensorEntity:
    """Only the HA SensorEntity property contract used by these tests."""

    _attr_name: str
    _attr_icon: str
    _attr_native_unit_of_measurement: str
    _attr_native_value: float | None
    _attr_available: bool

    @property
    def name(self):
        return self._attr_name

    @property
    def icon(self):
        return self._attr_icon

    @property
    def native_unit_of_measurement(self):
        return self._attr_native_unit_of_measurement

    @property
    def native_value(self):
        return self._attr_native_value

    @property
    def available(self):
        return self._attr_available


class MockTemplateError(Exception):
    """Stand-in for HA's TemplateError exception type, not its implementation."""


def load_sensor_with_scoped_ha_stubs():
    modules = {
        name: ModuleType(name)
        for name in (
            "homeassistant",
            "homeassistant.components",
            "homeassistant.components.sensor",
            "homeassistant.const",
            "homeassistant.exceptions",
            "homeassistant.helpers",
            "homeassistant.helpers.config_validation",
            "homeassistant.helpers.aiohttp_client",
        )
    }
    for name in ("homeassistant", "homeassistant.components", "homeassistant.helpers"):
        modules[name].__path__ = []
    for name, module in modules.items():
        parent, _, child = name.rpartition(".")
        if parent in modules:
            setattr(modules[parent], child, module)

    sensor_stub = modules["homeassistant.components.sensor"]
    sensor_stub.__dict__.update(
        PLATFORM_SCHEMA=vol.Schema({}), SensorEntity=MockSensorEntity
    )
    constants = modules["homeassistant.const"]
    for name, value in (
        ("ATTR_ATTRIBUTION", "attribution"),
        ("CONF_ICON", "icon"),
        ("CONF_NAME", "name"),
        ("CONF_UNIT_OF_MEASUREMENT", "unit_of_measurement"),
        ("CONF_VALUE_TEMPLATE", "value_template"),
    ):
        setattr(constants, name, value)
    modules["homeassistant.exceptions"].__dict__.update(
        TemplateError=MockTemplateError
    )
    modules["homeassistant.helpers.config_validation"].__dict__.update(
        string=str, template=lambda value: value
    )
    modules["homeassistant.helpers.aiohttp_client"].__dict__.update(
        async_get_clientsession=Mock()
    )

    sensor_path = Path(clock.__file__).with_name("sensor.py")
    spec = importlib.util.spec_from_file_location(
        "custom_components.doomsday_clock._sensor_unittest", sensor_path
    )
    assert spec is not None and spec.loader is not None
    sensor = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(sensor)
    return sensor


class DoomsdayClockSensorTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.sensor_module = load_sensor_with_scoped_ha_stubs()

    def setUp(self):
        self.response = Mock(spec=["raise_for_status", "text"])
        self.response.text = AsyncMock(
            return_value="<h1>It is now 85 seconds to midnight</h1>"
        )
        self.request = MagicMock(spec=["__aenter__", "__aexit__"])
        self.request.__aenter__.return_value = self.response
        self.request.__aexit__.return_value = False
        self.session = Mock(spec=["get"])
        self.session.get.return_value = self.request
        self.hass = SimpleNamespace(
            async_add_executor_job=AsyncMock(
                side_effect=lambda function, *args: function(*args)
            )
        )
        self.monotonic = Mock(return_value=1000.0)
        self.time_patch = patch.object(
            self.sensor_module, "time", SimpleNamespace(monotonic=self.monotonic)
        )
        self.time_patch.start()
        self.addCleanup(self.time_patch.stop)

    def test_loading_sensor_restores_home_assistant_modules(self):
        before = {
            name: module
            for name, module in sys.modules.items()
            if name == "homeassistant" or name.startswith("homeassistant.")
        }
        sensor = load_sensor_with_scoped_ha_stubs()
        after = {
            name: module
            for name, module in sys.modules.items()
            if name == "homeassistant" or name.startswith("homeassistant.")
        }
        self.assertEqual(after, before)
        self.assertNotIn(sensor.__name__, sys.modules)

    def make_sensor(self, template=None, unit="min"):
        entity = self.sensor_module.DoomsdayClockSensor(
            self.session, "Test Clock", unit, "mdi:nuke", template
        )
        entity.hass = self.hass
        return entity

    def advance_interval(self, intervals=1):
        self.monotonic.return_value += (
            self.sensor_module.MIN_TIME_BETWEEN_UPDATES.total_seconds() * intervals
        )

    async def test_setup_registers_entity_with_shared_session_and_binds_template(self):
        template = Mock(spec=["hass", "async_render"])
        add_entities = Mock()
        config = {
            "name": "Configured Clock",
            "icon": "mdi:clock",
            "unit_of_measurement": "minutes",
            "value_template": template,
        }
        with patch.object(
            self.sensor_module, "async_get_clientsession", return_value=self.session
        ) as get_session:
            await self.sensor_module.async_setup_platform(
                self.hass, config, add_entities
            )
        get_session.assert_called_once_with(self.hass)
        self.assertIs(template.hass, self.hass)
        add_entities.assert_called_once()
        entities, update_before_add = add_entities.call_args.args
        self.assertIs(update_before_add, True)
        self.assertEqual(len(entities), 1)
        entity = entities[0]
        self.assertIs(entity._session, self.session)
        self.assertIs(entity._value_template, template)
        self.assertEqual(entity.name, "Configured Clock")
        self.assertEqual(entity.icon, "mdi:clock")
        self.assertEqual(entity.native_unit_of_measurement, "minutes")
        self.session.get.assert_not_called()

    async def test_setup_without_template_uses_shared_session(self):
        add_entities = Mock()
        config = self.sensor_module.PLATFORM_SCHEMA({})
        with patch.object(
            self.sensor_module, "async_get_clientsession", return_value=self.session
        ) as get_session:
            await self.sensor_module.async_setup_platform(
                self.hass, config, add_entities
            )
        get_session.assert_called_once_with(self.hass)
        entity = add_entities.call_args.args[0][0]
        self.assertIs(entity._session, self.session)
        self.assertIsNone(entity._value_template)
        self.assertEqual(entity.name, "Doomsday Clock")
        self.assertEqual(entity.native_unit_of_measurement, "min")
        self.assertEqual(entity.icon, "mdi:nuke")

    async def test_successful_update_sets_numeric_value_and_source_attributes(self):
        entity = self.make_sensor()
        self.assertFalse(entity.available)
        self.assertIsNone(entity.native_value)
        self.assertIsNone(entity.extra_state_attributes["time"])
        self.session.get.assert_not_called()

        await entity.async_update()

        self.assertTrue(entity.available)
        self.assertIsInstance(entity.native_value, (int, float))
        self.assertAlmostEqual(entity.native_value, 85 / 60)
        self.assertEqual(
            entity.extra_state_attributes,
            {
                "attribution": self.sensor_module.CONF_ATTRIBUTION,
                "countdown": "It is now 85 seconds to midnight",
                "time": "23:58:35",
            },
        )
        self.session.get.assert_called_once_with(
            self.sensor_module.CONF_RESOURCE,
            timeout=self.sensor_module.REQUEST_TIMEOUT,
        )
        self.request.__aenter__.assert_awaited_once()
        self.request.__aexit__.assert_awaited_once()
        self.response.raise_for_status.assert_called_once_with()
        self.response.text.assert_awaited_once_with()
        self.hass.async_add_executor_job.assert_awaited_once_with(
            clock.extract_countdown,
            "<h1>It is now 85 seconds to midnight</h1>",
        )

    async def test_seconds_configuration_only_changes_label_without_a_template(self):
        add_entities = Mock()
        config = {
            "platform": "doomsday_clock",
            "scan_interval": 86400,
            "name": "Doomsday Clock",
            "icon": "mdi:nuke",
            "unit_of_measurement": "sec",
        }
        with patch.object(
            self.sensor_module, "async_get_clientsession", return_value=self.session
        ):
            await self.sensor_module.async_setup_platform(
                self.hass, config, add_entities
            )
        entity = add_entities.call_args.args[0][0]
        entity.hass = self.hass
        await entity.async_update()
        self.assertTrue(entity.available)
        self.assertEqual(entity.native_unit_of_measurement, "sec")
        self.assertAlmostEqual(entity.native_value, 85 / 60)
        self.assertEqual(entity.extra_state_attributes["time"], "23:58:35")

    async def test_seconds_labels_keep_minutes_value_and_source_attributes(self):
        for unit in ("s", "sec", "secs", "second", "seconds", "SEC", " seconds "):
            with self.subTest(unit=unit):
                entity = self.make_sensor(unit=unit)
                await entity.async_update()
                self.assertTrue(entity.available)
                self.assertEqual(entity.native_unit_of_measurement, unit)
                self.assertAlmostEqual(entity.native_value, 85 / 60)
                self.assertEqual(entity.extra_state_attributes["time"], "23:58:35")
                self.assertEqual(
                    entity.extra_state_attributes["countdown"],
                    "It is now 85 seconds to midnight",
                )

    async def test_seconds_label_does_not_convert_minute_based_source(self):
        for amount, expected in (("2", 2), ("2.5", 2.5)):
            with self.subTest(amount=amount):
                self.response.text.return_value = (
                    f"<h1>It is now {amount} minutes to midnight</h1>"
                )
                entity = self.make_sensor(unit="sec")
                await entity.async_update()
                self.assertEqual(entity.native_value, expected)

    async def test_minutes_and_custom_labels_keep_the_minutes_value(self):
        for unit in ("min", "minute", "minutes", "custom"):
            with self.subTest(unit=unit):
                entity = self.make_sensor(unit=unit)
                await entity.async_update()
                self.assertEqual(entity.native_unit_of_measurement, unit)
                self.assertAlmostEqual(entity.native_value, 85 / 60)

    async def test_seconds_conversion_is_controlled_by_template(self):
        template = Mock(spec=["async_render"])
        template.async_render.side_effect = lambda variables: variables["value"] * 60
        entity = self.make_sensor(template, unit="sec")
        await entity.async_update()
        template.async_render.assert_called_once_with({"value": 85 / 60})
        self.assertEqual(entity.native_value, 85)
        self.assertEqual(entity.extra_state_attributes["time"], "23:58:35")

    async def test_template_numeric_strings_do_not_change_source_clock_time(self):
        for rendered, expected in (("85", 85.0), (" 2.5 ", 2.5), ("0", 0.0)):
            with self.subTest(rendered=rendered):
                template = Mock(spec=["async_render"])
                template.async_render.return_value = rendered
                entity = self.make_sensor(template)
                await entity.async_update()
                self.assertTrue(entity.available)
                self.assertIsInstance(entity.native_value, float)
                self.assertEqual(entity.native_value, expected)
                template.async_render.assert_called_once_with({"value": 85 / 60})
                self.assertEqual(entity.extra_state_attributes["time"], "23:58:35")
                self.assertEqual(
                    entity.extra_state_attributes["countdown"],
                    "It is now 85 seconds to midnight",
                )

    async def test_http_timeout_and_empty_html_fail_safely_and_recover(self):
        forbidden = aiohttp.ClientResponseError(
            request_info=SimpleNamespace(real_url=self.sensor_module.CONF_RESOURCE),
            history=(),
            status=403,
            message="Forbidden",
        )
        for failure in ("http403", "timeout", "empty_html"):
            with self.subTest(failure=failure):
                self.response.raise_for_status.side_effect = None
                self.request.__aenter__.side_effect = None
                self.response.text.return_value = (
                    "<h1>It is now 85 seconds to midnight</h1>"
                )
                entity = self.make_sensor()
                await entity.async_update()
                self.assertTrue(entity.available)
                self.advance_interval()

                if failure == "http403":
                    self.response.raise_for_status.side_effect = forbidden
                elif failure == "timeout":
                    self.request.__aenter__.side_effect = TimeoutError("timed out")
                else:
                    self.response.text.return_value = ""
                with self.assertLogs(self.sensor_module._LOGGER, level="ERROR"):
                    await entity.async_update()
                self.assertFalse(entity.available)
                self.assertIsNone(entity.native_value)

                self.response.raise_for_status.side_effect = None
                self.request.__aenter__.side_effect = None
                self.response.text.return_value = (
                    "<h1>It is now 90 seconds to midnight</h1>"
                )
                request_count = self.session.get.call_count
                await entity.async_update()
                self.assertEqual(self.session.get.call_count, request_count)
                self.assertFalse(entity.available)

                self.advance_interval()
                await entity.async_update()
                self.assertEqual(self.session.get.call_count, request_count + 1)
                self.assertTrue(entity.available)
                self.assertEqual(entity.native_value, 1.5)
                self.assertEqual(entity.extra_state_attributes["time"], "23:58:30")

    async def test_updates_are_throttled_for_exactly_six_hours(self):
        self.assertEqual(
            self.sensor_module.MIN_TIME_BETWEEN_UPDATES.total_seconds(), 6 * 60 * 60
        )
        self.assertEqual(
            self.sensor_module.SCAN_INTERVAL,
            self.sensor_module.MIN_TIME_BETWEEN_UPDATES,
        )
        entity = self.make_sensor()
        await entity.async_update()
        self.response.text.return_value = "<h1>It is now 90 seconds to midnight</h1>"
        self.monotonic.return_value = 1000.0 + 6 * 60 * 60 - 0.001
        await entity.async_update()
        self.session.get.assert_called_once()
        self.hass.async_add_executor_job.assert_awaited_once()
        self.assertAlmostEqual(entity.native_value, 85 / 60)

        self.monotonic.return_value = 1000.0 + 6 * 60 * 60
        await entity.async_update()
        self.assertEqual(self.session.get.call_count, 2)
        self.assertEqual(self.hass.async_add_executor_job.await_count, 2)
        self.assertTrue(entity.available)
        self.assertEqual(entity.native_value, 1.5)

    async def test_invalid_template_values_mark_sensor_unavailable(self):
        invalid_values = (
            "not a number", "", None, True, False,
            "nan", "NaN", "inf", "-inf",
            float("nan"), float("inf"), float("-inf"),
        )
        for rendered in invalid_values:
            with self.subTest(rendered=rendered):
                template = Mock(spec=["async_render"])
                template.async_render.return_value = "2"
                entity = self.make_sensor(template)
                await entity.async_update()
                self.assertTrue(entity.available)
                self.advance_interval()
                template.async_render.return_value = rendered
                with self.assertLogs(self.sensor_module._LOGGER, level="ERROR"):
                    await entity.async_update()
                self.assertFalse(entity.available)
                self.assertIsNone(entity.native_value)

    async def test_template_error_marks_sensor_unavailable(self):
        template = Mock(spec=["async_render"])
        template.async_render.return_value = "2"
        entity = self.make_sensor(template)
        await entity.async_update()
        self.assertTrue(entity.available)
        self.advance_interval()
        template.async_render.side_effect = self.sensor_module.TemplateError(
            "template rendering failed"
        )
        with self.assertLogs(self.sensor_module._LOGGER, level="ERROR"):
            await entity.async_update()
        self.assertFalse(entity.available)
        self.assertIsNone(entity.native_value)


if __name__ == "__main__":
    unittest.main()
