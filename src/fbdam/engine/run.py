"""CLI entry point for orchestrating the FBDAM pipeline.

The command defined here drives the full optimisation workflow and now
distinguishes between feasible and infeasible solves, surfacing diagnostic
information without aborting the run.  Artifacts are always produced, even
when the solver cannot find a feasible solution.
"""

from __future__ import annotations

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
from fbdam.engine.reporting import write_report  # stub function is fine initially
from fbdam.utils import make_run_id, parse_run_id, slugify_run_name

app = typer.Typer(add_completion=False, help="FBDAM — minimal optimization system")
console = Console()
rich_traceback(show_locals=False)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _generate_run_id(scenario_path: Path, started_at: datetime) -> str:
    """Create a filesystem-friendly run identifier."""
    stem = scenario_path.stem or "run"
    slug = slugify_run_name(stem)
    return make_run_id(slug, started_at)


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
    export_mps: bool = typer.Option(
        True,
        "--export-mps/--no-export-mps",
        help="Export the model to MPS format (standard LP/MIP format).",
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

        outputs_root = outputs.expanduser().resolve()
        if run_id:
            try:
                run_identifier = parse_run_id(run_id)["id"]
            except ValueError:
                run_identifier = str(run_id)
        else:
            run_identifier = _generate_run_id(scenario, started_at)
        run_dir = outputs_root / run_identifier
        run_dir.mkdir(parents=True, exist_ok=True)

        cfg_snapshot = _snapshot_config(cfg.raw, scenario, run_identifier)

        solver_options = dict(cfg.solver.options or {})
        log_relative_path = None
        log_file = solver_options.get("log_file")
        if log_file:
            log_path = run_dir / Path(str(log_file)).name
            log_path.parent.mkdir(parents=True, exist_ok=True)
            solver_options["log_file"] = str(log_path)
            log_relative_path = log_path.relative_to(run_dir)

        # 2) Build model (Pyomo)
        model = build_model(cfg)  # can be a stub returning a sentinel for now

        # 3) Solve model
        results = solve_model(model, solver_name=cfg.solver.name, options=solver_options)

        # 4) Reporting
        manifest = write_report(
            model=model,
            solver_results=results,
            domain=cfg.domain,
            cfg_snapshot=cfg_snapshot,
            run_dir=run_dir,
            run_id=run_identifier,
            include_constraints_activity=include_constraints_activity,
            solver_log_relative_path=str(log_relative_path) if log_relative_path else None,
            export_mps=export_mps,
        )

        manifest_path = run_dir / "manifest.json"
        is_feasible = results.get("is_feasible", True)
        termination = results.get("termination", "unknown")
        status = results.get("status", "unknown")

        if is_feasible:
            panel_lines = [
                "[bold green]Pipeline finished successfully[/]",
                f"Run ID: [bold]{run_identifier}[/]",
                f"Artifacts dir: {run_dir}",
                f"Manifest entries: {len(manifest.get('artifacts', []))}",
                f"Manifest path: {manifest_path}",
            ]
            console.print(
                Panel.fit(
                    "\n".join(panel_lines),
                    border_style="green",
                )
            )
        else:
            solver_log_display = "N/A"
            if log_relative_path:
                solver_log_display = str(run_dir / log_relative_path)
            mps_display = str(run_dir / "model.mps") if export_mps else "N/A"
            panel_lines = [
                f"Termination: {termination}",
                f"Status: {status}",
                "",
                "[dim]Diagnostic artifacts saved:[/]",
                f"Run ID: [bold]{run_identifier}[/]",
                f"Artifacts dir: {run_dir}",
                f"Solver log: {solver_log_display}",
                f"Model MPS: {mps_display}",
                f"Manifest path: {manifest_path}",
            ]
            console.print(
                Panel.fit(
                    "\n".join(panel_lines),
                    title="[bold yellow]Model is INFEASIBLE[/]",
                    border_style="yellow",
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
