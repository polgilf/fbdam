from __future__ import annotations

import argparse
import random
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Mapping

import yaml

from fbdam.config.runtime import MaterializedScenario, ScenarioLoadError, load_materialized_scenario
from fbdam.engine.model import build_model
from fbdam.engine.reporting import write_report
from fbdam.engine.solver import solve_model
from fbdam.utils import build_run_dir, make_run_id

DEFAULT_SOLVER_NAME = "appsi_highs"


def _timestamp_id(prefix: str) -> str:
    now = datetime.now(timezone.utc)
    return make_run_id(prefix, now)


def _merge_solver_defaults(defaults: Mapping[str, object], overrides: Dict[str, object]) -> Dict[str, object]:
    merged = dict(defaults)
    for key, value in overrides.items():
        if value is None:
            continue
        merged[key] = value
    return merged


def _solver_options_from_effective(effective: Mapping[str, object]) -> Dict[str, object]:
    options: Dict[str, object] = {}
    time_limit = float(effective.get("time_limit_s") or 0)
    if time_limit > 0:
        options["time_limit"] = time_limit
    mip_gap = float(effective.get("mip_gap") or 0)
    if mip_gap > 0:
        options["mip_rel_gap"] = mip_gap
    threads = effective.get("threads")
    if threads not in (None, "auto"):
        options["threads"] = threads
    return options


def _write_run_params(run_dir: Path, params: Dict[str, object]) -> Path:
    path = run_dir / "run_params.yaml"
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(params, handle, sort_keys=False)
    return path


def _effective_model_config(materialized: MaterializedScenario) -> Mapping[str, object]:
    return materialized.config


def run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FBDAM run orchestrator")
    parser.add_argument("--scenario", required=True, help="Scenario identifier (config/scenario)")
    parser.add_argument("--run-id", dest="run_id", help="Optional run identifier")
    parser.add_argument("--seed", type=int, default=1, help="Random seed")
    parser.add_argument("--time-limit", type=float, default=None, help="Override time limit (seconds)")
    parser.add_argument("--mip-gap", type=float, default=None, help="Override MIP gap")
    parser.add_argument("--threads", default=None, help="Override solver threads")

    args = parser.parse_args(argv)

    try:
        materialized = load_materialized_scenario(args.scenario)
    except ScenarioLoadError as exc:
        print(f"Error: {exc}")
        return 2

    config = _effective_model_config(materialized)
    if not isinstance(config, Mapping):
        print("Error: configuration is not a mapping")
        return 3

    solver_defaults = config.get("solver_defaults", {}) if isinstance(config, Mapping) else {}
    overrides = {
        "time_limit_s": args.time_limit,
        "mip_gap": args.mip_gap,
        "threads": args.threads,
    }
    effective_solver = _merge_solver_defaults(solver_defaults, overrides)

    run_id = args.run_id or _timestamp_id(materialized.scenario_id)
    run_dir = build_run_dir(materialized.dataset_id, materialized.config_id, run_id)

    argv_for_log = argv if argv is not None else sys.argv[1:]

    run_params = {
        "run_id": run_id,
        "scenario_id": materialized.scenario_id,
        "seed": int(args.seed),
        "overrides": {
            "solver": {k: effective_solver.get(k) for k in ("time_limit_s", "mip_gap", "threads")},
            "model": {},
        },
        "flags": {"quick_qa": True},
        "cli": {"argv": shlex.join([sys.executable or "python"] + list(argv_for_log))},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _write_run_params(run_dir, run_params)

    random.seed(args.seed)

    model = build_model(materialized.domain, config)
    solver_name = DEFAULT_SOLVER_NAME
    solver_options = _solver_options_from_effective(effective_solver)
    solver_report = solve_model(model, solver_name=solver_name, options=solver_options)

    constraint_ids = config["model"]["structure"]["constraints"]
    dials = config["model"].get("dials", {})

    write_report(
        model=model,
        domain=materialized.domain,
        solver_report=solver_report,
        run_dir=run_dir,
        dataset_id=materialized.dataset_id,
        config_id=materialized.config_id,
        scenario_id=materialized.scenario_id,
        run_id=run_id,
        seed=int(args.seed),
        effective_solver=effective_solver,
        dials=dials,
        constraint_ids=constraint_ids,
        dataset_metadata=materialized.dataset_metadata,
        scenario_filters=materialized.scenario_filters,
    )

    return 0


def main() -> None:
    sys.exit(run_cli())


if __name__ == "__main__":
    main()
