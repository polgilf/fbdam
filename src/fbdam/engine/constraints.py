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
from collections.abc import Mapping
from typing import Any, Callable, Dict
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
# Helpers for dial resolution and slack handling
# ---------------------------------------------------------------------

def _get_model_params(m: pyo.ConcreteModel) -> Dict[str, Any]:
    return getattr(m, "model_params", {}) or {}


def _get_lambda_value(model_params: Mapping[str, Any]) -> float | None:
    for key in ("lambda", "lambda_", "lam"):
        if key in model_params:
            value = model_params[key]
            return float(value)
    return None


def _coerce_mapping(value: Any) -> Mapping[Any, Any] | None:
    if isinstance(value, Mapping):
        return value
    return None


def _resolve_indexed_value(
    source: Any,
    index: Any,
    *,
    default: float | None = None,
) -> float:
    mapping = _coerce_mapping(source)
    if mapping is None:
        if source is None:
            if default is not None:
                return float(default)
            raise ValueError("No value provided for dial.")
        return float(source)

    if isinstance(index, tuple) and len(index) == 2:
        first, second = index
        if first in mapping:
            nested = mapping[first]
            if isinstance(nested, Mapping):
                if second in nested:
                    return float(nested[second])
                for key in ("default", "__default__"):
                    if key in nested:
                        return float(nested[key])
            else:
                return float(nested)

    if index in mapping:
        return float(mapping[index])

    for key in ("default", "__default__"):
        if key in mapping:
            return float(mapping[key])

    if default is not None:
        return float(default)

    raise KeyError(f"Dial mapping missing value for index {index!r}.")


def _get_dial_value(
    m: pyo.ConcreteModel,
    params: Mapping[str, Any],
    name: str,
    index: Any | None = None,
    *,
    default: float | None = None,
) -> float:
    source = params.get(name) if isinstance(params, Mapping) else None
    if source is None:
        model_params = _get_model_params(m)
        dials = model_params.get("dials", {})
        if isinstance(dials, Mapping):
            source = dials.get(name)
    if index is None:
        if isinstance(source, Mapping):
            # Without an index, prefer an explicit default entry.
            for key in ("default", "__default__"):
                if key in source:
                    return float(source[key])
        if source is None:
            if default is not None:
                return float(default)
            raise ValueError(f"Dial '{name}' not provided.")
        return float(source)
    return _resolve_indexed_value(source, index, default=default)


def _should_use_slack(m: pyo.ConcreteModel, params: Mapping[str, Any]) -> bool:
    flag = params.get("use_slack") if isinstance(params, Mapping) else None
    if isinstance(flag, str):
        text = flag.strip().lower()
        if text in {"auto", "default"}:
            flag = None
        else:
            flag = text in {"true", "1", "yes", "y"}
    if flag is not None:
        return bool(flag)
    lam_value = _get_lambda_value(_get_model_params(m))
    return lam_value is not None and lam_value > 0


def _slack_term(m: pyo.ConcreteModel, params: Mapping[str, Any]) -> pyo.Expression | float:
    return m.epsilon if _should_use_slack(m, params) else 0.0


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


@register_constraint("stock_balance")
def add_stock_balance(m: pyo.ConcreteModel, params: dict) -> None:
    """Ensure allocations of each item do not exceed available supply."""

    def rule(model, i):
        return sum(model.x[i, h] for h in model.H) <= model.Avail[i]

    m.StockBalance = pyo.Constraint(m.I, rule=rule)


@register_constraint("purchase_budget")
def add_purchase_budget(m: pyo.ConcreteModel, params: dict) -> None:
    """Limit total purchases by the available monetary budget."""

    budget = params.get("budget") if isinstance(params, Mapping) else None
    if budget is None:
        budget = _get_model_params(m).get("budget")
    if budget is None:
        raise ValueError("purchase_budget constraint requires a 'budget' value.")

    budget_value = float(budget)

    def rule(model):
        return sum(model.cost[i] * model.y[i] for i in model.I) <= budget_value

    m.PurchaseBudget = pyo.Constraint(rule=rule)


@register_constraint("household_floor")
def add_household_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """
    household_floor — Household minimum utility
    -------------------------------------------
    Implements  \bar u_h - omega_h * \bar u_all >= -epsilon.

    Params (dict):
        omega: Optional scalar or mapping per household. Defaults to the
               scenario dial if defined, otherwise 0.0.
        use_slack: bool | "auto" — whether to include epsilon on the RHS.
    """
    slack = _slack_term(m, params)

    def rule(model, h):
        omega = _get_dial_value(model, params, "omega", h, default=0.0)
        return model.mean_utility[h] - omega * model.global_mean_utility >= -slack

    m.HouseholdFloor = pyo.Constraint(m.H, rule=rule)


@register_constraint("nutrient_floor")
def add_nutrient_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """Implements  \bar u_n - gamma_n * \bar u_all >= -epsilon."""

    slack = _slack_term(m, params)

    def rule(model, n):
        gamma = _get_dial_value(model, params, "gamma", n, default=0.0)
        return model.mean_utility_nutrient[n] - gamma * model.global_mean_utility >= -slack

    m.NutrientFloor = pyo.Constraint(m.N, rule=rule)


@register_constraint("pair_floor")
def add_pair_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """Implements  u[n,h] - kappa_{n,h} * \bar u_all >= -epsilon."""

    slack = _slack_term(m, params)

    def rule(model, n, h):
        kappa = _get_dial_value(model, params, "kappa", (n, h), default=0.0)
        return model.u[n, h] - kappa * model.global_mean_utility >= -slack

    m.PairFloor = pyo.Constraint(m.N, m.H, rule=rule)


@register_constraint("fairshare_cap_house")
def add_fairshare_cap_house(m: pyo.ConcreteModel, params: dict) -> None:
    """
    fairshare_cap_house — Fairness cap by household
    -----------------------------------------------
    Limits deviations from proportional allocation (L1-based fairness).

    Σ_i |x[i,h] - α·w[h]| ≤ β·w[h]·Σ_i S[i]

    Params (dict):
        alpha: float — proportional share coefficient (0–1)
    """
    alpha = _get_dial_value(m, params, "alpha", default=0.7)

    def rule(model, h):
        return sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I) <= alpha * model.fairshare_weight[h] * model.TotSupply

    m.FairCapHouse = pyo.Constraint(m.H, rule=rule)


@register_constraint("deviation_identity")
def add_deviation_identity(m: pyo.ConcreteModel, params: dict) -> None:
    """Linearize absolute deviation around proportional share."""

    def rule(model, i, h):
        fair_target = model.fairshare_weight[h] * model.Avail[i]
        return model.x[i, h] - fair_target == model.dpos[i, h] - model.dneg[i, h]

    m.DeviationIdentity = pyo.Constraint(m.I, m.H, rule=rule)


@register_constraint("deviation_item_cap")
def add_deviation_item_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """Aggregate per-item L1 deviation cap with dial alpha."""

    def rule(model, i):
        alpha = _get_dial_value(model, params, "alpha", i)
        return sum(model.dpos[i, h] + model.dneg[i, h] for h in model.H) <= alpha * model.Avail[i]

    m.DeviationItemCap = pyo.Constraint(m.I, rule=rule)


@register_constraint("deviation_household_cap")
def add_deviation_household_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """Aggregate per-household L1 deviation cap with dial beta."""

    def rule(model, h):
        beta = _get_dial_value(model, params, "beta", h)
        return sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I) <= beta * model.TotSupply

    m.DeviationHouseholdCap = pyo.Constraint(m.H, rule=rule)


@register_constraint("deviation_pair_cap")
def add_deviation_pair_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """Per (item, household) deviation cap with dial rho."""

    def rule(model, i, h):
        rho = _get_dial_value(model, params, "rho", (i, h))
        return model.dpos[i, h] + model.dneg[i, h] <= rho * model.Avail[i]

    m.DeviationPairCap = pyo.Constraint(m.I, m.H, rule=rule)


# ---------------------------------------------------------------------
# Utility: list registered constraints
# ---------------------------------------------------------------------

def list_constraints() -> None:
    """Print a summary of all registered constraints."""
    print("Registered constraints:")
    for name in sorted(CONSTRAINTS_REGISTRY):
        print(f"  - {name}")
