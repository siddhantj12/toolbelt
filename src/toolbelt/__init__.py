"""Small, dependency-free Python utilities."""

from toolbelt.iterables import (
    batched,
    chunk_by,
    dedupe,
    first,
    flatten,
    partition,
    windowed,
)
from toolbelt.mapping import deep_merge, get_path, invert
from toolbelt.text import common_prefix, slugify, strip_ansi, truncate, word_wrap
from toolbelt.timing import retry

__all__ = [
    "batched",
    "chunk_by",
    "common_prefix",
    "dedupe",
    "deep_merge",
    "first",
    "flatten",
    "get_path",
    "invert",
    "partition",
    "retry",
    "slugify",
    "strip_ansi",
    "truncate",
    "windowed",
    "word_wrap",
]
__version__ = "0.1.0"
