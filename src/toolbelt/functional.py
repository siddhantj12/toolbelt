"""Function helpers."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

T = TypeVar("T")

__all__ = ["once"]

_unset = object()


def once(func: Callable[..., T]) -> Callable[..., T]:
    """Wrap ``func`` so its body runs at most once; later calls replay the first outcome.

    The first call runs ``func`` with whatever arguments it's given and
    caches what happens. Every call after that — regardless of its own
    arguments — returns that same cached result without running ``func``
    again; arguments to later calls are accepted but ignored. This holds
    even when the first call raises: the exception is cached too and
    re-raised on every later call, so a failing ``func`` is never retried.

        >>> count = 0
        >>> @once
        ... def setup():
        ...     global count
        ...     count += 1
        ...     return "ready"
        >>> setup()
        'ready'
        >>> setup()
        'ready'
        >>> count
        1

    Handy for one-time initialization that must run at most once even if
    it is called from several places, possibly with different arguments.
    """
    result: Any = _unset
    error: Exception | None = None

    def wrapper(*args: Any, **kwargs: Any) -> T:
        nonlocal result, error
        if error is not None:
            raise error
        if result is _unset:
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                error = exc
                raise
        return result

    return wrapper
