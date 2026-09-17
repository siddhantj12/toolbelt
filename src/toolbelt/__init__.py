"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.text import slugify, truncate
from toolbelt.timing import Timer

__all__ = ["Timer", "batched", "chunk_by", "dedupe", "slugify", "truncate"]
__version__ = "0.1.0"
