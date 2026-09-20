"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.text import slugify, truncate
from toolbelt.timing import retry

__all__ = ["batched", "chunk_by", "dedupe", "retry", "slugify", "truncate"]
__version__ = "0.1.0"
