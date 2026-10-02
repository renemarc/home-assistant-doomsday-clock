"""Regression tests for the real countdown parser; no Home Assistant required."""

import unittest

from custom_components.doomsday_clock.clock import (
    extract_countdown,
    minutes_to_time,
    sentence_to_minutes,
)


class CountdownParserTests(unittest.TestCase):
    def test_present_setting_is_85_seconds_not_85_minutes(self):
        sentence, minutes = extract_countdown(
            "<h1>It is now 85 seconds to midnight</h1>"
        )
        self.assertEqual(sentence, "It is now 85 seconds to midnight")
        self.assertAlmostEqual(minutes, 85 / 60)
        self.assertEqual(minutes_to_time(minutes), "23:58:35")

    def test_seconds_settings(self):
        for seconds in (85, 89, 90, 100):
            with self.subTest(seconds=seconds):
                sentence = f"It is now {seconds} seconds to midnight"
                self.assertAlmostEqual(sentence_to_minutes(sentence), seconds / 60)
                self.assertAlmostEqual(
                    extract_countdown(f"<h2>{sentence}</h2>")[1], seconds / 60
                )

    def test_integer_word_and_half_minutes(self):
        cases = (
            ("It is now 1 minute to midnight", 1),
            ("It is now 12 minutes to midnight.", 12),
            ("It is two minutes to midnight", 2),
            ("It is still three minutes to midnight!", 3),
            ("It is now nineteen minutes to midnight", 19),
            ("IT IS NOW TWO MINUTES TO MIDNIGHT", 2),
            ("half a minute to midnight", 0.5),
            ("It is now two and a half minutes to midnight", 2.5),
            ("It is now two and half minutes to midnight", 2.5),
            ("It is now 2 and a half minutes to midnight", 2.5),
            ("It is now 2.5 minutes to midnight", 2.5),
        )
        for sentence, expected in cases:
            with self.subTest(sentence=sentence):
                self.assertEqual(sentence_to_minutes(sentence), expected)

    def test_whitespace_and_nonbreaking_spaces(self):
        sentence = " \n It\t is\u00a0 now  85\n seconds\u00a0to\t midnight \n"
        self.assertAlmostEqual(sentence_to_minutes(sentence), 85 / 60)
        heading, minutes = extract_countdown(f"<h1>{sentence}</h1>")
        self.assertEqual(heading, "It is now 85 seconds to midnight")
        self.assertAlmostEqual(minutes, 85 / 60)

    def test_nested_markup_and_html_nonbreaking_spaces(self):
        heading, minutes = extract_countdown(
            "<h3><span>It is</span>&nbsp;<em>now</em>\n"
            "<strong>85</strong> <span>seconds</span>&nbsp;to "
            "<a href='/'>midnight</a></h3>"
        )
        self.assertEqual(heading, "It is now 85 seconds to midnight")
        self.assertAlmostEqual(minutes, 85 / 60)

    def test_only_current_heading_is_selected_not_history_or_faq(self):
        html = """
            <section id="history">
              <h2>100 seconds to midnight</h2>
              <h3>It is two minutes to midnight</h3>
              <p>It is now 90 seconds to midnight</p>
            </section>
            <section id="faq">
              <h2>Why was it 90 seconds to midnight?</h2>
              <p>It is now 100 seconds to midnight</p>
            </section>
            <h1>It is now 85 seconds to midnight</h1>
            <h4>It is still three minutes to midnight</h4>
        """
        self.assertEqual(
            extract_countdown(html),
            ("It is now 85 seconds to midnight", 85 / 60),
        )

    def test_identical_current_headings_are_accepted(self):
        sentence = "It is now 85 seconds to midnight"
        self.assertEqual(
            extract_countdown(f"<h1>{sentence}</h1><h2>{sentence}</h2>"),
            (sentence, 85 / 60),
        )

    def test_equivalent_current_headings_are_accepted(self):
        self.assertEqual(
            extract_countdown(
                "<h1>It is now 90 seconds to midnight</h1>"
                "<h2>It is now 1.5 minutes to midnight.</h2>"
            ),
            ("It is now 90 seconds to midnight", 1.5),
        )

    def test_conflicting_current_headings_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            extract_countdown(
                "<h1>It is now 85 seconds to midnight</h1>"
                "<h2>It is now 90 seconds to midnight</h2>"
            )

    def test_missing_current_heading_is_rejected(self):
        cases = (
            "",
            "<html><body></body></html>",
            "<p>It is now 85 seconds to midnight</p>",
            "<div>It is now 85 seconds to midnight</div>",
            "<h2>85 seconds to midnight</h2>",
            "<h2>When was it 90 seconds to midnight?</h2>",
        )
        for html in cases:
            with (
                self.subTest(html=html),
                self.assertRaisesRegex(ValueError, "heading not found"),
            ):
                extract_countdown(html)

    def test_unrecognized_countdown_is_rejected(self):
        for sentence in ("not a countdown", "It is now soon to midnight"):
            with self.subTest(sentence=sentence), self.assertRaises(ValueError):
                sentence_to_minutes(sentence)

    def test_minutes_to_time_without_a_setting(self):
        self.assertIsNone(minutes_to_time(None))

    def test_minutes_to_time_preserves_seconds(self):
        for seconds, expected in (
            (85, "23:58:35"),
            (89, "23:58:31"),
            (90, "23:58:30"),
            (100, "23:58:20"),
            (120, "23:58:00"),
        ):
            with self.subTest(seconds=seconds):
                self.assertEqual(minutes_to_time(seconds / 60), expected)


if __name__ == "__main__":
    unittest.main()
