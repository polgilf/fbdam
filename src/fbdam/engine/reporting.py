from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Mapping

import yaml

import pyomo.environ as pyo

from fbdam.engine.domain import DomainIndex
from fbdam.engine.kpis import compute_metrics


def _git_revision() -> str:
    try:
        rev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=Path.cwd())
        return rev.decode().strip()
    except Exception:  # pragma: no cover - best effort only
        return "unknown"


def _value(component: pyo.Component) -> float:
    return float(pyo.value(component, exception=False) or 0.0)


def _serialise_allocations(model: pyo.ConcreteModel) -> Dict[str, Dict[str, float]]:
    allocations: Dict[str, Dict[str, float]] = {}
    for i in model.I:
        allocations[i] = {h: _value(model.x[i, h]) for h in model.H}
    return allocations


def write_report(
    *,
    model: pyo.ConcreteModel,
    domain: DomainIndex,
    solver_report: Mapping[str, object],
    run_dir: Path,
    dataset_id: str,
    config_id: str,
    scenario_id: str,
    run_id: str,
    seed: int,
    effective_solver: Mapping[str, object],
    dials: Mapping[str, object],
    constraint_ids: Iterable[str],
    dataset_metadata: Mapping[str, object],
    scenario_filters: Mapping[str, object],
) -> Dict[str, str]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(exist_ok=True)

    metrics = compute_metrics(model, domain, solver_report)
    metrics_path = run_dir / "metrics.json"
    with metrics_path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    atom = {
        "meta": {
            "dataset_id": dataset_id,
            "config_id": config_id,
            "scenario_id": scenario_id,
            "run_id": run_id,
            "code_revision": _git_revision(),
            "constraints_used": list(constraint_ids),
            "dataset_metadata": dict(dataset_metadata),
            "scenario_filters": dict(scenario_filters),
            "exec": {
                "seed": seed,
                "effective_solver": dict(effective_solver),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "model_effective_dials": dict(dials),
        },
        "solution": {
            "allocations": _serialise_allocations(model),
            "satisfaction": {h: _value(model.s[h]) for h in model.H},
        },
        "aggregates": {
            "tnu": metrics["tnu"],
            "household_allocation": {h: _value(model.household_allocation[h]) for h in model.H},
            "total_supply": _value(model.total_supply),
            "total_requirement": _value(model.total_requirement),
        },
    }

    atom_path = run_dir / "atom.yaml"
    with atom_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(atom, handle, sort_keys=False)

    log_path = run_dir / "logs" / "solver.log"
    with log_path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(solver_report, indent=2, sort_keys=True))

    return {"atom": str(atom_path), "metrics": str(metrics_path), "log": str(log_path)}


__all__ = ["write_report"]
