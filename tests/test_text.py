import pytest

from toolbelt.text import common_prefix, slugify, truncate, word_wrap


class TestCommonPrefix:
    def test_shared_leading_substring(self):
        assert common_prefix(["flower", "flow", "flight"]) == "fl"

    def test_no_shared_characters_returns_empty_string(self):
        assert common_prefix(["dog", "cat"]) == ""

    def test_single_string_is_returned_unchanged(self):
        assert common_prefix(["hello"]) == "hello"

    def test_empty_string_in_input_yields_empty_prefix(self):
        assert common_prefix(["", "abc"]) == ""

    def test_empty_sequence_raises(self):
        with pytest.raises(ValueError):
            common_prefix([])


from toolbelt.text import strip_ansi


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

    def test_leading_space_does_not_discard_all_content(self):
        assert truncate(" hello", 3) == " h…"

    def test_word_boundary_at_very_start_falls_back_to_char_cut(self):
        assert truncate(" abcdef", 4) == " ab…"



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
