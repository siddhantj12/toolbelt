"""Function helpers."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

T = TypeVar("T")

__all__ = ["compose", "once"]

_unset = object()


def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Combine ``funcs`` into one callable that applies them right-to-left.

    ``compose(f, g, h)(x)`` calls ``h(x)`` first, feeds its return value to
    ``g``, then feeds that to ``f`` — equivalent to ``f(g(h(x)))``. Only the
    rightmost function receives the original call's arguments; every other
    function is called with exactly one argument, the previous function's
    return value.

        >>> compose(str, lambda x: x + 1)(2)
        '3'
        >>> compose(str.upper, str.strip)("  hi  ")
        'HI'

    Calling ``compose()`` with no arguments returns the identity function,
    which returns its single argument unchanged:

        >>> compose()(5)
        5

    Raises ``TypeError`` if any argument is not callable; this is checked
    eagerly, when ``compose()`` is called, not when the result is.
    """
    for func in funcs:
        if not callable(func):
            raise TypeError(f"compose() arguments must be callable, got {func!r}")

    if not funcs:

        def identity(value: T) -> T:
            return value

        return identity

    *rest, innermost = funcs

    def composed(*args: Any, **kwargs: Any) -> Any:
        result = innermost(*args, **kwargs)
        for func in reversed(rest):
            result = func(result)
        return result

    return composed


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
