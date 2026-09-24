import pytest

from toolbelt.text import slugify, truncate


class TestSlugify:
    def test_lowercases_and_joins_words(self):
        assert slugify("Hello World") == "hello-world"

    def test_folds_accents_to_ascii(self):
        assert slugify("Crème Brûlée, please!") == "creme-brulee-please"

    def test_collapses_runs_of_punctuation(self):
        assert slugify("a -- b__c") == "a-b-c"

    def test_strips_leading_and_trailing_separators(self):
        assert slugify("  !hi!  ") == "hi"

    def test_honours_custom_separator(self):
        assert slugify("Hello World", separator="_") == "hello_world"

    def test_string_with_no_alphanumerics_becomes_empty(self):
        assert slugify("!!!") == ""

    def test_multi_char_separator_does_not_eat_shared_letters(self):
        # Regression: str.strip(separator) treats a multi-character separator
        # as a set of characters, not a literal substring, so a naive fix
        # would strip the trailing "an" from "banana" down to "b".
        assert slugify("banana!!!", separator="an") == "banana"

    def test_multi_char_separator_still_strips_from_both_ends(self):
        assert slugify("__hello__", separator="__") == "hello"

    def test_multi_char_separator_keeps_content_ending_in_separator(self):
        assert slugify("Japan!", separator="an") == "japan"

    def test_empty_separator_collapses_without_stripping(self):
        assert slugify("hi!!", separator="") == "hi"


class TestTruncate:
    def test_short_string_is_unchanged(self):
        assert truncate("hello", 10) == "hello"

    def test_exact_length_is_unchanged(self):
        assert truncate("hello", 5) == "hello"

    def test_breaks_on_word_boundary(self):
        assert truncate("hello brave world", 12) == "hello brave…"

    def test_result_never_exceeds_limit(self):
        assert len(truncate("hello brave world", 12)) <= 12

    def test_single_long_word_is_cut_mid_word(self):
        assert truncate("supercalifragilistic", 8) == "superca…"

    def test_custom_suffix(self):
        assert truncate("hello brave world", 12, suffix="...") == "hello..."

    def test_limit_smaller_than_suffix_raises(self):
        with pytest.raises(ValueError):
            truncate("hello", 1, suffix="...")
