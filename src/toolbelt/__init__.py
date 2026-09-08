"""Small, dependency-free Python utilities."""

from toolbelt.iterables import batched, chunk_by, dedupe
from toolbelt.text import slugify, truncate, word_wrap

__all__ = ["batched", "chunk_by", "dedupe", "slugify", "truncate", "word_wrap"]
__version__ = "0.1.0"
