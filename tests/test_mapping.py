import pytest

from toolbelt.mapping import deep_merge, get_path, invert


class TestDeepMerge:
    def test_merges_nested_dicts_recursively(self):
        a = {"a": 1, "opts": {"x": 1, "y": 2}}
        b = {"opts": {"y": 3, "z": 4}}
        assert deep_merge(a, b) == {"a": 1, "opts": {"x": 1, "y": 3, "z": 4}}

    def test_non_dict_conflict_takes_b_outright(self):
        assert deep_merge({"x": {"y": 1}}, {"x": 5}) == {"x": 5}

    def test_does_not_mutate_inputs(self):
        a = {"opts": {"x": 1}}
        b = {"opts": {"y": 2}}
        deep_merge(a, b)
        assert a == {"opts": {"x": 1}}
        assert b == {"opts": {"y": 2}}

    def test_empty_inputs_yield_a_copy_of_the_other(self):
        assert deep_merge({}, {}) == {}
        assert deep_merge({"a": 1}, {}) == {"a": 1}
        assert deep_merge({}, {"a": 1}) == {"a": 1}

    def test_non_dict_argument_raises(self):
        with pytest.raises(TypeError):
            deep_merge({"a": 1}, None)


class TestGetPath:
    def test_looks_up_nested_value(self):
        assert get_path({"a": {"b": {"c": 1}}}, "a.b.c") == 1

    def test_single_segment_path(self):
        assert get_path({"a": 1}, "a") == 1

    def test_missing_segment_returns_default(self):
        assert get_path({"a": {}}, "a.b.c", default="missing") == "missing"

    def test_missing_segment_defaults_to_none(self):
        assert get_path({"a": {}}, "a.b.c") is None

    def test_non_mapping_value_along_path_returns_default(self):
        assert get_path({"a": [1, 2, 3]}, "a.b", default="missing") == "missing"

    def test_empty_mapping_returns_default(self):
        assert get_path({}, "a.b.c", default="missing") == "missing"

    def test_non_mapping_argument_raises(self):
        with pytest.raises(TypeError):
            get_path(["a", "b"], "a.b")


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
