"""Parse the Bulletin's current Doomsday Clock setting."""

import math
import re

from bs4 import BeautifulSoup

_NUMBER_WORDS = {
    word: number
    for number, word in enumerate(
        (
            "zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
            "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
        )
    )
}
_COUNTDOWN_PATTERN = re.compile(
    r"(?:it is (?:(?:now|still) )?)?"
    r"(?P<amount>\d+(?:\.\d+)?|" + "|".join(_NUMBER_WORDS) + r"|half)"
    r"(?P<half> and (?:a )?half)? (?:a )?"
    r"(?P<unit>minutes?|seconds?) to midnight[.!]?",
    re.IGNORECASE,
)


def sentence_to_minutes(sentence):
    """Convert a countdown heading to minutes, including seconds and halves."""
    sentence = " ".join(sentence.split())
    match = _COUNTDOWN_PATTERN.fullmatch(sentence)
    if match is None:
        raise ValueError(f"Unrecognized Doomsday Clock countdown: {sentence}")

    amount = match.group("amount").lower()
    if amount == "half":
        value = 0.5
    elif amount in _NUMBER_WORDS:
        value = _NUMBER_WORDS[amount]
    else:
        value = float(amount)
    if match.group("half"):
        value += 0.5
    if match.group("unit").lower().startswith("second"):
        value /= 60
    if not math.isfinite(value):
        raise ValueError("Doomsday Clock countdown is not finite")
    return value


def extract_countdown(html):
    """Extract only the current-setting heading, never a historical card."""
    soup = BeautifulSoup(html, "html.parser")
    matches = []
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        sentence = " ".join(heading.get_text(" ", strip=True).split())
        if sentence.lower().startswith("it is now "):
            matches.append((sentence, sentence_to_minutes(sentence)))

    if not matches:
        raise ValueError("Current-setting heading not found; the source page may have changed")
    if len({minutes for _, minutes in matches}) != 1:
        raise ValueError("Conflicting current-setting headings found")
    return matches[0]


def minutes_to_time(minutes):
    """Convert source minutes to the clock face time, rounded to the second."""
    if minutes is None:
        return None
    seconds = (86400 - round(minutes * 60)) % 86400
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
