import pytest

from toolbelt.text import (
    camel_case,
    common_prefix,
    human_bytes,
    mask,
    ordinal,
    pluralize,
    slugify,
    snake_case,
    strip_ansi,
    truncate,
    word_wrap,
)


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


class TestSnakeCase:
    def test_converts_camel_case(self):
        assert snake_case("helloWorld") == "hello_world"

    def test_converts_pascal_case(self):
        assert snake_case("HelloWorld") == "hello_world"

    def test_converts_kebab_case(self):
        assert snake_case("hello-world") == "hello_world"

    def test_converts_spaced_words(self):
        assert snake_case("Hello World") == "hello_world"

    def test_keeps_leading_acronym_together(self):
        assert snake_case("HTTPServer") == "http_server"

    def test_keeps_mid_word_acronym_together(self):
        assert snake_case("parseHTTPResponse") == "parse_http_response"

    def test_mixed_separators_normalise_to_underscore(self):
        assert snake_case("already-snake_case Words") == "already_snake_case_words"

    def test_empty_input_returns_empty_string(self):
        assert snake_case("") == ""

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError):
            snake_case(123)


class TestOrdinal:
    def test_common_suffixes(self):
        assert ordinal(1) == "1st"
        assert ordinal(2) == "2nd"
        assert ordinal(3) == "3rd"
        assert ordinal(4) == "4th"

    def test_eleven_to_thirteen_are_always_th(self):
        assert ordinal(11) == "11th"
        assert ordinal(12) == "12th"
        assert ordinal(13) == "13th"

    def test_larger_numbers_ending_in_eleven_to_thirteen_are_th(self):
        assert ordinal(111) == "111th"
        assert ordinal(112) == "112th"
        assert ordinal(113) == "113th"

    def test_larger_numbers_follow_last_digit(self):
        assert ordinal(21) == "21st"
        assert ordinal(22) == "22nd"
        assert ordinal(23) == "23rd"

    def test_zero_is_th(self):
        assert ordinal(0) == "0th"

    def test_negative_numbers_keep_sign(self):
        assert ordinal(-1) == "-1st"
        assert ordinal(-12) == "-12th"

    def test_non_int_raises_type_error(self):
        with pytest.raises(TypeError):
            ordinal("1")


class TestCamelCase:
    def test_converts_snake_case(self):
        assert camel_case("convert_to_camel_case") == "convertToCamelCase"

    def test_converts_kebab_case(self):
        assert camel_case("convert-to-camel-case") == "convertToCamelCase"

    def test_converts_spaced_words(self):
        assert camel_case("convert to camel case") == "convertToCamelCase"

    def test_keeps_mid_word_acronym_uppercase(self):
        assert camel_case("parse_HTTP_response") == "parseHTTPResponse"

    def test_lowercases_leading_acronym(self):
        assert camel_case("HTTP_server") == "httpServer"

    def test_single_word_is_lowercased(self):
        assert camel_case("Hello") == "hello"

    def test_empty_input_returns_empty_string(self):
        assert camel_case("") == ""

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError):
            camel_case(123)


class TestPluralize:
    def test_singular_count_uses_singular_form(self):
        assert pluralize(1, "file") == "1 file"

    def test_plural_count_appends_s_by_default(self):
        assert pluralize(3, "file") == "3 files"

    def test_zero_uses_plural_form(self):
        assert pluralize(0, "file") == "0 files"

    def test_negative_one_uses_singular_form(self):
        assert pluralize(-1, "file") == "-1 file"

    def test_other_negative_counts_use_plural_form(self):
        assert pluralize(-3, "file") == "-3 files"

    def test_irregular_plural_is_used_when_given(self):
        assert pluralize(2, "child", "children") == "2 children"
        assert pluralize(1, "child", "children") == "1 child"

    def test_empty_singular_still_produces_a_result(self):
        assert pluralize(1, "") == "1 "
        assert pluralize(2, "") == "2 s"

    def test_non_int_count_raises_type_error(self):
        with pytest.raises(TypeError):
            pluralize("1", "file")


class TestMask:
    def test_hides_all_but_last_visible_characters(self):
        assert mask("1234567812345678") == "************5678"

    def test_custom_visible_count(self):
        assert mask("1234567812345678", visible=2) == "**************78"

    def test_custom_mask_character(self):
        assert mask("secret", visible=0, char="#") == "######"

    def test_value_no_longer_than_visible_is_unchanged(self):
        assert mask("hi", visible=4) == "hi"
        assert mask("ab", visible=2) == "ab"

    def test_empty_input_returns_empty_string(self):
        assert mask("") == ""

    def test_negative_visible_raises_value_error(self):
        with pytest.raises(ValueError):
            mask("secret", visible=-1)

    def test_multi_character_char_raises_value_error(self):
        with pytest.raises(ValueError):
            mask("secret", char="**")


class TestHumanBytes:
    def test_bytes_under_base_are_a_bare_integer(self):
        assert human_bytes(500) == "500 B"

    def test_zero_is_zero_bytes(self):
        assert human_bytes(0) == "0 B"

    def test_binary_scaling_uses_1024_and_i_units(self):
        assert human_bytes(1536) == "1.5 KiB"
        assert human_bytes(1024) == "1.0 KiB"

    def test_decimal_scaling_uses_1000_and_plain_units(self):
        assert human_bytes(1_600_000, binary=False) == "1.6 MB"

    def test_float_input_is_accepted(self):
        assert human_bytes(1536.0) == "1.5 KiB"

    def test_large_value_climbs_multiple_units(self):
        assert human_bytes(1024**3) == "1.0 GiB"

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            human_bytes(-1)

    def test_non_numeric_raises_type_error(self):
        with pytest.raises(TypeError):
            human_bytes("1024")

    def test_bool_raises_type_error(self):
        with pytest.raises(TypeError):
            human_bytes(True)
