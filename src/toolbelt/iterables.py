"""Iterator helpers."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable, Iterator
from itertools import islice
from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = [
    "batched",
    "chunk_by",
    "dedupe",
    "first",
    "flatten",
    "group_by",
    "partition",
    "windowed",
]


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


def first(iterable: Iterable[T], default: T | None = None) -> T | None:
    """Return the first item of ``iterable``, or ``default`` if it is empty.

    Unlike ``next(iter(iterable))``, this never raises ``StopIteration`` on
    an empty input. Only the first item is consumed, so it is safe to call
    on an infinite generator.

        >>> first([3, 1, 2])
        3
        >>> first([], default="none")
        'none'
    """
    for item in iterable:
        return item
    return default


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


def group_by(
    iterable: Iterable[T], key: Callable[[T], Hashable]
) -> dict[Hashable, list[T]]:
    """Group items of ``iterable`` into lists keyed by ``key(item)``.

    Unlike ``itertools.groupby``, ``iterable`` does not need to be sorted
    first — items sharing a key are collected together no matter where they
    appear. Keys appear in the returned dict in first-seen order, and each
    key's list keeps the items' original relative order.

        >>> group_by(["ant", "bee", "ape", "cow"], key=lambda w: w[0])
        {'a': ['ant', 'ape'], 'b': ['bee'], 'c': ['cow']}

    Empty input returns ``{}``. If ``key`` raises, the exception propagates
    and no dict is returned.
    """
    groups: dict[Hashable, list[T]] = {}
    for item in iterable:
        groups.setdefault(key(item), []).append(item)
    return groups


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
