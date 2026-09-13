"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.text import slugify, strip_ansi, truncate

__all__ = ["batched", "chunk_by", "dedupe", "slugify", "strip_ansi", "truncate"]
__version__ = "0.1.0"
