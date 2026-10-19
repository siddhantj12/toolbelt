import pytest

from toolbelt.files import atomic_write, read_lines


class TestAtomicWrite:
    def test_writes_text_to_a_new_file(self, tmp_path):
        target = tmp_path / "config.txt"
        atomic_write(target, "hello")
        assert target.read_text() == "hello"

    def test_overwrites_an_existing_file(self, tmp_path):
        target = tmp_path / "config.txt"
        target.write_text("old")
        atomic_write(target, "new")
        assert target.read_text() == "new"

    def test_leaves_no_temp_file_behind(self, tmp_path):
        atomic_write(tmp_path / "config.txt", "hello")
        assert [p.name for p in tmp_path.iterdir()] == ["config.txt"]

    def test_empty_string_writes_an_empty_file(self, tmp_path):
        target = tmp_path / "config.txt"
        atomic_write(target, "")
        assert target.read_text() == ""

    def test_accepts_a_str_path(self, tmp_path):
        target = tmp_path / "config.txt"
        atomic_write(str(target), "hello")
        assert target.read_text() == "hello"

    def test_missing_parent_directory_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            atomic_write(tmp_path / "missing" / "config.txt", "hello")


class TestReadLines:
    def test_strips_and_skips_blanks_by_default(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("  first  \n\n   \n  second\n")
        assert read_lines(target) == ["first", "second"]

    def test_strip_false_keeps_original_spacing(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("  first  \nsecond\n")
        assert read_lines(target, strip=False) == ["  first  ", "second"]

    def test_skip_blank_false_keeps_blank_lines(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("first\n\nsecond\n")
        assert read_lines(target, skip_blank=False) == ["first", "", "second"]

    def test_strip_false_and_skip_blank_false_keeps_everything(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("  first  \n\n  second\n")
        assert read_lines(target, strip=False, skip_blank=False) == [
            "  first  ",
            "",
            "  second",
        ]

    def test_whitespace_only_line_is_dropped_even_without_strip(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("first\n   \nsecond\n")
        assert read_lines(target, strip=False) == ["first", "second"]

    def test_empty_file_returns_empty_list(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("")
        assert read_lines(target) == []

    def test_accepts_a_str_path(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("first\nsecond\n")
        assert read_lines(str(target)) == ["first", "second"]

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            read_lines(tmp_path / "missing.txt")
