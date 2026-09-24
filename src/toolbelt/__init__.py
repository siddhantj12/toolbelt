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
from toolbelt.text import slugify, truncate, word_wrap

__all__ = [
    "batched",
    "chunk_by",
    "dedupe",
    "first",
    "flatten",
    "partition",
    "slugify",
    "truncate",
    "windowed",
    "word_wrap",
]
__version__ = "0.1.0"
