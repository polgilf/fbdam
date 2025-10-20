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

# Optional: expose the CLI runner for programmatic invocation
try:
    from fbdam.run import run_cli as cli_main
except Exception:  # pragma: no cover
    cli_main = None  # CLI may be unavailable in minimal installs

__all__ = [
    "__version__",
    "build_model",
    "solve_model",
    "write_report",
    "cli_main",
]
