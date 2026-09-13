"""String helpers."""

from __future__ import annotations

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_ANSI_ESCAPE = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def slugify(value: str, *, separator: str = "-") -> str:
    """Return a lowercase, URL-safe slug built from ``value``.

    Accents are folded to their ASCII base characters, runs of non-alphanumeric
    characters collapse into a single ``separator``, and leading and trailing
    separators are stripped.

        >>> slugify("Crème Brûlée, please!")
        'creme-brulee-please'
    """
    folded = unicodedata.normalize("NFKD", value)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    collapsed = _NON_ALNUM.sub(separator, ascii_only.lower())
    return collapsed.strip(separator)


def truncate(value: str, limit: int, *, suffix: str = "…") -> str:
    """Shorten ``value`` to at most ``limit`` characters, including ``suffix``.

    Truncation happens at a word boundary when one is available, so the result
    does not end mid-word. Raises ``ValueError`` if ``limit`` is too small to
    fit ``suffix``.
    """
    if limit < len(suffix):
        raise ValueError(
            f"limit ({limit}) must be at least len(suffix) ({len(suffix)})"
        )
    if len(value) <= limit:
        return value

    cut = limit - len(suffix)
    head = value[:cut]
    if value[cut] != " " and " " in head:
        head = head.rsplit(" ", 1)[0]
    return head.rstrip() + suffix


def strip_ansi(text: str) -> str:
    """Return ``text`` with ANSI escape sequences removed.

    Strips SGR codes (colors, bold, etc.), cursor-movement sequences, and
    other CSI/Fe escape sequences that terminals interpret rather than
    display. Text with no escape sequences is returned unchanged.

        >>> strip_ansi("\\x1b[31mError:\\x1b[0m disk full")
        'Error: disk full'

    Raises ``TypeError`` if ``text`` is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    return _ANSI_ESCAPE.sub("", text)
