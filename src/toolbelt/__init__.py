"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.mapping import deep_merge
from toolbelt.text import slugify, truncate

__all__ = ["batched", "chunk_by", "dedupe", "deep_merge", "slugify", "truncate"]
__version__ = "0.1.0"
