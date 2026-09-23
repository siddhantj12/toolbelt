from hypothesis import given, strategies as st

from toolbelt.text import slugify


@given(st.text())
def test_slugify_is_idempotent(value):
    once = slugify(value)
    assert slugify(once) == once


@given(st.text(), st.sampled_from(["-", "_", ".", "~~", ""]))
def test_slugify_is_idempotent_with_custom_separator(value, separator):
    once = slugify(value, separator=separator)
    assert slugify(once, separator=separator) == once
