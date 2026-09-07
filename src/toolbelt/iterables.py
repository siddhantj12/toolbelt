"""Iterator helpers."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Iterator
from itertools import islice
from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = ["batched", "chunk_by", "dedupe", "flatten"]


def batched(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield consecutive lists of at most ``size`` items from ``iterable``.

    The final batch is short when the input does not divide evenly. Works on
    any iterable, including generators, and never materialises more than one
    batch at a time.
    """
    if size < 1:
        raise ValueError(f"size must be at least 1, got {size}")

    iterator = iter(iterable)
    while batch := list(islice(iterator, size)):
        yield batch


def dedupe(
    iterable: Iterable[T], *, key: Callable[[T], Hashable] | None = None
) -> Iterator[T]:
    """Yield items from ``iterable``, skipping ones already seen.

    Order is preserved and the first occurrence of each item wins. ``key``
    selects the value used for comparison, which lets unhashable items be
    deduplicated by a hashable attribute.
    """
    seen: set[Hashable] = set()
    for item in iterable:
        marker = item if key is None else key(item)
        if marker not in seen:
            seen.add(marker)
            yield item


def flatten(nested: Iterable[object], depth: int = 1) -> Iterator[object]:
    """Yield the leaf items of ``nested``, descending up to ``depth`` levels.

    An item is descended into only if it is iterable and not a ``str`` or
    ``bytes`` — those are always yielded whole, never split into characters.
    Anything else that isn't iterable is also yielded as-is. Raises
    ``ValueError`` if ``depth`` is negative.

        >>> list(flatten([1, [2, 3], [4, [5, 6]]]))
        [1, 2, 3, 4, [5, 6]]
        >>> list(flatten([1, [2, [3, 4]]], depth=2))
        [1, 2, 3, 4]
        >>> list(flatten(["ab", ["cd", "ef"]]))
        ['ab', 'cd', 'ef']
    """
    if depth < 0:
        raise ValueError(f"depth must be at least 0, got {depth}")

    for item in nested:
        if depth > 0 and isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item, depth - 1)
        else:
            yield item


def chunk_by(iterable: Iterable[T], key: Callable[[T], Hashable]) -> Iterator[list[T]]:
    """Group *consecutive* items that share the same ``key`` value.

    Unlike ``itertools.groupby`` the groups are yielded as lists, so a group
    stays valid after the iterator advances past it. The input is not sorted
    first, so non-adjacent matches produce separate groups.
    """
    group: list[T] = []
    group_marker: Hashable = object()

    for item in iterable:
        marker = key(item)
        if group and marker != group_marker:
            yield group
            group = []
        group.append(item)
        group_marker = marker

    if group:
        yield group
