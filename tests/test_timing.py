import pytest

from toolbelt.timing import Timer


class TestTimer:
    def test_elapsed_reflects_time_passed_in_block(self, monkeypatch):
        ticks = iter([10.0, 12.5])
        monkeypatch.setattr("time.perf_counter", lambda: next(ticks))

        with Timer() as t:
            pass

        assert t.elapsed == 2.5

    def test_elapsed_keeps_advancing_while_still_running(self, monkeypatch):
        ticks = iter([10.0, 11.0, 13.0, 20.0])
        monkeypatch.setattr("time.perf_counter", lambda: next(ticks))

        t = Timer()
        with t:
            assert t.elapsed == 1.0
            assert t.elapsed == 3.0

    def test_elapsed_freezes_after_the_block_exits_even_on_error(self, monkeypatch):
        ticks = iter([10.0, 14.0])
        monkeypatch.setattr("time.perf_counter", lambda: next(ticks))

        with pytest.raises(ValueError):
            with Timer() as t:
                raise ValueError("boom")

        assert t.elapsed == 4.0
        assert t.elapsed == 4.0

    def test_elapsed_before_entering_raises(self):
        t = Timer()
        with pytest.raises(RuntimeError):
            t.elapsed

    def test_repr_before_and_after_use(self, monkeypatch):
        assert repr(Timer()) == "Timer(not started)"

        ticks = iter([10.0, 10.125])
        monkeypatch.setattr("time.perf_counter", lambda: next(ticks))

        with Timer() as t:
            pass

        assert repr(t) == "Timer(elapsed=0.1250s)"
