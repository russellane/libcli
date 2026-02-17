"""Standalone utility functions."""

import textwrap
from pathlib import Path

__all__ = ["dedent", "hideuser"]


def dedent(text: str) -> str:
    """Make `textwrap.dedent` convenient."""
    return textwrap.dedent(text).strip()


def hideuser(path: Path) -> Path:
    """Replace home with tilde; complements `Path.expanduser`."""
    _path = str(path)
    _home = str(Path.home())
    if not _path.startswith(_home):
        return path
    return Path("~" + _path[len(_home) :])
