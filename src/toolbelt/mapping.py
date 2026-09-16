"""Mapping helpers."""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V", bound=Hashable)

__all__ = ["invert"]


def invert(mapping: Mapping[K, V]) -> dict[V, K]:
    """Return a new dict with ``mapping``'s keys and values swapped.

    Values become keys, so they must be hashable. When two or more keys
    share the same value, the key that appears last in ``mapping``'s
    iteration order wins — the same rule a
    ``{v: k for k, v in mapping.items()}`` comprehension would apply.
    ``mapping`` itself is not modified.

        >>> invert({"a": 1, "b": 2})
        {1: 'a', 2: 'b'}
        >>> invert({"a": 1, "b": 1})
        {1: 'b'}

    Raises ``TypeError`` if ``mapping`` is not a ``Mapping``, or if one of
    its values is not hashable.
    """
    if not isinstance(mapping, Mapping):
        raise TypeError(f"mapping must be a Mapping, got {type(mapping).__name__}")

    return {value: key for key, value in mapping.items()}
