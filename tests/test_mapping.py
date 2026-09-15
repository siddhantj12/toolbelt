import pytest

from toolbelt.mapping import get_path


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
