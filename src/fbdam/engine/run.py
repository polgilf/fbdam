"""
run.py — CLI entry point for FBDAM
----------------------------------
Orchestrates the end-to-end pipeline:
  1) Load scenario (YAML) → validated config
  2) Build model (Pyomo) from config
  3) Solve model with selected solver/backend
  4) Generate outputs (reports, tables, metadata)

This is a minimal, production-ready skeleton:
- Typer-based CLI
- Clear error handling and exit codes
- Non-intrusive logging with Rich
- Paths resolved relative to the scenario file
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install as rich_traceback

# Pipeline imports (expected to exist in the same package)
from fbdam.engine.io import load_scenario, IOConfigError
from fbdam.engine.model import build_model  # stub function is fine initially
from fbdam.engine.solver import solve_model  # stub function is fine initially
from fbdam.engine.reporting_old import write_report  # stub function is fine initially

app = typer.Typer(add_completion=False, help="FBDAM — minimal optimization system")
console = Console()
rich_traceback(show_locals=False)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _generate_run_id(scenario_path: Path, started_at: datetime) -> str:
    """Create a filesystem-friendly run identifier."""
    stem = scenario_path.stem or "run"
    slug_chars = []
    for ch in stem.lower():
        if ch.isalnum() or ch in {"-", "_"}:
            slug_chars.append(ch)
        else:
            slug_chars.append("-")
    slug = "".join(slug_chars).strip("-_") or "run"
    timestamp = started_at.strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{slug}"


def _snapshot_config(raw_cfg: dict, scenario_path: Path, run_id: str) -> dict:
    """Build a serializable snapshot of the run configuration."""
    snapshot = dict(raw_cfg)
    snapshot.setdefault("metadata", {})
    if isinstance(snapshot["metadata"], dict):
        snapshot["metadata"] = dict(snapshot["metadata"])
    else:
        snapshot["metadata"] = {"original": snapshot["metadata"]}
    snapshot["metadata"].update(
        {
            "scenario_path": str(scenario_path),
            "generated_at": _utc_now_iso().replace("+00:00", "Z"),
            "run_id": run_id,
        }
    )
    return snapshot


@app.callback()
def main_callback() -> None:
    """Global options (extend in the future if needed)."""
    # Reserved for global flags like --verbose / --no-color / --profile, etc.
    return


@app.command("run")
def run(
    scenario: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path to the scenario YAML file.",
    ),
    outputs: Path = typer.Option(
        Path("outputs") / "runs",
        "--outputs",
        "-o",
        help="Directory where run folders will be created (defaults to outputs/runs).",
    ),
    solver: str = typer.Option(
        None,
        "--solver",
        help="Optional solver name override (e.g., 'appsi_highs' or 'highs'). "
             "If omitted, the scenario's solver.name is used.",
    ),
    run_id: Optional[str] = typer.Option(
        None,
        "--run-id",
        help="Optional run identifier to name the run folder. If omitted, a timestamp-based id is used.",
    ),
    include_constraints_activity: bool = typer.Option(
        False,
        "--constraints-activity/--no-constraints-activity",
        help="Export constraint activity/slacks tables (may be slow).",
    ),
) -> None:
    """
    Execute the full pipeline: load → build → solve → report.
    """
    started_at = datetime.now(timezone.utc)
    t0 = started_at.isoformat(timespec="seconds")
    console.print(Panel.fit(f"[bold cyan]FBDAM pipeline started[/]  [dim]{t0} UTC[/]"))

    try:
        # 1) Load scenario (validated + normalized)
        cfg = load_scenario(scenario)

        # Optional solver override
        if solver:
            new_solver = type(cfg.solver)(name=solver, options=cfg.solver.options)
            new_raw = cfg.raw | {"solver": {"name": solver, "options": cfg.solver.options}}
            cfg = replace(cfg, solver=new_solver, raw=new_raw)

        # 2) Build model (Pyomo)
        model = build_model(cfg)  # can be a stub returning a sentinel for now

        # 3) Solve model
        results = solve_model(model, solver_name=cfg.solver.name, options=cfg.solver.options)

        # 4) Reporting
        outputs_root = outputs.expanduser().resolve()
        run_identifier = run_id or _generate_run_id(scenario, started_at)
        run_dir = outputs_root / run_identifier
        run_dir.mkdir(parents=True, exist_ok=True)

        cfg_snapshot = _snapshot_config(cfg.raw, scenario, run_identifier)
        manifest = write_report(
            model=model,
            solver_results=results,
            domain=cfg.domain,
            cfg_snapshot=cfg_snapshot,
            run_dir=run_dir,
            run_id=run_identifier,
            include_constraints_activity=include_constraints_activity,
        )

        manifest_path = run_dir / "manifest.json"
        console.print(
            Panel.fit(
                "\n".join(
                    [
                        "[bold green]Pipeline finished successfully[/]",
                        f"Run ID: [bold]{run_identifier}[/]",
                        f"Artifacts dir: {run_dir}",
                        f"Manifest entries: {len(manifest.get('artifacts', []))}",
                        f"Manifest path: {manifest_path}",
                    ]
                ),
                border_style="green",
            )
        )
    except IOConfigError as e:
        console.print(Panel.fit(f"[bold red]Scenario/IO error[/]\n{e}", border_style="red"))
        raise typer.Exit(code=2)
    except FileNotFoundError as e:
        console.print(Panel.fit(f"[bold red]File not found[/]\n{e}", border_style="red"))
        raise typer.Exit(code=3)
    except Exception as e:  # pragma: no cover
        console.print(Panel.fit(f"[bold red]Unhandled error[/]\n{e}", border_style="red"))
        raise typer.Exit(code=1)


@app.command("version")
def version() -> None:
    """Print version information."""
    # Lazy import to avoid import cycles if __init__ evolves
    try:
        from importlib.metadata import version as _pkg_version
        v = _pkg_version("fbdam")
    except Exception:
        v = "0.1.0 (dev)"
    console.print(f"fbdam {v}")


if __name__ == "__main__":
    app()
