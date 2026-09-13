import pytest

from toolbelt.text import slugify, strip_ansi, truncate


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


class TestStripAnsi:
    def test_removes_color_codes(self):
        assert strip_ansi("\x1b[31mError:\x1b[0m disk full") == "Error: disk full"

    def test_removes_cursor_movement_sequences(self):
        assert strip_ansi("\x1b[2Kloading\x1b[1A\x1b[1G") == "loading"

    def test_text_without_escapes_is_unchanged(self):
        assert strip_ansi("plain text") == "plain text"

    def test_empty_input_returns_empty(self):
        assert strip_ansi("") == ""

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError):
            strip_ansi(123)
