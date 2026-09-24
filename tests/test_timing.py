import pytest

from toolbelt.timing import retry


class TestRetry:
    def test_returns_result_on_first_success(self):
        calls = []

        @retry(attempts=3, backoff=0)
        def succeeds():
            calls.append(1)
            return "ok"

        assert succeeds() == "ok"
        assert len(calls) == 1

    def test_retries_until_success(self):
        calls = []

        @retry(attempts=3, backoff=0)
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise RuntimeError("not yet")
            return "ok"

        assert flaky() == "ok"
        assert len(calls) == 3

    def test_raises_last_exception_after_exhausting_attempts(self):
        calls = []

        @retry(attempts=3, backoff=0)
        def always_fails():
            calls.append(1)
            raise ValueError(f"attempt {len(calls)}")

        with pytest.raises(ValueError, match="attempt 3"):
            always_fails()
        assert len(calls) == 3

    def test_sleeps_with_doubling_backoff_between_attempts(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr("toolbelt.timing.time.sleep", sleeps.append)

        calls = []

        @retry(attempts=4, backoff=0.5)
        def always_fails():
            calls.append(1)
            raise RuntimeError("nope")

        with pytest.raises(RuntimeError):
            always_fails()
        assert sleeps == [0.5, 1.0, 2.0]

    def test_attempts_below_one_raises(self):
        with pytest.raises(ValueError):
            retry(attempts=0)
