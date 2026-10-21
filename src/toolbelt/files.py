"""File helpers."""

from __future__ import annotations

import contextlib
import os
import tempfile
from pathlib import Path

__all__ = ["atomic_write", "read_lines"]


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

    If ``path`` already exists, its permission bits are carried over to the
    replacement file, so overwriting a world-readable config file doesn't
    silently leave it readable only by its owner. A newly created file gets
    the temporary file's own restrictive permissions, same as before.

    ``text`` may be ``""``, which (over)writes ``path`` with an empty file.
    Raises ``FileNotFoundError`` if ``path``'s parent directory does not
    exist, since there is nowhere to create the temporary file.
    """
    target = Path(path)
    try:
        mode = target.stat().st_mode & 0o777
    except FileNotFoundError:
        mode = None
    fd, tmp_path = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as tmp_file:
            tmp_file.write(text)
        if mode is not None:
            os.chmod(tmp_path, mode)
        os.replace(tmp_path, target)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_path)
        raise


def read_lines(
    path: str | os.PathLike[str],
    *,
    strip: bool = True,
    skip_blank: bool = True,
    encoding: str = "utf-8",
) -> list[str]:
    """Return the lines of the text file at ``path`` as a list of strings.

    The file is read in one pass and split on universal newlines, so no
    line in the result ever includes its trailing newline. ``strip``
    (default ``True``) removes each line's leading and trailing whitespace;
    set it to ``False`` to keep a line's own leading/trailing spaces exactly
    as written. ``skip_blank`` (default ``True``) drops lines that are empty
    or whitespace-only — that check looks at the line's stripped text
    regardless of ``strip``, so a line of only spaces is dropped even when
    ``strip=False`` keeps every other line's spacing intact.

        >>> from pathlib import Path
        >>> import tempfile
        >>> target = Path(tempfile.mkdtemp()) / "notes.txt"
        >>> _ = target.write_text("  first  \\n\\n  second\\n")
        >>> read_lines(target)
        ['first', 'second']
        >>> read_lines(target, strip=False, skip_blank=False)
        ['  first  ', '', '  second']

    An empty file returns ``[]``. Raises ``FileNotFoundError`` if ``path``
    does not exist.
    """
    lines = Path(path).read_text(encoding=encoding).splitlines()
    if strip:
        lines = [line.strip() for line in lines]
    if skip_blank:
        lines = [line for line in lines if line.strip()]
    return lines
