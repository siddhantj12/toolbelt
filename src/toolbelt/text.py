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


def ordinal(n: int) -> str:
    """Return the English ordinal string for an integer, e.g. ``"1st"``, ``"22nd"``.

    The suffix is chosen from the last two digits of ``abs(n)``: ``11``,
    ``12`` and ``13`` always take ``"th"`` (and so does any number ending in
    them, like ``113``), even though they end in ``1``, ``2`` or ``3``.
    Everything else follows the usual ``1`` → ``"st"``, ``2`` → ``"nd"``,
    ``3`` → ``"rd"``, otherwise ``"th"`` rule. Negative numbers keep their
    sign, with the suffix picked the same way.

        >>> ordinal(1)
        '1st'
        >>> ordinal(22)
        '22nd'
        >>> ordinal(113)
        '113th'
        >>> ordinal(-2)
        '-2nd'

    ``0`` returns ``"0th"``. Raises ``TypeError`` if ``n`` is not an ``int``.
    """
    if not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")

    last_two = abs(n) % 100
    if 11 <= last_two <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(last_two % 10, "th")
    return f"{n}{suffix}"


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


_DECIMAL_UNITS = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
_BINARY_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")


def human_bytes(n: float, *, binary: bool = True) -> str:
    """Format a byte count as a human-readable string, e.g. ``"1.5 MiB"``.

    ``binary`` (the default) scales by 1024 and uses ``KiB``/``MiB``/...;
    set it to ``False`` to scale by 1000 and use ``KB``/``MB``/... instead.
    The value is divided down until it fits under the base, then shown with
    one decimal place; values under the base are shown as a bare integer
    byte count with no decimal.

        >>> human_bytes(1536)
        '1.5 KiB'
        >>> human_bytes(1_600_000, binary=False)
        '1.6 MB'
        >>> human_bytes(0)
        '0 B'

    Raises ``TypeError`` if ``n`` is not an ``int`` or ``float``, and
    ``ValueError`` if it is negative.
    """
    if isinstance(n, bool) or not isinstance(n, (int, float)):
        raise TypeError(f"n must be an int or float, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must not be negative, got {n}")

    base = 1024 if binary else 1000
    units = _BINARY_UNITS if binary else _DECIMAL_UNITS

    value = float(n)
    unit_index = 0
    while value >= base and unit_index < len(units) - 1:
        value /= base
        unit_index += 1

    if unit_index == 0:
        return f"{int(value)} {units[0]}"
    return f"{value:.1f} {units[unit_index]}"


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    """Return ``"<count> <word>"`` with the singular or plural form chosen for you.

    The singular form is used when ``abs(count) == 1``; every other count,
    including ``0`` and negative counts other than ``-1``, uses the plural
    form — matching ordinary English usage. ``plural`` defaults to
    ``singular + "s"``, which covers most words; pass it explicitly for an
    irregular plural.

        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(3, "file")
        '3 files'
        >>> pluralize(0, "file")
        '0 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    Raises ``TypeError`` if ``count`` is not an ``int``.
    """
    if not isinstance(count, int):
        raise TypeError(f"count must be an int, got {type(count).__name__}")

    if abs(count) == 1:
        word = singular
    else:
        word = plural if plural is not None else singular + "s"
    return f"{count} {word}"
