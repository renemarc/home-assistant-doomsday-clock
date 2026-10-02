"""Sensor platform for Doomsday Clock."""

import datetime
import logging
import math
import time

import aiohttp
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_ICON,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_VALUE_TEMPLATE,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .clock import extract_countdown, minutes_to_time

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Doomsday Clock"
DEFAULT_ICON = "mdi:nuke"
DEFAULT_UNIT_OF_MEASUREMENT = "min"

CONF_ATTRIBUTION = "Threat assessment by the Bulletin of the Atomic Scientists"
CONF_RESOURCE = "https://thebulletin.org/doomsday-clock/"

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(hours=6)
SCAN_INTERVAL = MIN_TIME_BETWEEN_UPDATES
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.string,
        vol.Optional(
            CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_UNIT_OF_MEASUREMENT
        ): cv.string,
        vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Doomsday Clock sensor using Home Assistant's HTTP session."""
    value_template = config.get(CONF_VALUE_TEMPLATE)
    if value_template is not None:
        value_template.hass = hass

    async_add_entities(
        [
            DoomsdayClockSensor(
                async_get_clientsession(hass),
                config[CONF_NAME],
                config[CONF_UNIT_OF_MEASUREMENT],
                config[CONF_ICON],
                value_template,
            )
        ],
        True,
    )


class DoomsdayClockSensor(SensorEntity):
    """Representation of a Doomsday Clock sensor."""

    def __init__(self, session, name, unit_of_measurement, icon, value_template):
        """Initialize the sensor without fetching data."""
        self._session = session
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_icon = icon
        self._attr_native_value = None
        self._attr_available = False
        self._value_template = value_template
        self._sentence = None
        self._minutes = None
        self._last_update = None

    @property
    def extra_state_attributes(self):
        """Return the source countdown and clock face, independent of templates."""
        return {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
            "countdown": self._sentence,
            "time": minutes_to_time(self._minutes),
        }

    async def async_update(self):
        """Fetch and parse the current setting without blocking the event loop."""
        now = time.monotonic()
        if (
            self._last_update is not None
            and now - self._last_update < MIN_TIME_BETWEEN_UPDATES.total_seconds()
        ):
            return
        self._last_update = now

        try:
            async with self._session.get(
                CONF_RESOURCE, timeout=REQUEST_TIMEOUT
            ) as response:
                response.raise_for_status()
                html = await response.text()
            sentence, minutes = await self.hass.async_add_executor_job(
                extract_countdown, html
            )
            value = minutes
            if self._value_template is not None:
                value = self._value_template.async_render({"value": minutes})
                if isinstance(value, bool):
                    raise ValueError("value_template must return a finite number")
                value = float(value)
                if not math.isfinite(value):
                    raise ValueError("value_template must return a finite number")
        except (aiohttp.ClientError, TimeoutError, UnicodeError) as err:
            self._attr_available = False
            self._attr_native_value = None
            _LOGGER.error("Unable to fetch Doomsday Clock URL %s: %s", CONF_RESOURCE, err)
            return
        except (ValueError, TypeError, TemplateError) as err:
            self._attr_available = False
            self._attr_native_value = None
            _LOGGER.error("Unable to update Doomsday Clock: %s", err)
            return

        self._sentence = sentence
        self._minutes = minutes
        self._attr_native_value = value
        self._attr_available = True
        _LOGGER.debug("Doomsday Clock countdown: %s (%s minutes)", sentence, minutes)
