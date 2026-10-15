"""Time/duration helpers."""

from __future__ import annotations

import re

__all__ = ["human_duration", "parse_duration"]

_UNITS = (("h", 3600), ("m", 60), ("s", 1))
_UNIT_SECONDS = dict(_UNITS)
_TOKEN_RE = re.compile(r"(\d+)(h|m|s)")


def human_duration(seconds: float) -> str:
    """Format a duration in seconds as a compact string like ``"1h 2m 3s"``.

    Breaks ``seconds`` into hours, minutes and seconds and joins whichever of
    those are non-zero, largest first, each as a number followed by its
    single-letter suffix. A duration under a minute renders as a lone
    seconds unit, and a duration of exactly ``0`` renders as ``"0s"`` rather
    than an empty string.

        >>> human_duration(3723)
        '1h 2m 3s'
        >>> human_duration(45)
        '45s'
        >>> human_duration(3600)
        '1h'
        >>> human_duration(0)
        '0s'

    ``seconds`` may be a ``float``; the fractional part is rounded to the
    nearest whole second before formatting rather than carried through as a
    decimal, with an exact half rounded to even (``0.5`` -> ``"0s"``,
    ``1.5`` -> ``"2s"``).

    Raises ``TypeError`` if ``seconds`` is not an ``int`` or ``float``, and
    ``ValueError`` if it is negative.
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise TypeError(f"seconds must be an int or float, got {type(seconds).__name__}")
    if seconds < 0:
        raise ValueError(f"seconds must not be negative, got {seconds}")

    remaining = round(seconds)
    parts = []
    for suffix, unit_seconds in _UNITS:
        value, remaining = divmod(remaining, unit_seconds)
        if value:
            parts.append(f"{value}{suffix}")

    return " ".join(parts) if parts else "0s"


def parse_duration(text: str) -> int:
    """Parse a compact duration string like ``"1h30m"`` into whole seconds.

    ``text`` is one or more ``<number><unit>`` tokens, where ``unit`` is
    ``h``, ``m`` or ``s`` (hours, minutes, seconds). Tokens may be separated
    by spaces or not, and may appear in any order, but each unit may occur
    at most once. This makes it the inverse of ``human_duration``:
    ``parse_duration(human_duration(n)) == n`` for any non-negative
    integer ``n``.

        >>> parse_duration("1h30m")
        5400
        >>> parse_duration("1h 2m 3s")
        3723
        >>> parse_duration("45s")
        45
        >>> parse_duration("0s")
        0

    Raises ``TypeError`` if ``text`` is not a ``str``, and ``ValueError`` if
    it is empty or blank, contains a repeated unit, or has any leftover
    characters that don't form a valid token (including a missing unit
    suffix or an unrecognised one).
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    compact = "".join(text.split())
    if not compact:
        raise ValueError("text must not be empty")

    seen = set()
    total = 0
    pos = 0
    for match in _TOKEN_RE.finditer(compact):
        if match.start() != pos:
            raise ValueError(f"invalid duration string: {text!r}")
        unit = match.group(2)
        if unit in seen:
            raise ValueError(f"unit {unit!r} repeated in: {text!r}")
        seen.add(unit)
        total += int(match.group(1)) * _UNIT_SECONDS[unit]
        pos = match.end()

    if pos != len(compact):
        raise ValueError(f"invalid duration string: {text!r}")

    return total
