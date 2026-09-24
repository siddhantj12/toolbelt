"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe, windowed
from toolbelt.text import slugify, truncate

__all__ = ["batched", "chunk_by", "dedupe", "slugify", "truncate", "windowed"]
__version__ = "0.1.0"
