"""
constraints.py — Constraint registry and definitions
----------------------------------------------------
Provides a plugin-style registry for reusable constraint blocks
used in FBDAM optimization models.

Design principles:
- Each constraint is a callable: (model, params) -> None
- They are registered dynamically via the @register_constraint decorator.
- This allows catalogs (YAML) to activate them by name (e.g., "u_link").

Example:
    @register_constraint("u_link")
    def add_u_link(m, params):
        def rule(m, n, h):
            return m.u[n, h] <= m.q[n, h] / m.R[h, n]
        m.U_link = pyo.Constraint(m.N, m.H, rule=rule)

The model builder (model.py) will iterate through constraints declared
in the validated configuration and invoke each registered handler.
"""

from __future__ import annotations
from typing import Callable, Dict
import pyomo.environ as pyo


# ---------------------------------------------------------------------
# Registry infrastructure
# ---------------------------------------------------------------------

# Type alias for constraint-building functions
ConstraintFn = Callable[[pyo.ConcreteModel, dict], None]

# Global registry (name → function)
CONSTRAINTS_REGISTRY: Dict[str, ConstraintFn] = {}


def register_constraint(name: str) -> Callable[[ConstraintFn], ConstraintFn]:
    """
    Decorator to register a new constraint handler.

    Args:
        name: Symbolic name used in the YAML catalog and configuration.
    Returns:
        The original function (after registering it in the global dict).
    """
    def decorator(fn: ConstraintFn) -> ConstraintFn:
        if name in CONSTRAINTS_REGISTRY:
            raise ValueError(f"Constraint '{name}' is already registered.")
        CONSTRAINTS_REGISTRY[name] = fn
        return fn

    return decorator


def get_constraint(name: str) -> ConstraintFn:
    """
    Retrieve a registered constraint handler by name.
    Raises KeyError if not found.
    """
    try:
        return CONSTRAINTS_REGISTRY[name]
    except KeyError as e:
        raise KeyError(f"Constraint '{name}' not found in registry.") from e


# ---------------------------------------------------------------------
# Example constraint implementations
# ---------------------------------------------------------------------

@register_constraint("u_link")
def add_u_link(m: pyo.ConcreteModel, params: dict) -> None:
    """
    u_link — Utility linkage constraint
    -----------------------------------
    Links household-nutrient utility with delivered quantity and requirement.

    Mathematical form:
        u[n,h] <= q[n,h] / R[h,n]     ∀ n ∈ N, h ∈ H

    Params (dict):
        none
    """
    def rule(m, n, h):
        return m.u[n, h] <= m.q[n, h] / m.R[h, n]

    m.U_link = pyo.Constraint(m.N, m.H, rule=rule)


@register_constraint("household_floor")
def add_household_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """
    household_floor — Household minimum utility
    -------------------------------------------
    Ensures each household reaches a minimum average utility level.

    ū_h >= U_floor × ū
    where ū = overall mean utility

    Params (dict):
        U_floor: float (e.g., 0.8) — fraction of global average to guarantee
    """
    U_floor = float(params.get("U_floor", 0.8))

    # The builder must define m.mean_utility somewhere (e.g., via expression)
    def rule(m, h):
        return m.mean_utility[h] >= U_floor * m.global_mean_utility

    m.HHFloor = pyo.Constraint(m.H, rule=rule)


@register_constraint("fairshare_cap_house")
def add_fairshare_cap_house(m: pyo.ConcreteModel, params: dict) -> None:
    """
    fairshare_cap_house — Fairness cap by household
    -----------------------------------------------
    Limits deviations from proportional allocation (L1-based fairness).

    Σ_i |x[i,h] - α·γ[h]| ≤ β·γ[h]·Σ_i S[i]

    Params (dict):
        alpha: float — proportional share coefficient (0–1)
    """
    alpha = float(params.get("alpha", 0.7))

    def rule(m, h):
        return sum(m.dpos[i, h] + m.dneg[i, h] for i in m.I) <= alpha * m.gamma[h] * sum(
            m.S[i] for i in m.I
        )

    m.FairCapHouse = pyo.Constraint(m.H, rule=rule)


# ---------------------------------------------------------------------
# Utility: list registered constraints
# ---------------------------------------------------------------------

def list_constraints() -> None:
    """Print a summary of all registered constraints."""
    print("Registered constraints:")
    for name in sorted(CONSTRAINTS_REGISTRY):
        print(f"  - {name}")
