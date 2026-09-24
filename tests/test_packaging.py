import importlib.resources


def test_py_typed_marker_is_shipped_with_the_package():
    """PEP 561: the marker must sit inside the installed ``toolbelt`` package."""
    marker = importlib.resources.files("toolbelt").joinpath("py.typed")
    assert marker.is_file()
    assert marker.read_text() == ""
