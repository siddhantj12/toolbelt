import pytest

from toolbelt.text import slugify, truncate, word_wrap


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


class TestWordWrap:
    def test_wraps_at_width(self):
        assert word_wrap("one two three four", 10) == "one two\nthree four"

    def test_preserves_paragraph_breaks(self):
        text = "first para\n\nsecond para"
        assert word_wrap(text, 20) == "first para\n\nsecond para"

    def test_collapses_single_newlines_within_a_paragraph(self):
        assert word_wrap("one two\nthree four", 100) == "one two three four"

    def test_long_word_is_kept_whole(self):
        assert word_wrap("supercalifragilistic", 8) == "supercalifragilistic"

    def test_no_line_exceeds_width_except_a_single_long_word(self):
        result = word_wrap("the quick brown fox jumps over", 10)
        assert all(len(line) <= 10 for line in result.split("\n"))

    def test_empty_input_returns_empty_string(self):
        assert word_wrap("", 10) == ""

    def test_whitespace_only_input_returns_empty_string(self):
        assert word_wrap("   \n\n  ", 10) == ""

    def test_width_below_one_raises(self):
        with pytest.raises(ValueError):
            word_wrap("hello", 0)
