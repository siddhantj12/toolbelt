import importlib.resources

import toolbelt.text


def test_py_typed_marker_is_shipped_with_the_package():
    """PEP 561: the marker must sit inside the installed ``toolbelt`` package."""
    marker = importlib.resources.files("toolbelt").joinpath("py.typed")
    assert marker.is_file()
    assert marker.read_text() == ""


def test_text_module_declares_all_to_scope_star_imports():
    """Regression: every other submodule defines ``__all__`` except
    ``toolbelt.text``, so ``from toolbelt.text import *`` pulled in its
    ``re``, ``textwrap`` and ``unicodedata`` imports alongside the intended
    public functions. ``__all__`` is what ``import *`` consults, so pinning
    it to exactly the public functions closes that leak."""
    assert set(toolbelt.text.__all__) == {
        "camel_case",
        "common_prefix",
        "human_bytes",
        "mask",
        "ordinal",
        "pluralize",
        "slugify",
        "snake_case",
        "strip_ansi",
        "truncate",
        "word_wrap",
    }
    assert "re" not in toolbelt.text.__all__
    assert "textwrap" not in toolbelt.text.__all__
    assert "unicodedata" not in toolbelt.text.__all__
