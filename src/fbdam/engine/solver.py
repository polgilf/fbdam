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
from typing import Any, Dict, Optional
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

    solver = _get_solver(solver_name, options)
    results = solver.solve(model, tee=False)
    elapsed = time.time() - start

    # Extract solution info
    solver_info = {
        "solver": solver_name,
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

def _get_solver(name: str, options: Dict[str, Any]):
    """Return an appropriate Pyomo solver instance."""
    name = name.lower().strip()

    # Attempt preferred appsi_highs interface
    if name == "appsi_highs":
        try:
            from pyomo.contrib.appsi.solvers.highs import Highs
            solver = Highs()
            _apply_options(solver, options)
            return solver
        except ImportError:
            print("[solver] appsi_highs unavailable, falling back to highs CLI")
            return _fallback_highs(options)

    # Classic CLI interface
    if name == "highs":
        return _fallback_highs(options)

    raise ValueError(f"Unsupported solver name '{name}'. Use 'appsi_highs' or 'highs'.")


def _fallback_highs(options: Dict[str, Any]):
    """Fallback: use the traditional HiGHS executable interface."""
    solver = pyo.SolverFactory("highs")
    _apply_options(solver, options)
    return solver


def _apply_options(solver, options: Dict[str, Any]) -> None:
    """Apply solver options (safe for both Appsi and classic interfaces)."""
    for key, val in options.items():
        try:
            solver.options[key] = val
        except Exception:
            # Some interfaces use different option mechanisms
            if hasattr(solver, "set_option"):
                solver.set_option(key, val)
            else:
                print(f"[solver] Warning: option '{key}' not supported.")


def _extract_variable_values(model: pyo.ConcreteModel) -> Dict[str, float]:
    """Return a flat mapping of variable names → values."""
    values: Dict[str, float] = {}
    for var in model.component_objects(pyo.Var, active=True):
        name = var.getname()
        for idx in var:
            values[f"{name}[{idx}]"] = pyo.value(var[idx])
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
