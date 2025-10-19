"""
solver.py — Solver interface
----------------------------
Handles solver creation, configuration, and execution for FBDAM models.

Design:
- Preferred backend: appsi_highs (fast, modern Pyomo interface)
- Fallback backend: classic highs (via executable in PATH)
- Captures solver metadata (status, termination, runtime, etc.)
- Returns a structured result dictionary for reporting.

Typical usage:
    from fbdam.engine.solver import solve_model
    res = solve_model(model, solver_name="appsi_highs", options={"time_limit": 10})
"""

from __future__ import annotations
import inspect
import time
from typing import Any, Dict, Iterable, Optional, Tuple

import pyomo.environ as pyo


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

    results = _invoke_solver(solver, model)
    elapsed = time.time() - start

    # Extract solution info
    solver_info = {
        "solver": resolved_name,
        "elapsed_sec": round(elapsed, 4),
        "termination": str(results.solver.termination_condition)
        if hasattr(results, "solver") else "unknown",
        "status": str(results.solver.status) if hasattr(results, "solver") else "unknown",
    }

    # Compute objective value if available
    try:
        obj_val = pyo.value(model.OBJ)
    except Exception:
        obj_val = None
    solver_info["objective_value"] = obj_val

    # Variable dump (flat dict)
    var_values = _extract_variable_values(model)
    solver_info["variables"] = var_values

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
        "status": "mock-solution",
    }

    try:
        solver_info["objective_value"] = pyo.value(model.OBJ)
    except Exception:
        solver_info["objective_value"] = None

    solver_info["variables"] = _extract_variable_values(model)
    solver_info["gap"] = None
    solver_info["best_bound"] = None
    return solver_info


def _extract_variable_values(model: pyo.ConcreteModel) -> Dict[str, float]:
    """Return a flat mapping of variable names → values."""
    values: Dict[str, float] = {}
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
    print(f"Status:        {results.get('status')}")
    print(f"Termination:   {results.get('termination')}")
    print(f"Time (s):      {results.get('elapsed_sec')}")
    print(f"Objective val: {results.get('objective_value')}")
    print("======================\n")

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
        "status": getattr(getattr(res, "solver", None), "status", None),
        "time": getattr(getattr(res, "solver", None), "time", None),
    }
    return meta
