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


_ANSI_ESCAPE = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

_ACRONYM_BOUNDARY = re.compile(r"([A-Z]+)([A-Z][a-z])")
_CASE_BOUNDARY = re.compile(r"([a-z0-9])([A-Z])")
_WORD_SEPARATORS = re.compile(r"[\s_-]+")


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


def snake_case(text: str) -> str:
    """Convert camelCase, PascalCase, kebab-case or spaced text to snake_case.

    A run of two or more uppercase letters is treated as an acronym and kept
    together as one word, splitting off only the capital that starts the next
    word — so ``"HTTPServer"`` becomes ``"http_server"``, not
    ``"h_t_t_p_server"``. Existing ``-``, ``_`` and whitespace are also
    treated as word boundaries, so kebab-case and already-separated input
    convert the same way.

        >>> snake_case("parseHTTPResponse")
        'parse_http_response'
        >>> snake_case("already-snake_case Words")
        'already_snake_case_words'

    ``""`` returns ``""``. Raises ``TypeError`` if ``text`` is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    if not text:
        return ""

    marked = _ACRONYM_BOUNDARY.sub(r"\1_\2", text)
    marked = _CASE_BOUNDARY.sub(r"\1_\2", marked)
    words = _WORD_SEPARATORS.split(marked.strip())
    return "_".join(word for word in words if word).lower()


def camel_case(text: str) -> str:
    """Convert snake_case, kebab-case or spaced text to camelCase.

    Splits on ``-``, ``_`` and whitespace. The first word is always
    lowercased, matching camelCase convention. Each later word is
    capitalized — except one that is already all uppercase and more than one
    character long, which is treated as an acronym and kept exactly as
    written rather than reduced to a single capital. So a caller that wants
    ``"HTTP"`` rather than ``"Http"`` in the output spells it that way in the
    input, anywhere but the first word.

        >>> camel_case("convert_to_camel_case")
        'convertToCamelCase'
        >>> camel_case("parse_HTTP_response")
        'parseHTTPResponse'

    ``""`` returns ``""``. Raises ``TypeError`` if ``text`` is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    words = [word for word in _WORD_SEPARATORS.split(text.strip()) if word]
    if not words:
        return ""

    def cased(word: str) -> str:
        return word if word.isupper() and len(word) > 1 else word.capitalize()

    return words[0].lower() + "".join(cased(word) for word in words[1:])
