"""Iterator helpers."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable, Iterator
from itertools import islice
from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = ["batched", "chunk_by", "dedupe", "windowed"]


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


def windowed(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield sliding windows of ``size`` consecutive items from ``iterable``.

    Each window overlaps the previous one by ``size - 1`` items and advances
    by one. If ``iterable`` yields fewer than ``size`` items overall, no
    window is produced at all — there is no short window at the end, unlike
    ``batched``. Works lazily on any iterable, including generators.

        >>> list(windowed([1, 2, 3, 4], 2))
        [[1, 2], [2, 3], [3, 4]]
    """
    if size < 1:
        raise ValueError(f"size must be at least 1, got {size}")

    iterator = iter(iterable)
    window: deque[T] = deque(islice(iterator, size), maxlen=size)
    if len(window) < size:
        return
    yield list(window)
    for item in iterator:
        window.append(item)
        yield list(window)


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
