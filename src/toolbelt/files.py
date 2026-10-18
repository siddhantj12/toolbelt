"""File helpers."""

from __future__ import annotations

import contextlib
import os
import tempfile
from pathlib import Path

__all__ = ["atomic_write"]


def atomic_write(path: str | os.PathLike[str], text: str, *, encoding: str = "utf-8") -> None:
    """Write ``text`` to ``path`` as a single atomic operation.

    ``text`` is written to a temporary file in ``path``'s own directory and
    then moved into place with ``os.replace``. Because that move is atomic,
    a reader opening ``path`` at any point sees either the previous contents
    in full or the new ones in full — never a partially written file — and
    a crash mid-write leaves the original file (if any) untouched rather
    than truncated.

        >>> import tempfile
        >>> target = Path(tempfile.mkdtemp()) / "config.txt"
        >>> atomic_write(target, "hello")
        >>> target.read_text()
        'hello'

    ``text`` may be ``""``, which (over)writes ``path`` with an empty file.
    Raises ``FileNotFoundError`` if ``path``'s parent directory does not
    exist, since there is nowhere to create the temporary file.
    """
    target = Path(path)
    fd, tmp_path = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as tmp_file:
            tmp_file.write(text)
        os.replace(tmp_path, target)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_path)
        raise
