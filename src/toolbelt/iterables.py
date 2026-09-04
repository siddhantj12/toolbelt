"""Iterator helpers."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Iterator
from itertools import islice
from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = ["batched", "chunk_by", "dedupe", "partition"]


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


def partition(
    iterable: Iterable[T], predicate: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """Split ``iterable`` into items that match ``predicate`` and items that don't.

    Returns a ``(matches, non_matches)`` tuple of lists, built in a single pass
    over ``iterable`` so ``predicate`` runs exactly once per item. Order is
    preserved within each list.

        >>> partition([1, 2, 3, 4, 5], lambda n: n % 2 == 0)
        ([2, 4], [1, 3, 5])

    Empty input returns ``([], [])``. If ``predicate`` raises, the exception
    propagates and no tuple is returned.
    """
    matches: list[T] = []
    non_matches: list[T] = []
    for item in iterable:
        (matches if predicate(item) else non_matches).append(item)
    return matches, non_matches


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
