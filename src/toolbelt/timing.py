"""Timing helpers."""

from __future__ import annotations

import time

__all__ = ["Timer"]


class Timer:
    """Measure wall-clock elapsed time with a context manager.

    Use it as ``with Timer() as t: ...``. ``t.elapsed`` (a float, in seconds)
    is readable at any point after entering: it keeps advancing while the
    block is still running, and freezes at the moment the block exits, even
    if the block raised. Reading ``.elapsed`` before entering the context
    raises ``RuntimeError``, since nothing has been measured yet.

        >>> import time
        >>> with Timer() as t:
        ...     time.sleep(0.01)
        >>> t.elapsed >= 0.01
        True
        >>> repr(t)
        'Timer(elapsed=0.0101s)'
    """

    def __init__(self) -> None:
        self._start: float | None = None
        self._end: float | None = None

    def __enter__(self):
        self._start = time.perf_counter()
        self._end = None
        return self

    def __exit__(self, *exc_info: object) -> None:
        self._end = time.perf_counter()

    @property
    def elapsed(self) -> float:
        """Seconds elapsed since entering, frozen once the block exits."""
        if self._start is None:
            raise RuntimeError("Timer.elapsed read before the context was entered")
        end = self._end if self._end is not None else time.perf_counter()
        return end - self._start

    def __repr__(self) -> str:
        if self._start is None:
            return "Timer(not started)"
        return f"Timer(elapsed={self.elapsed:.4f}s)"
