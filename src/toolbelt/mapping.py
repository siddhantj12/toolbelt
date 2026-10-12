"""Mapping helpers."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping
from typing import Any, TypeVar

K = TypeVar("K")

V = TypeVar("V", bound=Hashable)

__all__ = ["deep_merge", "flatten_dict", "get_path", "invert", "omit", "pick", "set_path"]


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


def pick(mapping: Mapping[K, Any], keys: Iterable[K]) -> dict[K, Any]:
    """Return a new dict with only the entries of ``mapping`` whose key is in ``keys``.

    A key in ``keys`` that isn't present in ``mapping`` is silently ignored, so
    ``pick`` never raises for an unknown key. Entries keep ``mapping``'s
    iteration order, not ``keys``'s. ``mapping`` itself is not modified.

        >>> pick({"a": 1, "b": 2, "c": 3}, ["a", "c"])
        {'a': 1, 'c': 3}
        >>> pick({"a": 1, "b": 2}, [])
        {}

    Raises ``TypeError`` if ``mapping`` is not a ``Mapping``.
    """
    if not isinstance(mapping, Mapping):
        raise TypeError(f"mapping must be a Mapping, got {type(mapping).__name__}")

    wanted = set(keys)
    return {key: value for key, value in mapping.items() if key in wanted}


def omit(mapping: Mapping[K, Any], keys: Iterable[K]) -> dict[K, Any]:
    """Return a new dict with ``mapping``'s entries excluding ``keys``.

    A key in ``keys`` that isn't present in ``mapping`` is silently ignored, so
    ``omit`` never raises for an unknown key. Remaining entries keep
    ``mapping``'s iteration order. ``mapping`` itself is not modified.

        >>> omit({"a": 1, "b": 2, "c": 3}, ["b"])
        {'a': 1, 'c': 3}
        >>> omit({"a": 1, "b": 2}, [])
        {'a': 1, 'b': 2}

    Raises ``TypeError`` if ``mapping`` is not a ``Mapping``.
    """
    if not isinstance(mapping, Mapping):
        raise TypeError(f"mapping must be a Mapping, got {type(mapping).__name__}")

    excluded = set(keys)
    return {key: value for key, value in mapping.items() if key not in excluded}


def set_path(mapping: Mapping[str, Any], path: str, value: Any) -> dict[str, Any]:
    """Return a new dict with a value set along a ``"."``-separated path of keys.

    Each segment of ``path`` becomes a nested dict; missing intermediates are
    created automatically. If a segment along the way already holds a
    non-dict value, it is replaced with a new nested dict rather than
    raising — the same "last write wins" rule ``deep_merge`` applies.
    ``mapping`` itself is not modified, nor are any of its nested dicts
    touched by the path; everything along the path is copied first.

        >>> set_path({"a": {"b": 1}}, "a.c.d", 2)
        {'a': {'b': 1, 'c': {'d': 2}}}
        >>> set_path({}, "a.b", 1)
        {'a': {'b': 1}}

    Raises ``TypeError`` if ``mapping`` is not a ``Mapping``, and
    ``ValueError`` if ``path`` is empty.
    """
    if not isinstance(mapping, Mapping):
        raise TypeError(f"mapping must be a Mapping, got {type(mapping).__name__}")
    if not path:
        raise ValueError("path must not be empty")

    *parents, last = path.split(".")
    result = dict(mapping)
    current = result
    for key in parents:
        existing = current.get(key)
        next_level = dict(existing) if isinstance(existing, Mapping) else {}
        current[key] = next_level
        current = next_level
    current[last] = value
    return result


def flatten_dict(mapping: Mapping[str, Any], sep: str = ".") -> dict[str, Any]:
    """Flatten a nested mapping into a single level, joining keys with ``sep``.

    Descends into nested ``Mapping`` values, building each leaf's key by
    joining the path to it with ``sep``. A key whose value is itself a
    mapping never appears in the result — only leaves do — so a key holding
    an *empty* nested mapping contributes no key at all, and that emptiness
    is not recoverable from the result.

        >>> flatten_dict({"a": 1, "b": {"c": 2, "d": {"e": 3}}})
        {'a': 1, 'b.c': 2, 'b.d.e': 3}
        >>> flatten_dict({"a": {"b": 1}}, sep="/")
        {'a/b': 1}
        >>> flatten_dict({"a": {}})
        {}

    If two different paths flatten to the same key (for example
    ``{"a.b": 1, "a": {"b": 2}}``), the one encountered later in iteration
    order wins, same as a ``dict`` literal with a repeated key.

    Raises ``TypeError`` if ``mapping`` is not a ``Mapping``.
    """
    if not isinstance(mapping, Mapping):
        raise TypeError(f"mapping must be a Mapping, got {type(mapping).__name__}")

    result: dict[str, Any] = {}

    def _walk(current: Mapping[str, Any], prefix: str) -> None:
        for key, value in current.items():
            full_key = f"{prefix}{sep}{key}" if prefix else str(key)
            if isinstance(value, Mapping):
                _walk(value, full_key)
            else:
                result[full_key] = value

    _walk(mapping, "")
    return result


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
