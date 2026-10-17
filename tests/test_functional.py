import pytest

from toolbelt.functional import compose, once


class TestCompose:
    def test_applies_functions_right_to_left(self):
        assert compose(str, lambda x: x + 1)(2) == "3"
        assert compose(str.upper, str.strip)("  hi  ") == "HI"

    def test_passes_through_the_outermost_calls_arguments_to_the_innermost_func(self):
        assert compose(str, lambda a, b: a + b)(2, 3) == "5"

    def test_no_functions_returns_the_identity_function(self):
        identity = compose()
        assert identity(5) == 5
        assert identity("hi") == "hi"

    def test_raises_type_error_for_a_non_callable_argument(self):
        with pytest.raises(TypeError, match="must be callable"):
            compose(str, 1)


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
