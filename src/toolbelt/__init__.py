"""Small, dependency-free Python utilities."""

from toolbelt.iterables import (
    batched,
    chunk_by,
    dedupe,
    first,
    flatten,
    group_by,
    partition,
    windowed,
)
from toolbelt.mapping import deep_merge, get_path, invert
from toolbelt.text import common_prefix, slugify, strip_ansi, truncate, word_wrap

__all__ = [
    "batched",
    "chunk_by",
    "common_prefix",
    "dedupe",
    "deep_merge",
    "first",
    "flatten",
    "get_path",
    "group_by",
    "invert",
    "partition",
    "slugify",
    "strip_ansi",
    "truncate",
    "windowed",
    "word_wrap",
]
__version__ = "0.1.0"
