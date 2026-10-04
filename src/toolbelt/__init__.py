"""Small, dependency-free Python utilities."""

from toolbelt.iterables import (
    batched,
    chunk_by,
    count_by,
    dedupe,
    first,
    flatten,
    group_by,
    interleave,
    nth,
    partition,
    peekable,
    unique_justseen,
    windowed,
)
from toolbelt.mapping import deep_merge, get_path, invert
from toolbelt.text import (
    common_prefix,
    slugify,
    snake_case,
    strip_ansi,
    truncate,
    word_wrap,
)

__all__ = [
    "batched",
    "chunk_by",
    "common_prefix",
    "count_by",
    "dedupe",
    "deep_merge",
    "first",
    "flatten",
    "get_path",
    "group_by",
    "interleave",
    "invert",
    "nth",
    "partition",
    "peekable",
    "slugify",
    "snake_case",
    "strip_ansi",
    "truncate",
    "unique_justseen",
    "windowed",
    "word_wrap",
]
__version__ = "0.1.0"
