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
import time
import inspect
from typing import Any, Dict, Optional, Tuple
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

    solver, active_solver_name = _get_solver(solver_name, options)
    if solver is None:
        return _mock_solve(model, active_solver_name, time.time() - start)

    results = _invoke_solver(solver, model)
    elapsed = time.time() - start

    # Extract solution info
    solver_info = {
        "solver": active_solver_name,
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

def _get_solver(name: str, options: Dict[str, Any]) -> Tuple[Optional[Any], str]:
    """Return an appropriate Pyomo solver instance and the resolved solver name."""
    name = name.lower().strip()

    # Attempt preferred appsi_highs interface
    if name == "appsi_highs":
        try:
            from pyomo.contrib.appsi.solvers.highs import Highs
            solver = Highs()
            try:
                is_available = bool(solver.available())
            except TypeError:
                # Older Pyomo versions expose ``available`` as a property
                is_available = bool(solver.available)
            if not is_available:
                print("[solver] appsi_highs not available, falling back to highs CLI")
                return _fallback_highs(options)
            _apply_options(solver, options)
            return solver, "appsi_highs"
        except ImportError:
            print("[solver] appsi_highs unavailable, falling back to highs CLI")
            return _fallback_highs(options)

    # Classic CLI interface
    if name == "highs":
        return _fallback_highs(options)

    raise ValueError(f"Unsupported solver name '{name}'. Use 'appsi_highs' or 'highs'.")


def _fallback_highs(options: Dict[str, Any]) -> Tuple[Optional[Any], str]:
    """Fallback: use the traditional HiGHS executable interface, if available."""
    solver = pyo.SolverFactory("highs")
    if solver is None or not solver.available(exception_flag=False):
        print("[solver] highs CLI not available; using mock solver")
        return None, "mock"
    _apply_options(solver, options)
    return solver, "highs"


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
