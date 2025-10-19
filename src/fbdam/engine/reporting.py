"""
reporting.py — Outputs, metrics, and logs for FBDAM
---------------------------------------------------
Utilities to persist a full "run" with structured artifacts:
- manifest.json with checksums
- JSON metrics (solver, model, KPIs)
- CSV exports for variables and constraints
- Markdown human-readable report
- NDJSON event log

Design goals:
- Pure stdlib + Pyomo (no optional dependencies like pyarrow)
- Idempotent writes (safe to re-run on the same run_dir)
- Narrow, composable functions; the CLI/orchestrator decides what to call
"""

from __future__ import annotations

import os
import io
import csv
import json
import hashlib
import datetime as dt
from typing import Any, Dict, Iterable, List, Tuple, Optional

import pyomo.environ as pyo


# ------------------------------------------------------------
# Filesystem helpers
# ------------------------------------------------------------

def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def write_text(path: str, text: str) -> str:
    """Write UTF-8 text file and return its SHA256 hex digest."""
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return sha256_file(path)


def write_json(path: str, obj: Any, indent: int = 2) -> str:
    """Write JSON file and return its SHA256 hex digest."""
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
    return sha256_file(path)


def sha256_file(path: str) -> str:
    """Compute SHA256 of a file path."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------
# Manifest + logging
# ------------------------------------------------------------

def save_manifest(run_dir: str, artifacts: List[str], meta: Optional[Dict[str, Any]] = None) -> str:
    """
    Create manifest.json in run_dir listing artifact checksums + metadata.

    Args:
        run_dir: base directory for a single run
        artifacts: list of relative paths inside run_dir
        meta: optional metadata to embed (run id, env, times, etc.)

    Returns:
        SHA256 digest of the written manifest.json
    """
    meta = meta or {}
    manifest = dict(meta)  # shallow copy
    rows = []
    for rel in artifacts:
        path = os.path.join(run_dir, rel)
        rows.append({"path": rel, "sha256": sha256_file(path)})
    manifest["artifacts"] = rows
    path = os.path.join(run_dir, "manifest.json")
    return write_json(path, manifest)


def log_event_ndjson(path: str, event: Dict[str, Any]) -> None:
    """
    Append a single event to an NDJSON log file with UTC timestamp.
    """
    _ensure_parent(path)
    row = {"t": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", **event}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ------------------------------------------------------------
# Model statistics extraction
# ------------------------------------------------------------

def extract_model_stats(model: pyo.ConcreteModel) -> Dict[str, Any]:
    """
    Compute counts of variables/constraints by component and type.

    Returns:
        {
          "model": {
            "vars_total": int,
            "vars_by_domain": {"x[i,h]": 200, ...},
            "vars_by_type": {"Binary": 10, "Integer": 5, "Continuous": 123},
            "cons_total": int,
            "cons_by_block": {"U_link": 120, ...}
          }
        }
    """
    # Variables
    vars_by_domain: Dict[str, int] = {}
    vars_by_type: Dict[str, int] = {"Binary": 0, "Integer": 0, "Continuous": 0}
    total_vars = 0

    for var in model.component_objects(pyo.Var, active=True):
        name = var.getname()
        count = sum(1 for _ in var.index_set())
        vars_by_domain[name] = vars_by_domain.get(name, 0) + count
        total_vars += count

        # Type classification (best effort)
        vdomain = var.domain
        if vdomain is pyo.Binary:
            vars_by_type["Binary"] += count
        elif vdomain in (pyo.Integers, pyo.PositiveIntegers, pyo.NonNegativeIntegers):
            vars_by_type["Integer"] += count
        else:
            # Everything else considered continuous (NonNegativeReals, Reals, etc.)
            vars_by_type["Continuous"] += count

    # Constraints
    cons_by_block: Dict[str, int] = {}
    total_cons = 0
    for cons in model.component_objects(pyo.Constraint, active=True):
        name = cons.getname()
        count = sum(1 for _ in cons.index_set()) if cons.is_indexed() else 1
        cons_by_block[name] = cons_by_block.get(name, 0) + count
        total_cons += count

    return {
        "model": {
            "vars_total": total_vars,
            "vars_by_domain": vars_by_domain,
            "vars_by_type": vars_by_type,
            "cons_total": total_cons,
            "cons_by_block": cons_by_block,
        }
    }


# ------------------------------------------------------------
# CSV exports
# ------------------------------------------------------------

def _write_csv(path: str, header: List[str], rows: Iterable[List[Any]]) -> str:
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return sha256_file(path)


def write_variables_csv(model: pyo.ConcreteModel, path: str) -> str:
    """
    Export all active variables to a wide CSV.
    Columns: var, i, h, n, index_extra, value, lb, ub

    - For index tuples longer than 3, extra components go to index_extra (repr).
    - lb/ub extracted per VarData (best-effort; may be None).
    """
    header = ["var", "i", "h", "n", "index_extra", "value", "lb", "ub"]
    def _rows():
        for var in model.component_objects(pyo.Var, active=True):
            vname = var.getname()
            for idx in var:
                v = var[idx]
                value = pyo.value(v)
                lb = v.lb if hasattr(v, "lb") else None
                ub = v.ub if hasattr(v, "ub") else None
                # normalize index
                if isinstance(idx, tuple):
                    i, h, n, extra = _split_index(idx)
                else:
                    i, h, n, extra = _split_index((idx,))
                yield [vname, i, h, n, extra, value, lb, ub]
    return _write_csv(path, header, _rows())


def write_constraints_csv(model: pyo.ConcreteModel, path: str) -> str:
    """
    Export constraint activities to CSV (best-effort).
    Columns: cons, i, h, n, index_extra, lower, body, upper, activity, slack_lower, slack_upper, dual

    Notes:
    - 'dual' requires a Suffix('dual') populated by the solver (LPs).
    - Slack is computed when bounds exist; otherwise left blank.
    """
    header = ["cons", "i", "h", "n", "index_extra",
              "lower", "body", "upper", "activity", "slack_lower", "slack_upper", "dual"]

    # Optional dual suffix
    duals = None
    for suf in model.component_objects(pyo.Suffix, active=True):
        if suf.getname() == "dual":
            duals = suf
            break

    def _rows():
        for cons in model.component_objects(pyo.Constraint, active=True):
            cname = cons.getname()
            if cons.is_indexed():
                iterator = cons.items()
            else:
                iterator = [ (None, cons) ]
            for key, c in iterator:
                lower = pyo.value(c.lower) if c.has_lb() else None
                upper = pyo.value(c.upper) if c.has_ub() else None
                body  = pyo.value(c.body)
                activity = body
                sL = (activity - lower) if lower is not None else None
                sU = (upper - activity) if upper is not None else None

                # dual value (if available)
                dual = None
                try:
                    if duals is not None:
                        dual = duals[c]
                except Exception:
                    dual = None

                # split index
                if key is None:
                    i, h, n, extra = None, None, None, ""
                else:
                    if not isinstance(key, tuple):
                        key = (key,)
                    i, h, n, extra = _split_index(key)

                yield [cname, i, h, n, extra, lower, body, upper, activity, sL, sU, dual]

    return _write_csv(path, header, _rows())


def write_solution_csv(model: pyo.ConcreteModel, path: str, var_name: str = "x") -> str:
    """
    Convenience export for a primary allocation variable (default: 'x[i,h]').
    Columns: item, household, value
    Skips entries with value==0 (to keep file compact).
    """
    header = ["item", "household", "value"]
    var = getattr(model, var_name, None)
    if var is None:
        # Nothing to export
        return _write_csv(path, header, [])

    def _rows():
        for idx in var:
            v = var[idx]
            val = pyo.value(v)
            if not val:
                continue
            # assume (i,h) index; tolerate scalars/tuples
            if isinstance(idx, tuple):
                item = idx[0] if len(idx) > 0 else None
                hh = idx[1] if len(idx) > 1 else None
            else:
                item, hh = idx, None
            yield [item, hh, val]

    return _write_csv(path, header, _rows())


# ------------------------------------------------------------
# Markdown report
# ------------------------------------------------------------

def write_markdown_summary(path: str,
                           solver_report: Dict[str, Any],
                           kpis: Optional[Dict[str, Any]] = None,
                           model_stats: Optional[Dict[str, Any]] = None,
                           title: str = "FBDAM Run Report") -> str:
    """
    Create a human-readable Markdown summary file.
    """
    kpis = kpis or {}
    model_stats = model_stats or {}

    lines: List[str] = []
    lines.append(f"# {title}")
    run_id = solver_report.get("run", {}).get("id", "")
    if run_id:
        lines.append(f"\n**Run ID:** `{run_id}`\n")

    # Solver
    s = solver_report.get("solver", {})
    lines.append("## Solver summary")
    lines.append(f"- Solver: {s.get('name','')}")
    lines.append(f"- Status: {s.get('status','')}")
    lines.append(f"- Termination: {s.get('termination','')}")
    if "obj_value" in s:
        lines.append(f"- Objective value: {s.get('obj_value')}")
    if "gap" in s:
        lines.append(f"- Gap: {s.get('gap')}")
    if "best_bound" in s:
        lines.append(f"- Best bound: {s.get('best_bound')}")
    wc = solver_report.get("run", {}).get("wall_clock_sec")
    if wc is not None:
        lines.append(f"- Wall-clock time (s): {wc}")

    # KPIs
    if kpis:
        lines.append("\n## KPIs")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        for k, v in (kpis.get("kpi", kpis)).items():
            lines.append(f"| {k} | {v} |")

    # Model stats
    if model_stats:
        ms = model_stats.get("model", model_stats)
        lines.append("\n## Model stats")
        lines.append(f"- Vars total: {ms.get('vars_total','')}")
        lines.append(f"- Cons total: {ms.get('cons_total','')}")
        if "vars_by_domain" in ms:
            lines.append("\n**Vars by domain**")
            for k, v in ms["vars_by_domain"].items():
                lines.append(f"- {k}: {v}")
        if "cons_by_block" in ms:
            lines.append("\n**Constraints by block**")
            for k, v in ms["cons_by_block"].items():
                lines.append(f"- {k}: {v}")

    text = "\n".join(lines) + "\n"
    return write_text(path, text)


# ------------------------------------------------------------
# Index utilities
# ------------------------------------------------------------

def _split_index(idx: Tuple[Any, ...]) -> Tuple[Optional[Any], Optional[Any], Optional[Any], str]:
    """
    Normalize an index tuple into (i, h, n, extra_repr).

    Examples:
      () -> (None, None, None, '')
      ('i',) -> ('i', None, None, '')
      ('i','h') -> ('i','h', None, '')
      ('n','h','z','extra') -> ('n','h','z', '(extra)')
    """
    i = idx[0] if len(idx) > 0 else None
    h = idx[1] if len(idx) > 1 else None
    n = idx[2] if len(idx) > 2 else None
    extra = ""
    if len(idx) > 3:
        extra = "(" + ", ".join(repr(x) for x in idx[3:]) + ")"
    return i, h, n, extra
