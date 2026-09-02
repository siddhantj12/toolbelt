"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.text import slugify, truncate

__all__ = ["batched", "chunk_by", "dedupe", "slugify", "truncate"]
__version__ = "0.1.0"
