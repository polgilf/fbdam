"""Utility script to delete files and directories from a target path.

Example usage::

    python utilities/clear_path.py outputs/demo
    python utilities/clear_path.py outputs/demo --create-dir

Programmatic use::

    from pathlib import Path
    from utilities.clear_path import clear_path

    clear_path(Path("outputs/demo"), create_dir=True)

The script removes all files and sub-directories located at the provided
``path`` while keeping the directory itself (if it is a directory).
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable


def _iter_children(path: Path) -> Iterable[Path]:
    """Yield direct children of *path* sorted for deterministic output."""
    return sorted(path.iterdir(), key=lambda child: child.name)


def clear_path(path: Path, *, create_dir: bool = False) -> None:
    """Delete the target path or, if it is a directory, all of its contents.

    Parameters
    ----------
    path:
        The path to delete. If *path* points to a directory, the directory is
        preserved but all of its contents are removed. If *path* points to a
        file or a symbolic link it is removed directly.
    create_dir:
        When *True*, create the directory (and any parents) if it does not
        already exist. This is useful in build scripts where a clean output
        directory should always be present after calling :func:`clear_path`.
    """

    if not path.exists():
        if not create_dir:
            print(f"Path '{path}' does not exist. Nothing to delete.")
            return

        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")
        return

    if path.is_file() or path.is_symlink():
        path.unlink()
        print(f"Deleted file: {path}")
        return

    if not path.is_dir():
        raise ValueError(f"Unsupported path type for '{path}'.")

    removed_anything = False
    for child in _iter_children(path):
        removed_anything = True
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
            print(f"Deleted directory: {child}")
        else:
            child.unlink()
            print(f"Deleted file: {child}")

    if removed_anything:
        print(f"Cleared contents of directory: {path}")
    else:
        print(f"Directory '{path}' was already empty.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Delete files and folders from a specified path. If the path is a "
            "directory, only its contents are deleted."
        )
    )
    parser.add_argument(
        "path",
        type=Path,
        help=(
            "Path to delete. Provide a directory to clear its contents or a "
            "file path to delete a specific file."
        ),
    )
    parser.add_argument(
        "--create-dir",
        action="store_true",
        help=(
            "If the target directory does not exist, create it (including "
            "any parents) instead of treating the call as a no-op."
        ),
    )

    args = parser.parse_args()
    try:
        clear_path(args.path, create_dir=args.create_dir)
    except Exception as exc:  # pragma: no cover - CLI guard
        parser.error(str(exc))


if __name__ == "__main__":
    main()
