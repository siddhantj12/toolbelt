import pytest

from toolbelt.timing import human_duration, parse_duration


class TestHumanDuration:
    def test_combines_hours_minutes_and_seconds(self):
        assert human_duration(3723) == "1h 2m 3s"

    def test_seconds_only_under_a_minute(self):
        assert human_duration(45) == "45s"

    def test_omits_zero_minutes_between_hours_and_seconds(self):
        assert human_duration(3603) == "1h 3s"

    def test_omits_trailing_zero_units(self):
        assert human_duration(3600) == "1h"

    def test_zero_seconds(self):
        assert human_duration(0) == "0s"

    def test_rounds_fractional_seconds(self):
        assert human_duration(1.5) == "2s"
        assert human_duration(0.4) == "0s"

    def test_rounds_half_to_even(self):
        assert human_duration(0.5) == "0s"

    def test_rejects_negative(self):
        with pytest.raises(ValueError):
            human_duration(-1)

    def test_rejects_non_numeric(self):
        with pytest.raises(TypeError):
            human_duration("60")

    def test_rejects_bool(self):
        with pytest.raises(TypeError):
            human_duration(True)


class TestParseDuration:
    def test_combines_hours_minutes_and_seconds(self):
        assert parse_duration("1h 2m 3s") == 3723

    def test_no_spaces(self):
        assert parse_duration("1h30m") == 5400

    def test_seconds_only(self):
        assert parse_duration("45s") == 45

    def test_zero(self):
        assert parse_duration("0s") == 0

    def test_tokens_in_any_order(self):
        assert parse_duration("3s2m1h") == 3723

    def test_inverse_of_human_duration(self):
        for seconds in (0, 45, 3600, 3603, 3723, 86400):
            assert parse_duration(human_duration(seconds)) == seconds

    def test_rejects_empty_string(self):
        with pytest.raises(ValueError):
            parse_duration("")

    def test_rejects_blank_string(self):
        with pytest.raises(ValueError):
            parse_duration("   ")

    def test_rejects_malformed_string(self):
        with pytest.raises(ValueError):
            parse_duration("1h garbage")

    def test_rejects_missing_unit(self):
        with pytest.raises(ValueError):
            parse_duration("1h30")

    def test_rejects_unknown_unit(self):
        with pytest.raises(ValueError):
            parse_duration("1h30d")

    def test_rejects_repeated_unit(self):
        with pytest.raises(ValueError):
            parse_duration("1h2h")

    def test_rejects_non_string(self):
        with pytest.raises(TypeError):
            parse_duration(60)
