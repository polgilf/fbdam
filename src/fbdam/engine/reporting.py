"""Deterministic reporting utilities for FBDAM runs."""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import pyomo.environ as pyo

try:
    from pyomo.opt import ProblemFormat  # type: ignore
except ImportError:  # pragma: no cover - fallback for older Pyomo releases
    ProblemFormat = None  # type: ignore

from fbdam.engine.domain import DomainIndex
from fbdam.engine.kpis import compute_kpis

ArtifactRows = Iterable[Sequence[Any]]


# ---------------------------------------------------------------------------
# Core dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactRecord:
    """Structured description of a generated artifact."""

    path: str
    sha256: str
    kind: str

    def as_dict(self) -> Dict[str, str]:
        return {"path": self.path, "sha256": self.sha256, "kind": self.kind}


@dataclass(frozen=True)
class ReportingContext:
    """Pure container with all data needed to generate report artifacts."""

    model: pyo.ConcreteModel
    solver_report: Dict[str, Any]
    model_stats: Dict[str, Any]
    kpis: Dict[str, Any]
    cfg_snapshot: Mapping[str, Any] | None
    domain: DomainIndex | None
    run_id: str
    run_started_at: str
    solver_log_relative_path: str | None = None


@dataclass(frozen=True)
class ArtifactSpec:
    """Specification linking a relative path with a writer callable."""

    relative_path: str
    kind: str
    writer: Callable[[ReportingContext, str], str]


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------


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


def _write_csv(path: str, header: Sequence[str], rows: ArtifactRows) -> str:
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(list(row))
    return sha256_file(path)


def sha256_file(path: str) -> str:
    """Compute SHA256 of a file path."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Public orchestration entry point
# ---------------------------------------------------------------------------


def write_report(
    *,
    model: pyo.ConcreteModel,
    solver_results: Mapping[str, Any],
    run_dir: os.PathLike[str] | str,
    run_id: str | None = None,
    domain: DomainIndex | None = None,
    cfg_snapshot: Mapping[str, Any] | None = None,
    include_constraints_activity: bool = False,
    export_mps: bool = True,
    title: str = "FBDAM Run Report",
    solver_log_relative_path: str | None = None,
) -> Dict[str, Any]:
    """Generate reporting artifacts for a solved model.

    Parameters
    ----------
    model:
        Solved Pyomo model instance.
    solver_results:
        Mapping produced by :func:`fbdam.engine.solver.solve_model`.
    run_dir:
        Target directory where artifacts will be stored.
    run_id:
        Optional run identifier overriding the generated timestamp-based value.
    domain:
        Optional :class:`DomainIndex` that provides context for KPIs.
    cfg_snapshot:
        Optional configuration snapshot (already validated), persisted for traceability.
    include_constraints_activity:
        When ``True`` dump constraint activities to ``constraints.csv``.
    export_mps:
        When ``True`` emit ``model.mps`` alongside standard artifacts.
    title:
        Heading for the Markdown summary.

    Returns
    -------
    dict
        Manifest with run metadata and artifact descriptors.  The manifest is
        also persisted to ``manifest.json`` inside ``run_dir``.
    """

    run_path = os.fspath(run_dir)
    os.makedirs(run_path, exist_ok=True)

    timestamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    run_started_at = timestamp.isoformat().replace("+00:00", "Z")
    resolved_run_id = run_id or _resolve_run_id(solver_results, run_started_at)

    solver_report = _normalise_solver_report(solver_results, resolved_run_id, run_started_at)
    model_stats = extract_model_stats(model)
    kpis = compute_kpis(model, domain, solver_report)

    context = ReportingContext(
        model=model,
        solver_report=solver_report,
        model_stats=model_stats,
        kpis=kpis,
        cfg_snapshot=cfg_snapshot,
        domain=domain,
        run_id=resolved_run_id,
        run_started_at=run_started_at,
        solver_log_relative_path=solver_log_relative_path,
    )

    artifact_specs = _build_artifact_plan(context, include_constraints_activity, export_mps, title)
    artifact_records: List[ArtifactRecord] = []

    for spec in artifact_specs:
        target = os.path.join(run_path, spec.relative_path)
        checksum = spec.writer(context, target)
        artifact_records.append(ArtifactRecord(spec.relative_path, checksum, spec.kind))

    manifest = build_manifest(context, artifact_records)
    manifest_path = os.path.join(run_path, "manifest.json")
    write_json(manifest_path, manifest)
    return manifest


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------


def build_manifest(context: ReportingContext, artifacts: Sequence[ArtifactRecord]) -> Dict[str, Any]:
    """Create manifest payload from the reporting context and artifacts."""

    return {
        "run": {
            "id": context.run_id,
            "started_at": context.run_started_at,
        },
        "solver": context.solver_report.get("solver", {}),
        "artifacts": [record.as_dict() for record in artifacts],
    }


def _resolve_run_id(solver_results: Mapping[str, Any], timestamp: str) -> str:
    candidate = None
    run_meta = solver_results.get("run") if isinstance(solver_results, Mapping) else None
    if isinstance(run_meta, Mapping):
        candidate = run_meta.get("id")
    if candidate:
        return str(candidate)
    compact = timestamp.replace(":", "").replace("-", "")
    return f"fbdam-{compact}"


# ---------------------------------------------------------------------------
# Artifact plan + writers
# ---------------------------------------------------------------------------


def _build_artifact_plan(
    context: ReportingContext,
    include_constraints: bool,
    export_mps: bool,
    title: str,
) -> List[ArtifactSpec]:
    specs: List[ArtifactSpec] = [
        ArtifactSpec("solver_report.json", "metric", _write_solver_report),
        ArtifactSpec("model_stats.json", "metric", _write_model_stats),
        ArtifactSpec("kpis.json", "metric", _write_kpis),
        ArtifactSpec("variables.csv", "table", _write_variables_csv_artifact),
        ArtifactSpec("solution.csv", "table", _write_solution_csv_artifact),
        ArtifactSpec("report.md", "report", _build_markdown_writer(title)),
    ]

    if context.cfg_snapshot is not None:
        specs.append(ArtifactSpec("config_snapshot.json", "config", _write_config_snapshot))

    if include_constraints:
        specs.append(ArtifactSpec("constraints.csv", "table", _write_constraints_csv_artifact))

    if export_mps:
        specs.append(ArtifactSpec("model.mps", "model", _write_model_mps_artifact))

    if context.solver_log_relative_path:
        specs.append(ArtifactSpec(context.solver_log_relative_path, "log", _register_existing_artifact))

    return specs


def _register_existing_artifact(context: ReportingContext, path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return sha256_file(path)


def _write_solver_report(context: ReportingContext, path: str) -> str:
    return write_json(path, context.solver_report)


def _write_model_stats(context: ReportingContext, path: str) -> str:
    return write_json(path, context.model_stats)


def _write_kpis(context: ReportingContext, path: str) -> str:
    return write_json(path, context.kpis)


def _write_config_snapshot(context: ReportingContext, path: str) -> str:
    return write_json(path, context.cfg_snapshot)


def _write_variables_csv_artifact(context: ReportingContext, path: str) -> str:
    return write_variables_csv(context.model, path)


def _write_constraints_csv_artifact(context: ReportingContext, path: str) -> str:
    return write_constraints_csv(context.model, path)


def _write_solution_csv_artifact(context: ReportingContext, path: str) -> str:
    return write_solution_csv(context.model, path)


def _write_model_mps_artifact(context: ReportingContext, path: str) -> str:
    """Artifact writer for MPS export."""
    return write_model_mps(context.model, path)


def _build_markdown_writer(title: str) -> Callable[[ReportingContext, str], str]:
    def _writer(context: ReportingContext, path: str) -> str:
        return write_markdown_summary(
            path=path,
            solver_report=context.solver_report,
            kpis=context.kpis,
            model_stats=context.model_stats,
            title=title,
        )

    return _writer


# ---------------------------------------------------------------------------
# Solver + KPI computations
# ---------------------------------------------------------------------------


def _normalise_solver_report(
    solver_results: Mapping[str, Any],
    run_id: str,
    run_started_at: str,
) -> Dict[str, Any]:
    solver_section = {
        "name": solver_results.get("solver"),
        "status": solver_results.get("status"),
        "termination": solver_results.get("termination"),
        "elapsed_sec": solver_results.get("elapsed_sec"),
        "objective_value": solver_results.get("objective_value"),
        "gap": solver_results.get("gap"),
        "best_bound": solver_results.get("best_bound"),
    }

    return {
        "run": {
            "id": run_id,
            "started_at": run_started_at,
        },
        "solver": {k: v for k, v in solver_section.items() if v is not None},
        "raw": dict(solver_results),
    }

# ---------------------------------------------------------------------------
# Model MPS export
# ---------------------------------------------------------------------------


def write_model_mps(model: pyo.ConcreteModel, path: str) -> str:
    """
    Export the Pyomo model to MPS format.
    
    Args:
        model: Solved or unsolved Pyomo model
        path: Target file path (e.g., "model.mps")
    
    Returns:
        SHA256 checksum of the written file
    """
    _ensure_parent(path)

    io_options = {"symbolic_solver_labels": True}

    fmt = None
    problem_format = getattr(pyo, "ProblemFormat", None)
    if problem_format is not None and getattr(problem_format, "mps", None) is not None:
        fmt = problem_format.mps
    elif ProblemFormat is not None and getattr(ProblemFormat, "mps", None) is not None:
        fmt = ProblemFormat.mps

    try:
        if fmt is not None:
            model.write(path, format=fmt, io_options=io_options)
        else:
            model.write(path, format="mps", io_options=io_options)
    except TypeError:
        # Some Pyomo writers do not accept io_options; retry without them.
        if fmt is not None:
            model.write(path, format=fmt)
        else:
            model.write(path, format="mps")

    return sha256_file(path)

# ---------------------------------------------------------------------------
# Model statistics extraction (adapted from original module)
# ---------------------------------------------------------------------------


def extract_model_stats(model: pyo.ConcreteModel) -> Dict[str, Any]:
    """Compute counts of variables/constraints by component and type."""

    vars_by_domain: Dict[str, int] = {}
    vars_by_type: Dict[str, int] = {"Binary": 0, "Integer": 0, "Continuous": 0}
    total_vars = 0

    for var in model.component_objects(pyo.Var, active=True):
        name = var.getname()
        for idx in var:
            vars_by_domain[name] = vars_by_domain.get(name, 0) + 1
            total_vars += 1

            vardata = var[idx]
            if getattr(vardata, "is_binary", None) and vardata.is_binary():
                vars_by_type["Binary"] += 1
            elif getattr(vardata, "is_integer", None) and vardata.is_integer():
                vars_by_type["Integer"] += 1
            else:
                vars_by_type["Continuous"] += 1

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


# ---------------------------------------------------------------------------
# CSV exports
# ---------------------------------------------------------------------------


def write_variables_csv(model: pyo.ConcreteModel, path: str) -> str:
    """Export all active variables to a wide CSV."""

    header = ["var", "i", "h", "n", "index_extra", "value", "lb", "ub"]

    def _rows() -> ArtifactRows:
        for var in model.component_objects(pyo.Var, active=True):
            vname = var.getname()
            for idx in var:
                v = var[idx]
                value = pyo.value(v, exception=False)
                lb = getattr(v, "lb", None)
                ub = getattr(v, "ub", None)
                if isinstance(idx, tuple):
                    i, h, n, extra = _split_index(idx)
                else:
                    i, h, n, extra = _split_index((idx,))
                yield [vname, i, h, n, extra, value, lb, ub]

    return _write_csv(path, header, _rows())


def write_constraints_csv(model: pyo.ConcreteModel, path: str) -> str:
    """Export constraint activities to CSV."""

    header = [
        "cons",
        "i",
        "h",
        "n",
        "index_extra",
        "lower",
        "body",
        "upper",
        "activity",
        "slack_lower",
        "slack_upper",
        "dual",
    ]

    duals = None
    for suf in model.component_objects(pyo.Suffix, active=True):
        if suf.getname() == "dual":
            duals = suf
            break

    def _rows() -> ArtifactRows:
        for cons in model.component_objects(pyo.Constraint, active=True):
            cname = cons.getname()
            iterator = cons.items() if cons.is_indexed() else [(None, cons)]
            for key, c in iterator:
                lower = pyo.value(c.lower) if c.has_lb() else None
                upper = pyo.value(c.upper) if c.has_ub() else None
                body = pyo.value(c.body)
                activity = body
                sL = (activity - lower) if lower is not None else None
                sU = (upper - activity) if upper is not None else None

                dual = None
                if duals is not None:
                    try:
                        dual = duals[c]
                    except Exception:
                        dual = None

                if key is None:
                    i, h, n, extra = None, None, None, ""
                else:
                    if not isinstance(key, tuple):
                        key = (key,)
                    i, h, n, extra = _split_index(key)

                yield [cname, i, h, n, extra, lower, body, upper, activity, sL, sU, dual]

    return _write_csv(path, header, _rows())


def write_solution_csv(model: pyo.ConcreteModel, path: str, var_name: str = "x") -> str:
    """Export a primary allocation variable (default: ``x[i, h]``)."""

    header = ["item", "household", "value"]
    var = getattr(model, var_name, None)
    if var is None:
        return _write_csv(path, header, [])

    def _rows() -> ArtifactRows:
        for idx in var:
            v = var[idx]
            val = pyo.value(v, exception=False)
            if not val:
                continue
            if isinstance(idx, tuple):
                item = idx[0] if len(idx) > 0 else None
                hh = idx[1] if len(idx) > 1 else None
            else:
                item, hh = idx, None
            yield [item, hh, val]

    return _write_csv(path, header, _rows())


def write_markdown_summary(
    path: str,
    solver_report: Mapping[str, Any],
    kpis: Optional[Mapping[str, Any]] = None,
    model_stats: Optional[Mapping[str, Any]] = None,
    title: str = "FBDAM Run Report",
) -> str:
    """Create a human-readable Markdown summary file."""

    kpis = kpis or {}
    model_stats = model_stats or {}

    lines: List[str] = []
    lines.append(f"# {title}")

    run_id = solver_report.get("run", {}).get("id")
    if run_id:
        lines.append(f"\n**Run ID:** `{run_id}`\n")

    solver_section = solver_report.get("solver", {})
    lines.append("## Solver summary")
    for key in ["name", "status", "termination", "elapsed_sec", "objective_value", "gap", "best_bound"]:
        if key in solver_section:
            pretty = key.replace("_", " ")
            lines.append(f"- {pretty.title()}: {solver_section[key]}")

    if kpis:
        payload = kpis.get("kpi", kpis)
        if payload:
            lines.append("\n## KPIs")
            lines.append("| Metric | Value |")
            lines.append("|---|---|")
            for key, value in payload.items():
                lines.append(f"| {key} | {value} |")

    if model_stats:
        ms = model_stats.get("model", model_stats)
        lines.append("\n## Model stats")
        for key in ["vars_total", "cons_total"]:
            if key in ms:
                pretty = key.replace("_", " ")
                lines.append(f"- {pretty.title()}: {ms[key]}")
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


# ---------------------------------------------------------------------------
# Index utilities
# ---------------------------------------------------------------------------


def _split_index(idx: Tuple[Any, ...]) -> Tuple[Optional[Any], Optional[Any], Optional[Any], str]:
    """Normalize an index tuple into (i, h, n, extra_repr)."""

    i = idx[0] if len(idx) > 0 else None
    h = idx[1] if len(idx) > 1 else None
    n = idx[2] if len(idx) > 2 else None
    extra = ""
    if len(idx) > 3:
        extra = "(" + ", ".join(repr(x) for x in idx[3:]) + ")"
    return i, h, n, extra


__all__ = [
    "write_report",
    "build_manifest",
    "compute_kpis",
    "extract_model_stats",
    "write_variables_csv",
    "write_constraints_csv",
    "write_solution_csv",
    "write_markdown_summary",
    "write_model_mps",
]



def attach_solver_artifacts(report: dict, solver_meta: dict) -> dict:
    report.setdefault("artifacts", {})
    report["artifacts"]["highs_log"] = solver_meta["log_file"]
    report["artifacts"]["highs_solution"] = solver_meta["solution_file"]
    report["artifacts"]["model_mps"] = solver_meta["mps_file"]
    report["solver"] = {
        "name": solver_meta["solver"],
        "termination_condition": solver_meta["termination_condition"],
        "status": solver_meta["status"],
        "time": solver_meta["time"],
    }
    return report