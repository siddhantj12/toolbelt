"""Iterator helpers."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable, Iterator
from itertools import islice
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")

__all__ = [
    "batched",
    "chunk_by",
    "count_by",
    "dedupe",
    "first",
    "flatten",
    "group_by",
    "interleave",
    "nth",
    "partition",
    "peekable",
    "unique_justseen",
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


def unique_justseen(
    iterable: Iterable[T], *, key: Callable[[T], Hashable] | None = None
) -> Iterator[T]:
    """Yield items from ``iterable``, dropping each that equals the item just before it.

    Unlike ``dedupe``, only *consecutive* duplicates are collapsed — the same
    value can reappear later once a different value has come between the
    occurrences. ``key`` selects the value used for comparison, which lets
    unhashable items be compared by a hashable attribute.

        >>> list(unique_justseen([1, 1, 2, 2, 1, 1]))
        [1, 2, 1]
        >>> list(unique_justseen(["A", "a", "B"], key=str.lower))
        ['A', 'B']

    Empty input yields nothing. If ``key`` raises, the exception propagates
    and iteration stops there.
    """
    sentinel = object()
    previous: Hashable = sentinel
    for item in iterable:
        marker = item if key is None else key(item)
        if marker != previous:
            yield item
        previous = marker


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


def nth(iterable: Iterable[T], n: int, default: T | None = None) -> T | None:
    """Return the item at index ``n`` of ``iterable``, or ``default`` if it's too short.

    Consumes at most ``n + 1`` items, so it works lazily on any iterable,
    including an infinite or single-pass generator. ``n`` counts from 0, like
    sequence indexing.

        >>> nth([10, 20, 30], 1)
        20
        >>> nth([10, 20, 30], 5, default="missing")
        'missing'
        >>> nth(iter([]), 0, default="empty")
        'empty'

    Raises ``ValueError`` if ``n`` is negative, since a single-pass iterable
    has no way to count backward from its end.
    """
    if n < 0:
        raise ValueError(f"n must be at least 0, got {n}")
    try:
        return next(islice(iterable, n, None))
    except StopIteration:
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


def interleave(*iterables: Iterable[T]) -> Iterator[T]:
    """Yield items from each of ``iterables`` in round-robin order.

    Each round takes one item from every iterable that still has one, in the
    order the iterables were given. An iterable that runs out is dropped from
    later rounds while the others keep going, so the result is exhausted only
    once every input is — not just the shortest, unlike ``zip``.

        >>> list(interleave([1, 2, 3], [10, 20], [100]))
        [1, 10, 100, 2, 20, 3]

    Called with no iterables, or only empty ones, yields nothing. Raises
    ``TypeError`` if an argument is not iterable.
    """
    iterators = [iter(it) for it in iterables]
    while iterators:
        still_going = []
        for iterator in iterators:
            try:
                item = next(iterator)
            except StopIteration:
                continue
            yield item
            still_going.append(iterator)
        iterators = still_going


class peekable(Generic[T]):
    """Iterator wrapper that lets you look at the next item without consuming it.

    Wraps ``iterable`` for one-pass iteration via ``next()`` or a ``for``
    loop, same as the original would give. ``peek(default)`` looks at the
    item the next ``next()`` call would return, without advancing — calling
    ``peek`` repeatedly keeps returning that same item until ``next()`` (or
    another iteration step) actually consumes it.

        >>> it = peekable([1, 2, 3])
        >>> it.peek()
        1
        >>> it.peek()
        1
        >>> next(it)
        1
        >>> list(it)
        [2, 3]

    With no ``default``, peeking past the end raises ``StopIteration`` — the
    same error ``next()`` would raise on an empty iterator. Pass ``default``
    to get a value back instead of the exception:

        >>> peekable([]).peek(default="empty")
        'empty'
    """

    _unset = object()

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterator = iter(iterable)
        self._cache: list[T] = []

    def __iter__(self) -> peekable[T]:
        return self

    def __next__(self) -> T:
        if self._cache:
            return self._cache.pop(0)
        return next(self._iterator)

    def peek(self, default: Any = _unset) -> Any:
        """Return the next item without consuming it; see class docstring."""
        if not self._cache:
            try:
                self._cache.append(next(self._iterator))
            except StopIteration:
                if default is peekable._unset:
                    raise
                return default
        return self._cache[0]


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


def count_by(iterable: Iterable[T], key: Callable[[T], Hashable]) -> dict[Hashable, int]:
    """Count items of ``iterable`` grouped by ``key(item)``.

    Keys appear in the returned dict in first-seen order, each mapped to how
    many items produced that key.

        >>> count_by(["ant", "bee", "ape", "cow"], key=lambda w: w[0])
        {'a': 2, 'b': 1, 'c': 1}

    Empty input returns ``{}``. If ``key`` raises, the exception propagates
    and no dict is returned.
    """
    counts: dict[Hashable, int] = {}
    for item in iterable:
        marker = key(item)
        counts[marker] = counts.get(marker, 0) + 1
    return counts


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
