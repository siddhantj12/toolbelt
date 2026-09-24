"""Mapping helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

__all__ = ["deep_merge", "get_path"]


def deep_merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dicts into a new one, ``b`` winning conflicts.

    A key present in only one of the dicts is kept as-is. When both dicts
    have a nested dict at the same key, those nested dicts are merged
    recursively; for any other kind of conflict — including a dict on one
    side and a non-dict on the other — the value from ``b`` replaces the
    value from ``a`` outright, it is not merged into it. Neither input is
    mutated.

        >>> deep_merge({"a": 1, "opts": {"x": 1, "y": 2}}, {"opts": {"y": 3, "z": 4}})
        {'a': 1, 'opts': {'x': 1, 'y': 3, 'z': 4}}

    Raises ``TypeError`` if either argument is not a ``dict``.
    """
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise TypeError("deep_merge() requires two dicts")

    merged = dict(a)
    for key, b_value in b.items():
        a_value = merged.get(key)
        if isinstance(a_value, dict) and isinstance(b_value, dict):
            merged[key] = deep_merge(a_value, b_value)
        else:
            merged[key] = b_value
    return merged


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
