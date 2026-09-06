"""String helpers."""

from __future__ import annotations

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str, *, separator: str = "-") -> str:
    """Return a lowercase, URL-safe slug built from ``value``.

    Accents are folded to their ASCII base characters, runs of non-alphanumeric
    characters collapse into a single ``separator``, and leading and trailing
    separators are stripped. The strip removes the exact ``separator`` text,
    not any of its individual characters, so a multi-character separator never
    eats into real content that happens to share a letter with it.

        >>> slugify("Crème Brûlée, please!")
        'creme-brulee-please'
        >>> slugify("banana!!!", separator="an")
        'banana'
    """
    folded = unicodedata.normalize("NFKD", value)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    collapsed = _NON_ALNUM.sub(separator, ascii_only.lower())
    if not separator:
        return collapsed
    while collapsed.startswith(separator):
        collapsed = collapsed[len(separator) :]
    while collapsed.endswith(separator):
        collapsed = collapsed[: len(collapsed) - len(separator)]
    return collapsed


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
