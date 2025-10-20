"""
constraints.py — Constraint registry and definitions
----------------------------------------------------
Provides a plugin-style registry for reusable constraint blocks
used in FBDAM optimization models.

Design principles:
- Each constraint is a callable: (model, params) -> None
- They are registered dynamically via the @register_constraint decorator.
- This allows catalogs (YAML) to activate them by name (e.g., "nutrition_utility_mapping").

Example:
    @register_constraint("nutrition_utility_mapping")
    def add_nutrition_utility_mapping(m, params):
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

# ═══════════════════════════════════════════════════════════════════
# Dial resolution — Simplified and explicit
# ═══════════════════════════════════════════════════════════════════

def _get_dial_value(
    model: pyo.ConcreteModel,
    params: Mapping[str, Any],
    name: str,
    index: Any | None = None,
    default: float | None = 0.0,
) -> float:
    """
    Resolve dial value with clear priority:
    1. Constraint-level params[name]
    2. Model-level model.model_params['dials'][name]
    3. Provided default

    Supports scalar dials and indexed mappings (including tuple indices)
    through the ``index`` argument.
    
    Raises ValueError if not found and no default.
    """
    # Priority 1: constraint params
    if name in params:
        return _materialise_dial_value(params[name], index, default)
    
    # Priority 2: model dials
    model_params = getattr(model, "model_params", {})
    if isinstance(model_params, Mapping):
        dials = model_params.get("dials", {})
        if isinstance(dials, Mapping) and name in dials:
            return _materialise_dial_value(dials[name], index, default)

    # Priority 3: default
    if default is not None:
        return float(default)
    
    raise ValueError(f"Dial '{name}' not found in params or model.model_params.dials")


def _materialise_dial_value(source: Any, index: Any | None, default: float | None) -> float:
    if isinstance(source, Mapping):
        if index is None:
            for key in ("default", "__default__"):
                if key in source:
                    return float(source[key])
            raise KeyError("Mapping dial requires an index or default entry.")
        return _lookup_indexed_mapping(source, index, default)

    if source is None:
        raise KeyError("Dial source is None")

    return float(source)


def _lookup_indexed_mapping(mapping: Mapping[Any, Any], index: Any, default: float | None) -> float:
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

@register_constraint("nutrition_utility_mapping")
def add_u_link(m: pyo.ConcreteModel, params: dict) -> None:
    """
    nutrition_utility_mapping — Utility linkage constraint
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


@register_constraint("item_supply_limit")
def add_stock_balance(m: pyo.ConcreteModel, params: dict) -> None:
    """Ensure allocations of each item do not exceed available supply."""

    def rule(model, i):
        return sum(model.x[i, h] for h in model.H) <= model.Avail[i]

    m.StockBalance = pyo.Constraint(m.I, rule=rule)


@register_constraint("purchase_budget_limit")
def add_purchase_budget(m: pyo.ConcreteModel, params: dict) -> None:
    """Limit total purchases by the available monetary budget.

    This constraint creates three sub-constraints:
    1. **Budget limit** – total purchase cost cannot exceed the budget.
    2. **Purchase activation** – links the continuous purchase quantity ``y[i]``
       to the binary activation variable ``y_active[i]`` via a classic big-M
       formulation.
    3. **No waste** – if purchasing is activated, all available units (donated
       stock plus purchases) must be allocated; otherwise up to the donated
       stock may remain unused.

    The "no waste" requirement prevents wasting scarce budget resources on
    items that are not ultimately distributed.
    """

    budget = params.get("budget") if isinstance(params, Mapping) else None
    if budget is None:
        budget = _get_model_params(m).get("budget")
    if budget is None:
        raise ValueError("purchase_budget constraint requires a 'budget' value.")

    budget_value = float(budget)

    def _budget_rule(model):
        return sum(model.cost[i] * model.y[i] for i in model.I) <= budget_value

    m.PurchaseBudget = pyo.Constraint(rule=_budget_rule)

    # Small epsilon used to avoid division-by-zero when computing the activation big-M.
    EPS_COST = 1e-9

    def _max_purchase_for_item(model, item_id: str) -> float:
        unit_cost = float(model.cost[item_id])
        if budget_value <= 0:
            return 0.0
        denom = unit_cost if unit_cost > EPS_COST else EPS_COST
        return budget_value / denom

    def _purchase_activation_rule(model, item_id: str):
        big_m = _max_purchase_for_item(model, item_id)
        return model.y[item_id] <= big_m * model.y_active[item_id]

    m.PurchaseActivation = pyo.Constraint(m.I, rule=_purchase_activation_rule)

    # 3. NO WASTE when purchasing
    # If purchases are activated (y_active = 1), force full allocation of
    # Avail[i] = S[i] + y[i]. If no purchases (y_active = 0), allow up to
    # S[i] units of donated stock to remain unallocated.
    def _no_waste_rule(model, item_id: str):
        unallocated = model.Avail[item_id] - sum(model.x[item_id, h] for h in model.H)
        max_waste_without_purchase = model.S[item_id]
        return unallocated <= max_waste_without_purchase * (1 - model.y_active[item_id])

    m.PurchaseNoWaste = pyo.Constraint(m.I, rule=_no_waste_rule)


@register_constraint("household_adequacy_floor")
def add_household_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """
    household_adequacy_floor — Household minimum utility
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
        return model.household_mean_utility[h] - omega * model.global_mean_utility >= -slack

    m.HouseholdFloor = pyo.Constraint(m.H, rule=rule)


@register_constraint("nutrient_adequacy_floor")
def add_nutrient_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """nutrient_adequacy_floor — Implements \bar u_n - gamma_n * \bar u_all >= -epsilon."""

    slack = _slack_term(m, params)

    def rule(model, n):
        gamma = _get_dial_value(model, params, "gamma", n, default=0.0)
        return model.nutrient_mean_utility[n] - gamma * model.global_mean_utility >= -slack

    m.NutrientFloor = pyo.Constraint(m.N, rule=rule)


@register_constraint("pairwise_adequacy_floor")
def add_pair_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """pairwise_adequacy_floor — Implements u[n,h] - kappa_{n,h} * \bar u_all >= -epsilon."""

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


@register_constraint("fairshare_deviation_identity")
def add_deviation_identity(m: pyo.ConcreteModel, params: dict) -> None:
    """fairshare_deviation_identity — Linearize absolute deviation around proportional share."""

    def rule(model, i, h):
        fair_target = model.fairshare_weight[h] * model.Avail[i]
        return model.x[i, h] - fair_target == model.dpos[i, h] - model.dneg[i, h]

    m.DeviationIdentity = pyo.Constraint(m.I, m.H, rule=rule)


@register_constraint("item_equity_aggregate_cap")
def add_deviation_item_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """Aggregate per-item L1 deviation cap with dial alpha."""

    def rule(model, i):
        alpha = _get_dial_value(model, params, "alpha", i)
        return sum(model.dpos[i, h] + model.dneg[i, h] for h in model.H) <= alpha * model.Avail[i]

    m.DeviationItemCap = pyo.Constraint(m.I, rule=rule)


@register_constraint("household_equity_aggregate_cap")
def add_deviation_household_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """Aggregate per-household L1 deviation cap with dial beta."""

    def rule(model, h):
        beta = _get_dial_value(model, params, "beta", h)
        return sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I) <= beta * model.TotSupply

    m.DeviationHouseholdCap = pyo.Constraint(m.H, rule=rule)


@register_constraint("pairwise_equity_cap")
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
