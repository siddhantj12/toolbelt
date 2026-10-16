import pytest

from toolbelt.functional import once


class TestOnce:
    def test_runs_func_only_on_first_call(self):
        calls = []

        @once
        def record(value):
            calls.append(value)
            return value

        assert record("a") == "a"
        assert record("b") == "a"
        assert record("c") == "a"
        assert calls == ["a"]

    def test_works_with_a_no_argument_function(self):
        calls = 0

        @once
        def setup():
            nonlocal calls
            calls += 1
            return "ready"

        assert setup() == "ready"
        assert setup() == "ready"
        assert calls == 1

    def test_caches_and_replays_the_exception_without_retrying(self):
        calls = 0

        @once
        def boom():
            nonlocal calls
            calls += 1
            raise ValueError("no")

        with pytest.raises(ValueError, match="no"):
            boom()
        with pytest.raises(ValueError, match="no"):
            boom()
        assert calls == 1
