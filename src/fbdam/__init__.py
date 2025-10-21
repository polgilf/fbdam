"""
fbdam — Food Basket Design and Allocation Model
------------------------------------------------
Top-level package for the FBDAM optimization system.

This module exposes a concise, friendly API for common tasks:

    from fbdam import build_model, solve_model, write_report
    # or run the CLI (if installed with entry point):
    #   fbdam --help

Design notes:
- Keep imports lightweight to avoid side effects.
- Export only stable, high-level entry points.
"""

# Package version (sync with pyproject.toml)
__version__ = "0.1.0"

# High-level, stable API imports (do NOT re-export submodules wholesale)
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report

# Optional: expose the Typer CLI app (if you want programmatic access).
#
# Importing ``fbdam`` as part of ``python -m fbdam.engine.run`` previously
# imported the CLI module eagerly, which triggered a ``runpy`` warning because
# the module was already present in ``sys.modules`` before the interpreter tried
# to execute it as ``__main__``.  We now defer the import until the attribute is
# actually requested.

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - type checkers only
    from typer import Typer as _Typer

    cli_app: _Typer


def __getattr__(name: str):
    if name == "cli_app":
        try:
            from fbdam.engine.run import app as _cli_app
        except Exception as exc:  # pragma: no cover - propagate as attribute error
            raise AttributeError("CLI application is unavailable") from exc
        globals()[name] = _cli_app
        return _cli_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["__version__", "build_model", "solve_model", "write_report", "cli_app"]
