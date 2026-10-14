import pytest

from toolbelt.timing import human_duration


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
