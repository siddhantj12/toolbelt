import pytest

from toolbelt.mapping import invert


class TestInvert:
    def test_swaps_keys_and_values(self):
        assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_colliding_values_keep_the_last_key(self):
        assert invert({"a": 1, "b": 1}) == {1: "b"}

    def test_empty_input_returns_empty_dict(self):
        assert invert({}) == {}

    def test_does_not_mutate_input(self):
        original = {"a": 1, "b": 2}
        invert(original)
        assert original == {"a": 1, "b": 2}

    def test_non_mapping_argument_raises(self):
        with pytest.raises(TypeError):
            invert([("a", 1), ("b", 2)])

    def test_unhashable_value_raises(self):
        with pytest.raises(TypeError):
            invert({"a": [1, 2]})
