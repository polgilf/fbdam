"""
reporting.py — Output generation and run artifacts
--------------------------------------------------
Creates structured outputs for a single optimization run:
- Manifest with checksums
- Snapshots (config/domain)
- Solver report and model stats
- KPIs placeholder
- Variables table (Parquet/CSV fallback)
- Constraints activity (optional)
- Human-readable solution extract
- Markdown report
- NDJSON logs

Public helpers:
  - write_report(...)
  - save_manifest(...)
  - write_json(...)
  - write_markdown_summary(...)
  - write_variables_parquet(...)
  - write_constraints_parquet(...)
  - write_solution_csv(...)
  - log_event_ndjson(...)
  - extract_model_stats(...)
  - snapshot_domain(...)

Notes:
- Does not perform any solving or building; only consumes results/model/domain.
- Parquet writing requires 'pyarrow'. Falls back to CSV if unavailable.
"""

from __future__ import annotations

import json
import os
import sys
import hashlib
import datetime as dt
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional

import pandas as pd
import pyomo.environ as pyo

from fbdam.engine.domain import DomainIndex


# ---------------------------------------------------------------------
# Core entry point
# ---------------------------------------------------------------------

def write_report(
    model: pyo.ConcreteModel,
    solver_results: Dict[str, Any],
    domain: DomainIndex,
    cfg_snapshot: Dict[str, Any],
    run_dir: Path,
    run_id: Optional[str] = None,
    kpis: Optional[Dict[str, Any]] = None,
    include_constraints_activity: bool = False,
) -> Dict[str, Any]:
    """
    Generate all run artifacts into run_dir.

    Args:
        model: Solved Pyomo model (has m.OBJ, m.x, etc.)
        solver_results: dict returned by solve_model(...)
        domain: DomainIndex used to build the model
        cfg_snapshot: dict with expanded scenario/config (ready-to-dump YAML/JSON)
        run_dir: base directory for artifacts (will be created)
        run_id: optional custom id; default uses UTC timestamp
        kpis: optional domain KPI dict; default minimal KPIs are computed
        include_constraints_activity: compute constraint activities/slacks (slower)

    Returns:
        manifest dict
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    if not run_id:
        run_id = dt.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")

    # ---- snapshots & reports ----
    config_path = run_dir / "config_snapshot.yaml"
    domain_path = run_dir / "domain_snapshot.json"
    solver_path = run_dir / "solver_report.json"
    model_stats_path = run_dir / "model_stats.json"
    kpis_path = run_dir / "kpis.json"
    vars_parquet = run_dir / "variables.parquet"
    vars_csv_fallback = run_dir / "variables.csv"
    cons_parquet = run_dir / "constraints_activity.parquet"
    cons_csv_fallback = run_dir / "constraints_activity.csv"
    sol_csv = run_dir / "solution.csv"
    md_report = run_dir / "report.md"
    text_log = run_dir / "run.log"
    jsonl_log = run_dir / "run.ndjson"
    manifest_path = run_dir / "manifest.json"

    # 1) Save snapshots / reports
    _write_yaml_like(config_path, cfg_snapshot)  # YAML-ish with safe dumping
    write_json(domain_path, snapshot_domain(domain))
    write_json(solver_path, _normalize_solver_report(solver_results))
    model_stats = extract_model_stats(model)
    write_json(model_stats_path, model_stats)

    # 2) KPIs (minimal defaults if none provided)
    if kpis is None:
        kpis = _compute_minimal_kpis(model)
    write_json(kpis_path, {"kpi": kpis})

    # 3) Variables table (Parquet or CSV fallback)
    wrote_parquet = write_variables_parquet(model, vars_parquet)
    if not wrote_parquet:
        _variables_to_csv(model, vars_csv_fallback)

    # 4) Constraints activity/slacks (optional)
    if include_constraints_activity:
        wrote_parquet_cons = write_constraints_parquet(model, cons_parquet)
        if not wrote_parquet_cons:
            _constraints_to_csv(model, cons_csv_fallback)

    # 5) Human oriented solution extract
    write_solution_csv(model, sol_csv)

    # 6) Markdown summary
    write_markdown_summary(
        md_report,
        solver=_normalize_solver_report(solver_results),
        kpis=kpis,
        model_stats=model_stats,
        run_id=run_id,
    )

    # 7) Logs (empty initialize)
    text_log.touch()
    Path(jsonl_log).touch()
    log_event_ndjson(jsonl_log, {"event": "reporting.completed", "run_id": run_id})

    # 8) Manifest with checksums
    manifest = build_manifest(
        run_id=run_id,
        artifacts=[
            config_path, domain_path, solver_path, model_stats_path,
            kpis_path, (vars_parquet if wrote_parquet else vars_csv_fallback),
            (cons_parquet if (include_constraints_activity and wrote_parquet_cons) else None),
            sol_csv, md_report, text_log, jsonl_log
        ]
    )
    save_manifest(manifest_path, manifest)

    return manifest


# ---------------------------------------------------------------------
# JSON / YAML / Markdown utilities
# ---------------------------------------------------------------------

def write_json(path: Path, obj: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_yaml_like(path: Path, obj: Any) -> None:
    """
    Safe 'YAML-like' writer: if PyYAML is installed uses YAML,
    otherwise falls back to JSON with a YAML extension.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(obj, f, allow_unicode=True, sort_keys=False)
    except Exception:
        with path.open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)


def write_markdown_summary(
    path: Path,
    solver: Dict[str, Any],
    kpis: Dict[str, Any],
    model_stats: Dict[str, Any],
    run_id: str,
) -> None:
    """
    Write a small human-readable Markdown summary.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f"# FBDAM Run Summary — `{run_id}`\n")
    lines.append("## Solver\n")
    lines.append(f"- **Name:** {solver.get('solver')}")
    lines.append(f"- **Status:** {solver.get('status')}")
    lines.append(f"- **Termination:** {solver.get('termination')}")
    lines.append(f"- **Wall clock (s):** {solver.get('elapsed_sec')}")
    lines.append(f"- **Objective:** {solver.get('objective_value')}\n")

    lines.append("## Model Stats\n")
    lines.append(f"- **Variables (total):** {model_stats['model']['vars_total']}")
    lines.append(f"- **Constraints (total):** {model_stats['model']['cons_total']}")
    lines.append("- **Variables by domain:**")
    for k, v in model_stats["model"]["vars_by_domain"].items():
        lines.append(f"  - {k}: {v}")
    lines.append("- **Constraints by block:**")
    for k, v in model_stats["model"]["cons_by_block"].items():
        lines.append(f"  - {k}: {v}")
    lines.append("")

    lines.append("## KPIs\n")
    for k, v in kpis.items():
        lines.append(f"- **{k}:** {v}")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------
# Variables / Constraints tables
# ---------------------------------------------------------------------

def write_variables_parquet(model: pyo.ConcreteModel, path: Path) -> bool:
    """
    Dump variables to a long table and write Parquet.
    Returns True if Parquet was written; False if fell back to CSV elsewhere.
    """
    df = _variables_dataframe(model)
    try:
        import pyarrow  # noqa: F401
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
        return True
    except Exception:
        return False


def write_constraints_parquet(model: pyo.ConcreteModel, path: Path) -> bool:
    """
    Dump constraint activities/slacks to Parquet (best effort).
    Returns True if Parquet was written; False otherwise.
    """
    df = _constraints_dataframe(model)
    try:
        import pyarrow  # noqa: F401
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
        return True
    except Exception:
        return False


def write_solution_csv(model: pyo.ConcreteModel, path: Path) -> None:
    """
    Produce a human-oriented CSV focusing on x[i,h] allocations and
    simple aggregates per household and per item.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    # Long format: x[i,h]
    if hasattr(model, "x"):
        for (i, h) in model.x:
            rows.append({"var": "x", "i": str(i), "h": str(h), "value": _safe_value(model.x[i, h])})

    df = pd.DataFrame(rows, columns=["var", "i", "h", "value"])
    # Append totals
    if not df.empty:
        by_h = df.groupby("h")["value"].sum().reset_index().rename(columns={"value": "total_x_by_h"})
        by_i = df.groupby("i")["value"].sum().reset_index().rename(columns={"value": "total_x_by_i"})
        # Write three tabs as separate CSV blocks (simple and robust)
        with path.open("w", encoding="utf-8") as f:
            f.write("# allocations (long)\n")
            df.to_csv(f, index=False)
            f.write("\n# totals by household (sum x)\n")
            by_h.to_csv(f, index=False)
            f.write("\n# totals by item (sum x)\n")
            by_i.to_csv(f, index=False)
    else:
        df.to_csv(path, index=False)


# ---------------------------------------------------------------------
# Logs / Manifest
# ---------------------------------------------------------------------

def log_event_ndjson(path: Path, event: Dict[str, Any]) -> None:
    """
    Append a JSON object as a single line in an NDJSON file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    evt = {"t": dt.datetime.utcnow().isoformat() + "Z", **event}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")


def build_manifest(run_id: str, artifacts: Iterable[Optional[Path]]) -> Dict[str, Any]:
    """
    Create a manifest dict with checksums for given artifact paths.
    """
    arts = []
    for p in artifacts:
        if p is None:
            continue
        p = Path(p)
        arts.append({"path": str(p.name), "sha256": _sha256_of_file(p) if p.exists() else None})

    manifest = {
        "run_id": run_id,
        "started_at": None,            # may be filled by caller if known
        "finished_at": dt.datetime.utcnow().isoformat() + "Z",
        "environment": _env_snapshot(),
        "artifacts": arts,
    }
    return manifest


def save_manifest(path: Path, manifest: Dict[str, Any]) -> None:
    write_json(path, manifest)


# ---------------------------------------------------------------------
# Model/domain snapshots and stats
# ---------------------------------------------------------------------

def extract_model_stats(model: pyo.ConcreteModel) -> Dict[str, Any]:
    """
    Count variables/constraints and group by component name and type.
    """
    vars_by_domain: Dict[str, int] = {}
    vars_by_type: Dict[str, int] = {}
    vars_total = 0

    for var in model.component_objects(pyo.Var, active=True):
        vname = var.getname()
        count = 0
        vtype_counts: Dict[str, int] = {}
        for idx in var:
            count += 1
            dom = getattr(var[idx].domain, "name", str(var[idx].domain))
            vtype_counts[dom] = vtype_counts.get(dom, 0) + 1
        vars_by_domain[vname] = count
        vars_total += count
        for k, v in vtype_counts.items():
            vars_by_type[k] = vars_by_type.get(k, 0) + v

    cons_by_block: Dict[str, int] = {}
    cons_total = 0
    for con in model.component_objects(pyo.Constraint, active=True):
        cname = con.getname()
        # some constraints may be scalar (no indices)
        if con.is_indexed():
            cnt = len(list(con.index_set()))
        else:
            cnt = 1
        cons_by_block[cname] = cnt
        cons_total += cnt

    return {
        "model": {
            "vars_total": vars_total,
            "vars_by_domain": vars_by_domain,
            "vars_by_type": vars_by_type,
            "cons_total": cons_total,
            "cons_by_block": cons_by_block,
        }
    }


def snapshot_domain(domain: DomainIndex) -> Dict[str, Any]:
    """
    Minimal domain snapshot for reproducibility and quick diagnostics.
    """
    # Counts
    i_cnt = len(domain.items)
    n_cnt = len(domain.nutrients)
    h_cnt = len(domain.households)
    bounds_cnt = len(domain.bounds)
    req_cnt = len(domain.requirements)

    # Non-zero requirements
    nonzero_R = sum(1 for (_, _), r in domain.requirements.items() if r.amount > 0)

    return {
        "domain": {
            "items": i_cnt,
            "nutrients": n_cnt,
            "households": h_cnt,
            "bounds_pairs": bounds_cnt,
            "requirements_pairs": req_cnt,
            "requirements_nonzero": nonzero_R,
        }
    }


# ---------------------------------------------------------------------
# Internals — DataFrame builders and CSV fallbacks
# ---------------------------------------------------------------------

def _variables_dataframe(model: pyo.ConcreteModel) -> pd.DataFrame:
    """
    Build a long table of variables with normalized index columns.
    Columns: var, i, h, n, k, value, lower, upper
    """
    rows = []
    for var in model.component_objects(pyo.Var, active=True):
        vname = var.getname()
        for idx in var:
            val = _safe_value(var[idx])
            lb, ub = _safe_bounds(var, idx)
            # Normalize index tuple → up to 4 columns; extra indices go to 'k'
            idx_tuple = idx if isinstance(idx, tuple) else (idx,)
            norm = _normalize_index(idx_tuple)
            rows.append({
                "var": vname,
                **norm,           # i/h/n/k columns
                "value": val,
                "lower": lb,
                "upper": ub,
            })
    cols = ["var", "i", "h", "n", "k", "value", "lower", "upper"]
    df = pd.DataFrame(rows, columns=cols).fillna("")
    return df


def _constraints_dataframe(model: pyo.ConcreteModel) -> pd.DataFrame:
    """
    Build a long table of constraint activities/slacks (best effort).
    Columns: cons, i, h, n, k, activity, lower, upper, slack_lower, slack_upper
    """
    rows = []
    for con in model.component_objects(pyo.Constraint, active=True):
        cname = con.getname()
        if con.is_indexed():
            indices = list(con.index_set())
            iterator = indices
        else:
            iterator = [None]

        for idx in iterator:
            c = con if idx is None else con[idx]
            try:
                activity = pyo.value(c.body)
            except Exception:
                activity = None
            lower = _to_float(c.lower) if c.lower is not None else None
            upper = _to_float(c.upper) if c.upper is not None else None
            slack_lower = (activity - lower) if (activity is not None and lower is not None) else None
            slack_upper = (upper - activity) if (activity is not None and upper is not None) else None

            idx_tuple = idx if isinstance(idx, tuple) else (() if idx is None else (idx,))
            norm = _normalize_index(idx_tuple)
            rows.append({
                "cons": cname,
                **norm,
                "activity": activity,
                "lower": lower,
                "upper": upper,
                "slack_lower": slack_lower,
                "slack_upper": slack_upper,
            })

    cols = ["cons", "i", "h", "n", "k", "activity", "lower", "upper", "slack_lower", "slack_upper"]
    df = pd.DataFrame(rows, columns=cols).fillna("")
    return df


def _variables_to_csv(model: pyo.ConcreteModel, path: Path) -> None:
    df = _variables_dataframe(model)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _constraints_to_csv(model: pyo.ConcreteModel, path: Path) -> None:
    df = _constraints_dataframe(model)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


# ---------------------------------------------------------------------
# Tiny helpers
# ---------------------------------------------------------------------

def _safe_value(v) -> Optional[float]:
    try:
        return pyo.value(v)
    except Exception:
        return None


def _safe_bounds(var, idx) -> tuple[Optional[float], Optional[float]]:
    try:
        b = var[idx].bounds
        if b is None:
            return (None, None)
        lb = _to_float(b[0]) if b[0] is not None else None
        ub = _to_float(b[1]) if b[1] is not None else None
        return (lb, ub)
    except Exception:
        return (None, None)


def _to_float(x) -> Optional[float]:
    try:
        return float(pyo.value(x))
    except Exception:
        try:
            return float(x)
        except Exception:
            return None


def _normalize_index(idx_tuple: tuple) -> Dict[str, str]:
    """
    Map an index tuple to named columns: (i, h, n, k)
    Any extra dims are concatenated into 'k'.
    """
    parts = list(map(str, idx_tuple))
    out = {"i": "", "h": "", "n": "", "k": ""}
    if len(parts) > 0:
        out["i"] = parts[0]
    if len(parts) > 1:
        out["h"] = parts[1]
    if len(parts) > 2:
        out["n"] = parts[2]
    if len(parts) > 3:
        out["k"] = "|".join(parts[3:])
    return out


def _env_snapshot() -> Dict[str, Any]:
    import platform
    try:
        import pyomo  # type: ignore
        pyomo_ver = getattr(pyomo, "__version__", None)
    except Exception:
        pyomo_ver = None
    return {
        "python": platform.python_version(),
        "pyomo": pyomo_ver,
        "platform": platform.platform(),
        "executable": sys.executable,
    }


def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalize_solver_report(res: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure consistent fields in solver report.
    """
    return {
        "solver": res.get("solver"),
        "elapsed_sec": res.get("elapsed_sec"),
        "status": res.get("status"),
        "termination": res.get("termination"),
        "objective_value": res.get("objective_value"),
        "gap": res.get("gap"),               # may be absent; keep None
        "best_bound": res.get("best_bound")  # may be absent; keep None
    }


def _compute_minimal_kpis(model: pyo.ConcreteModel) -> Dict[str, Any]:
    """
    Minimal domain-agnostic KPIs:
      - tnu: total sum of u[n,h]
      - u_min: minimum utility over all (n,h)
      - u_mean: mean utility across (n,h)
    """
    tnu = None
    u_min = None
    u_mean = None

    if hasattr(model, "u"):
        vals = [ _safe_value(model.u[n, h]) for n in model.N for h in model.H ]
        vals = [v for v in vals if v is not None]
        if vals:
            tnu = float(sum(vals))
            u_min = float(min(vals))
            u_mean = float(sum(vals) / len(vals))
    return {"tnu": tnu, "u_min": u_min, "u_mean": u_mean}
