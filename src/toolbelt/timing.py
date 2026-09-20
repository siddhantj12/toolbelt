"""Timing helpers."""

from __future__ import annotations

import functools
import time
from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = ["retry"]


def retry(
    attempts: int, backoff: float = 0.0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Return a decorator that retries a failing call up to ``attempts`` times.

    The wrapped function is called immediately; if it raises, the call is
    retried until it succeeds or ``attempts`` calls have been made in total.
    Between retries the decorator sleeps ``backoff * 2 ** attempt`` seconds
    (``attempt`` starting at 0), so the delay doubles after every failure.
    Pass ``backoff=0`` (the default) to retry without waiting. On success the
    function's return value is passed through unchanged; if every attempt
    raises, the exception from the *last* attempt propagates. Raises
    ``ValueError`` if ``attempts`` is less than 1.

        >>> calls = []
        >>> @retry(attempts=3, backoff=0)
        ... def flaky():
        ...     calls.append(1)
        ...     if len(calls) < 2:
        ...         raise RuntimeError("not yet")
        ...     return "ok"
        >>> flaky()
        'ok'
        >>> len(calls)
        2
    """
    if attempts < 1:
        raise ValueError(f"attempts must be at least 1, got {attempts}")

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> T:
            for attempt in range(attempts - 1):
                try:
                    return func(*args, **kwargs)
                except Exception:  # noqa: BLE001 - retry must catch any failure
                    if backoff:
                        time.sleep(backoff * 2**attempt)
            return func(*args, **kwargs)

        return wrapper

    return decorator
