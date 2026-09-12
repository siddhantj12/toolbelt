"""String helpers."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def common_prefix(strings: Iterable[str]) -> str:
    """Return the longest string that is a prefix of every string in ``strings``.

    Comparison is exact — case-sensitive, no Unicode normalisation. A single
    string is returned unchanged, and ``""`` is returned when there is no
    shared prefix or when any string in ``strings`` is empty. Raises
    ``ValueError`` on an empty sequence, since no prefix can be computed.

        >>> common_prefix(["flower", "flow", "flight"])
        'fl'
    """
    strings = list(strings)
    if not strings:
        raise ValueError("common_prefix() requires at least one string")

    first, *rest = strings
    if not rest:
        return first

    prefix_len = len(first)
    for other in rest:
        prefix_len = min(prefix_len, len(other))
        for i in range(prefix_len):
            if first[i] != other[i]:
                prefix_len = i
                break

    return first[:prefix_len]


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
