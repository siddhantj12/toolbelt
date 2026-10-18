import pytest

from toolbelt.files import atomic_write


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
