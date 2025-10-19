"""
objectives.py — Objective registry and definitions
--------------------------------------------------
Plugin-style registry for model objectives in FBDAM.

Design:
- Each objective handler is a callable: (model, params, sense) -> None
- Handlers are registered via @register_objective("name")
- The builder (model.py) looks up the handler by 'name' from YAML config.

Example YAML:
  objectives:
    - id: sum_utility
      name: sum_utility
      sense: maximize
      params: {}

Example builder usage:
  from fbdam.engine.objectives import get_objective
  handler = get_objective(obj.name)
  handler(model, params=obj.params, sense=obj.sense)
"""

from __future__ import annotations
from collections.abc import Mapping
from typing import Callable, Dict, Optional
import pyomo.environ as pyo

# ---------------------------------------------------------------------
# Registry infrastructure
# ---------------------------------------------------------------------

ObjectiveFn = Callable[[pyo.ConcreteModel, dict, Optional[str]], None]
OBJECTIVES_REGISTRY: Dict[str, ObjectiveFn] = {}


def register_objective(name: str) -> Callable[[ObjectiveFn], ObjectiveFn]:
    """
    Decorator to register an objective handler.

    Args:
        name: Symbolic name used in YAML catalogs/config.
    Returns:
        The original function after registration.
    """
    def decorator(fn: ObjectiveFn) -> ObjectiveFn:
        if name in OBJECTIVES_REGISTRY:
            raise ValueError(f"Objective '{name}' is already registered.")
        OBJECTIVES_REGISTRY[name] = fn
        return fn
    return decorator


def get_objective(name: str) -> ObjectiveFn:
    """Retrieve a registered objective handler by name."""
    try:
        return OBJECTIVES_REGISTRY[name]
    except KeyError as e:
        raise KeyError(f"Objective '{name}' not found in registry.") from e


def _sense_to_pyomo(sense: Optional[str]) -> object:
    """
    Map a string sense to Pyomo's maximize/minimize.
    Defaults to maximize if not provided.
    """
    if sense is None:
        return pyo.maximize
    s = sense.lower().strip()
    if s == "maximize":
        return pyo.maximize
    if s == "minimize":
        return pyo.minimize
    raise ValueError(f"Invalid sense '{sense}'. Use 'maximize' or 'minimize'.")


def _get_lambda_value(model_params: Mapping[str, object] | None) -> float | None:
    params = model_params or {}
    for key in ("lambda", "lambda_", "lam"):
        if key in params:
            return float(params[key])
    return None


# ---------------------------------------------------------------------
# Objective implementations
# ---------------------------------------------------------------------

@register_objective("sum_utility")
def obj_sum_utility(m: pyo.ConcreteModel, params: dict, sense: Optional[str] = "maximize") -> None:
    """
    sum_utility — Total utility across nutrients and households
    -----------------------------------------------------------
    Creates an objective that maximizes (or minimizes) the sum of u[n,h].

    Mathematical form (default):
        Maximize  Σ_{n∈N} Σ_{h∈H} u[n,h]

    Params (dict):
        weight: optional float multiplier for this objective (default: 1.0)

    Notes:
        - Assumes m.u is defined over (N, H).
    """
    weight = float(params.get("weight", 1.0))
    pyomo_sense = _sense_to_pyomo(sense)

    if hasattr(m, "total_utility"):
        utility_expr = m.total_utility
    else:
        utility_expr = sum(m.u[n, h] for n in m.N for h in m.H)

    expr = weight * utility_expr

    lambda_value = _get_lambda_value(getattr(m, "model_params", None))
    if lambda_value and hasattr(m, "epsilon"):
        expr = expr - lambda_value * m.epsilon

    # Use a stable component name (overwrite if re-called by design).
    m.OBJ = pyo.Objective(expr=expr, sense=pyomo_sense)


# ---------------------------------------------------------------------
# Utility: list registered objectives
# ---------------------------------------------------------------------

def list_objectives() -> None:
    """Print a summary of all registered objectives."""
    print("Registered objectives:")
    for name in sorted(OBJECTIVES_REGISTRY):
        print(f"  - {name}")
