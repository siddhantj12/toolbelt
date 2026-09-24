import pytest

from toolbelt.mapping import deep_merge


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
