"""Time/duration helpers."""

from __future__ import annotations

__all__ = ["human_duration"]

_UNITS = (("h", 3600), ("m", 60), ("s", 1))


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
