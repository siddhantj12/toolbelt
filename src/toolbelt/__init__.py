"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.mapping import get_path
from toolbelt.text import slugify, truncate

__all__ = ["batched", "chunk_by", "dedupe", "get_path", "slugify", "truncate"]
__version__ = "0.1.0"
