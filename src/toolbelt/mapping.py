"""Nested mapping helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

__all__ = ["get_path"]


def get_path(mapping: Mapping[str, Any], path: str, default: Any = None) -> Any:
    """Look up a ``"."``-separated path of keys through nested mappings.

    Walks ``path`` one segment at a time, descending into nested ``Mapping``
    values. If a segment is missing, or a value along the way is not itself a
    ``Mapping``, ``default`` is returned instead of raising.

        >>> get_path({"a": {"b": {"c": 1}}}, "a.b.c")
        1
        >>> get_path({"a": {}}, "a.b.c", default="missing")
        'missing'

    Raises ``TypeError`` if ``mapping`` itself is not a ``Mapping``.
    """
    if not isinstance(mapping, Mapping):
        raise TypeError(f"mapping must be a Mapping, got {type(mapping).__name__}")

    current: Any = mapping
    for key in path.split("."):
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]
    return current
