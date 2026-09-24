"""String helpers."""

from __future__ import annotations

import re
import textwrap
import unicodedata
from collections.abc import Iterable

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")


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
    # Runs collapse to one separator, so at most one sits at each end.
    return collapsed.removeprefix(separator).removesuffix(separator)


def truncate(value: str, limit: int, *, suffix: str = "…") -> str:
    """Shorten ``value`` to at most ``limit`` characters, including ``suffix``.

    Truncation happens at a word boundary when one is available, so the result
    does not end mid-word. Raises ``ValueError`` if ``limit`` is too small to
    fit ``suffix``.

        >>> truncate("hello brave world", 12)
        'hello brave…'

    A word boundary is only used when it leaves something behind — a string
    that starts with whitespace right before the cut (e.g. ``" hello"``) falls
    back to a plain character cut instead of discarding all visible content:

        >>> truncate(" hello", 3)
        ' h…'
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
        head_at_boundary = head.rsplit(" ", 1)[0]
        if head_at_boundary:
            head = head_at_boundary
    return head.rstrip() + suffix


def word_wrap(text: str, width: int) -> str:
    """Wrap ``text`` to ``width`` columns, preserving paragraph breaks.

    A paragraph break is one or more blank lines; each paragraph is wrapped
    independently and paragraphs are rejoined with a single blank line
    between them. Within a paragraph, existing single line breaks and other
    runs of whitespace are collapsed before wrapping, so already-wrapped
    input is treated as one paragraph and re-flowed. A single word longer
    than ``width`` is kept whole on its own line rather than being broken.

        >>> word_wrap("one two three four", 10)
        'one two\\nthree four'
        >>> word_wrap("first para\\n\\nsecond para", 20)
        'first para\\n\\nsecond para'

    Raises ``ValueError`` if ``width`` is less than 1. Empty or
    whitespace-only input returns ``""``.
    """
    if width < 1:
        raise ValueError(f"width must be at least 1, got {width}")

    paragraphs = _PARAGRAPH_BREAK.split(text.strip())
    wrapped = [
        textwrap.fill(" ".join(paragraph.split()), width=width, break_long_words=False)
        for paragraph in paragraphs
        if paragraph.strip()
    ]
    return "\n\n".join(wrapped)
