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
from toolbelt.text import slugify, truncate

__all__ = ["batched", "chunk_by", "dedupe", "first", "flatten", "partition", "slugify", "truncate", "windowed"]
__version__ = "0.1.0"
