"""Solver interface and resilience helpers for FBDAM.

This module centralises solver selection and execution while ensuring that
infeasible or otherwise unsuccessful solves are reported gracefully.  The
returned payload always contains diagnostic metadata, including a boolean
``is_feasible`` flag, so downstream components can continue producing
artifacts even when the optimizer fails to find a solution.

Typical usage::

    from fbdam.engine.solver import solve_model
    res = solve_model(model, solver_name="appsi_highs", options={"time_limit": 10})
"""

from __future__ import annotations
import inspect
import time
import warnings
import logging
from typing import Any, Dict, Iterable, Optional, Tuple

import pyomo.environ as pyo


LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Solver selection and execution
# ---------------------------------------------------------------------

def solve_model(
    model: pyo.ConcreteModel,
    solver_name: str = "appsi_highs",
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Solve the given Pyomo model with selected solver backend.

    Args:
        model: Pyomo ConcreteModel (already built).
        solver_name: "appsi_highs" (preferred) or "highs" (fallback).
        options: dict of solver options (e.g., {"time_limit": 10, "mip_rel_gap": 0.01})

    Returns:
        dict with keys: status, termination, solver, time, objective, vars
    """

    options = options or {}
    start = time.time()

    resolved_name, solver = _select_solver(solver_name, options)
    if solver is None:
        return _mock_solve(model, resolved_name, time.time() - start)

    try:
        results = _invoke_solver(solver, model)
        elapsed = time.time() - start
    except Exception as exc:  # pragma: no cover - defensive safety net
        LOGGER.error("Solver invocation failed: %s", exc, exc_info=True)
        elapsed = time.time() - start
        return _build_error_report(resolved_name, elapsed, str(exc))

    elapsed = time.time() - start

    termination_raw, status_raw = _extract_status_terms(resolved_name, results)
    status = _determine_status(termination_raw, status_raw)
    is_feasible = _check_feasibility(termination_raw, status)

    best_feasible = getattr(results, "best_feasible_objective", None)
    best_bound = getattr(results, "best_objective_bound", None)

    if hasattr(results, "solver"):
        solver_section = getattr(results, "solver")
        best_feasible = getattr(solver_section, "best_objective", best_feasible)
        best_bound = getattr(solver_section, "best_bound", best_bound)
        if best_bound is None:
            best_bound = getattr(solver_section, "best_objective_bound", None)
        if best_bound is None:
            best_bound = getattr(solver_section, "upper_bound", None)
        if best_feasible is None:
            best_feasible = getattr(solver_section, "primal_bound", None)
        gap_value = getattr(solver_section, "mip_relative_gap", None)
    else:
        gap_value = getattr(results, "gap", None)

    if not is_feasible and status == "time_limit" and best_feasible is not None:
        # A feasible incumbent is available even though the solver hit a limit.
        is_feasible = True

    if not is_feasible:
        LOGGER.warning("Solver reported infeasible outcome: termination=%s status=%s", termination_raw, status)
    else:
        LOGGER.info("Solver finished with termination=%s status=%s", termination_raw, status)

    solver_info: Dict[str, Any] = {
        "solver": resolved_name,
        "elapsed_sec": round(elapsed, 4),
        "termination": termination_raw,
        "status": status,
        "is_feasible": is_feasible,
        "error_message": None,
    }

    solver_info["best_feasible_objective"] = best_feasible
    solver_info["best_objective_bound"] = best_bound

    gap = _compute_gap(best_feasible, best_bound, gap_value)
    solver_info["gap"] = gap

    try:
        obj_val = pyo.value(model.OBJ, exception=False)
    except Exception:  # pragma: no cover - safety
        obj_val = None
    solver_info["objective_value"] = obj_val

    solver_info["variables"] = _extract_variable_values(model)

    return solver_info

# ---------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------

def _select_solver(name: str, options: Dict[str, Any]) -> Tuple[str, Optional[Any]]:
    """Resolve the solver name and instantiate an available backend."""

    normalized = name.lower().strip()
    if normalized not in {"appsi_highs", "highs"}:
        raise ValueError("Unsupported solver name. Use 'appsi_highs' or 'highs'.")

    for candidate in _solver_resolution_order(normalized):
        solver = _instantiate_solver(candidate, options)
        if solver is not None:
            return candidate, solver

    warnings.warn(
        "No compatible solver found (tried appsi_highs/highs); falling back to mock solution.",
        RuntimeWarning,
        stacklevel=2,
    )
    return "mock", None


def _solver_resolution_order(requested: str) -> Iterable[str]:
    if requested == "appsi_highs":
        return ("appsi_highs", "highs")
    return ("highs",)


def _instantiate_solver(name: str, options: Dict[str, Any]) -> Optional[Any]:
    if name == "appsi_highs":
        try:
            from pyomo.contrib.appsi.solvers.highs import Highs

            solver = Highs()
            if not _is_solver_available(solver):
                return None
            _apply_options(solver, options)
            return solver
        except ImportError:
            return None

    if name == "highs":
        solver = pyo.SolverFactory("highs")
        if solver is None or not solver.available(exception_flag=False):
            return None
        _apply_options(solver, options)
        return solver

    return None


def _is_solver_available(solver: Any) -> bool:
    try:
        available = solver.available()
    except TypeError:
        available = solver.available
    return bool(available)


def _apply_options(solver, options: Dict[str, Any]) -> None:
    """Apply solver options (safe for both Appsi and classic interfaces)."""
    if solver is None:
        return
    for key, val in options.items():
        applied = False

        if hasattr(solver, "options"):
            try:
                solver.options[key] = val
                applied = True
            except Exception:
                pass

        if not applied and hasattr(solver, "set_option"):
            try:
                solver.set_option(key, val)
                applied = True
            except Exception:
                pass

        if not applied and hasattr(solver, "highs_options"):
            try:
                solver.highs_options[key] = val
                applied = True
            except Exception:
                pass

        if not applied:
            print(f"[solver] Warning: option '{key}' not supported.")


def _invoke_solver(solver, model: pyo.ConcreteModel):
    """Call ``solve`` with signature-aware kwargs to avoid TypeErrors."""
    solve_fn = solver.solve
    params = inspect.signature(solve_fn).parameters
    if "tee" in params:
        return solve_fn(model, tee=False)
    return solve_fn(model)


def _mock_solve(model: pyo.ConcreteModel, solver_name: str, elapsed: float) -> Dict[str, Any]:
    """Populate a feasible zero solution when no external solver is available."""
    for var in model.component_objects(pyo.Var, active=True):
        for idx in var:
            var[idx].set_value(0.0)

    solver_info = {
        "solver": solver_name,
        "elapsed_sec": round(elapsed, 4),
        "termination": "not attempted",
        "status": "mock",
        "is_feasible": True,
        "error_message": None,
    }

    try:
        solver_info["objective_value"] = pyo.value(model.OBJ, exception=False)
    except Exception:  # pragma: no cover - defensive
        solver_info["objective_value"] = None

    solver_info["variables"] = _extract_variable_values(model)
    solver_info["gap"] = None
    solver_info["best_feasible_objective"] = solver_info["objective_value"]
    solver_info["best_objective_bound"] = solver_info["objective_value"]
    return solver_info


def _extract_variable_values(model: pyo.ConcreteModel) -> Dict[str, Optional[float]]:
    """Return a flat mapping of variable names → values.

    Uninitialised variables yield ``None`` so that callers can inspect partial
    solver states without raising exceptions.
    """

    values: Dict[str, Optional[float]] = {}
    for var in model.component_objects(pyo.Var, active=True):
        name = var.getname()
        for idx in var:
            # ``pyo.value`` raises when a variable is uninitialized.  That can
            # happen if the solver terminates early or if a variable is fixed
            # by constraints rather than explicitly assigned a value.  Using
            # ``exception=False`` gives us ``None`` instead of bubbling up an
            # error so callers can still inspect the solution dictionary.
            values[f"{name}[{idx}]"] = pyo.value(var[idx], exception=False)
    return values


# ---------------------------------------------------------------------
# Utility: quick print summary
# ---------------------------------------------------------------------

def print_solver_summary(results: Dict[str, Any]) -> None:
    """Pretty-print minimal solver info."""
    print("\n=== Solver Summary ===")
    print(f"Solver:        {results.get('solver')}")
    print(f"Termination:   {results.get('termination')}")
    print(f"Time (s):      {results.get('elapsed_sec')}")
    print(f"Objective val: {results.get('objective_value')}")
    print("======================\n")


def _extract_status_terms(resolved_name: str, results: Any) -> Tuple[str, Optional[str]]:
    """Extract termination and raw status strings from solver results."""

    termination = "unknown"
    status: Optional[str] = None

    if resolved_name == "appsi_highs" and hasattr(results, "termination_condition"):
        termination = str(results.termination_condition)
        raw_status = getattr(results, "status", None)
        status = str(raw_status) if raw_status is not None else None
    elif hasattr(results, "solver"):
        solver_section = getattr(results, "solver")
        if hasattr(solver_section, "termination_condition"):
            termination = str(solver_section.termination_condition)
        if hasattr(solver_section, "status"):
            status = str(solver_section.status)
    elif hasattr(results, "termination_condition"):
        termination = str(results.termination_condition)

    return termination, status


def _determine_status(termination: str, raw_status: Optional[str]) -> str:
    """Normalise solver status into a short, user-friendly token.

    Args:
        termination: Termination condition string from the solver.
        raw_status: Optional raw status string reported by the solver backend.

    Returns:
        Canonical status string such as ``"ok"`` or ``"infeasible"``.
    """

    for candidate in (raw_status, termination):
        if not candidate:
            continue
        lowered = candidate.lower()
        if "optimal" in lowered:
            return "ok"
        if "infeasible" in lowered:
            return "infeasible"
        if "unbounded" in lowered:
            return "unbounded"
        if "limit" in lowered or "timeout" in lowered:
            return "time_limit"

    if raw_status:
        return raw_status.lower()
    if termination:
        return termination.lower()
    return "unknown"


def _check_feasibility(termination: str, status: str) -> bool:
    """Determine whether the solve is considered feasible.

    Args:
        termination: Termination condition string (lower-cased).
        status: Normalised status string from :func:`_determine_status`.

    Returns:
        ``True`` when the solver produced a feasible solution, ``False``
        otherwise.  The check errs on the side of caution and defaults to
        ``False`` when unsure.
    """

    termination = termination or ""
    status = status or ""
    tokens = f"{termination} {status}".lower()

    if "infeasible" in tokens or "unbounded" in tokens:
        return False
    if "optimal" in tokens or status == "ok":
        return True
    if "feasible" in termination and "infeasible" not in termination:
        return True
    return False


def _build_error_report(solver_name: str, elapsed: float, message: str) -> Dict[str, Any]:
    """Construct a consistent error payload when solver execution fails."""

    LOGGER.error("Building solver error report for %s: %s", solver_name, message)
    return {
        "solver": solver_name,
        "elapsed_sec": round(elapsed, 4),
        "termination": "error",
        "status": "error",
        "is_feasible": False,
        "objective_value": None,
        "best_feasible_objective": None,
        "best_objective_bound": None,
        "gap": None,
        "variables": {},
        "error_message": message,
    }


def _compute_gap(best_feasible: Optional[float], best_bound: Optional[float], gap_value: Optional[float]) -> Optional[float]:
    """Compute a relative optimality gap when the backend does not provide one."""

    if gap_value is not None:
        try:
            return round(float(gap_value), 6)
        except (TypeError, ValueError):  # pragma: no cover - defensive
            return None

    if best_feasible is None or best_bound is None:
        return None

    try:
        if best_feasible == 0:
            return None
        gap = abs(best_feasible - best_bound) / abs(best_feasible)
        return round(float(gap), 6)
    except Exception:  # pragma: no cover - defensive
        return None

# ---------------------------------------------------------------------
# Utility: quick print summary
# ---------------------------------------------------------------------

from pathlib import Path
from datetime import datetime
from pyomo.opt import SolverFactory

def solve_with_highs(m, run_id: str, base_outputs: Path) -> dict:
    """
    Resuelve con HiGHS (APPSI si está disponible) y guarda logs/artefactos.
    Devuelve metadatos útiles para reporting.
    """
    run_id = str(run_id)
    logs_dir = Path(base_outputs) / "logs"
    sols_dir = Path(base_outputs) / "solutions"
    models_dir = Path(base_outputs) / "models"
    for d in (logs_dir, sols_dir, models_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / f"highs-{run_id}.log"
    sol_file = sols_dir / f"highs-solution-{run_id}.txt"
    mps_file = models_dir / f"model-{run_id}.mps"

    # (Opcional) escribe el MPS exacto que vas a resolver
    m.write(filename=str(mps_file), io_options={"symbolic_solver_labels": True})

    # Preferir APPSI
    solver_name = None
    if SolverFactory('appsi_highs').available():
        solver_name = 'appsi_highs'
        solver = SolverFactory('appsi_highs')
        # Tiempo límite, threads, etc. via config (APPSI) si quieres:
        # solver.config.time_limit = 300
        # Pasa opciones nativas de HiGHS:
        solver.highs_options = {
            "output_flag": True,
            "log_to_console": False,
            "log_file": str(log_file),
            "write_solution_to_file": True,
            "write_solution_style": 1,   # 1 = pretty, ver doc
            "solution_file": str(sol_file),  # APPSI las respeta vía highs_options
        }
        res = solver.solve(m)
    else:
        # Fallback al wrapper clásico
        solver_name = 'highs'
        solver = SolverFactory('highs')
        # Ojo: en el wrapper clásico, las opciones van en 'options='
        # y se pasan directas a HiGHS.
        res = solver.solve(
            m,
            tee=False,  # el tee puede no funcionar con highspy
            options={
                "output_flag": "true",
                "log_to_console": "false",
                "log_file": str(log_file),
                "write_solution_to_file": "true",
                "write_solution_style": "1",
                "solution_file": str(sol_file),
            }
        )

    # Metadatos mínimos para tu reporter
    meta = {
        "solver": solver_name,
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "log_file": str(log_file),
        "solution_file": str(sol_file),
        "mps_file": str(mps_file),
        # Campos típicos de interés si los expone 'res'
        "termination_condition": getattr(getattr(res, "solver", None), "termination_condition", None),
        "time": getattr(getattr(res, "solver", None), "time", None),
    }
    return meta
