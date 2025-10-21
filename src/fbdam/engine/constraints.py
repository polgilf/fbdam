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
    if lam_value is not None:
        # Specification alignment: providing lambda (even 0) should enable the
        # shared slack variable so that λ = 0 yields the diagnostic regime
        # described in the mathematical model.
        return True
    return False


def _slack_term(m: pyo.ConcreteModel, params: Mapping[str, Any]) -> pyo.Expression | float:
    return m.epsilon if _should_use_slack(m, params) else 0.0


# ═══════════════════════════════════════════════════════════════════
# CORE MECHANICS CONSTRAINTS
# ───────────────────────────────────────────────────────────────────
# Structural relationships that ground the model: utility normalisation,
# supply conservation, and budget linkage. They enable the equity and
# adequacy mechanisms but are not dial-controlled themselves.
# ═══════════════════════════════════════════════════════════════════

@register_constraint("nutrition_utility_mapping")
def add_u_link(m: pyo.ConcreteModel, params: dict) -> None:
    """
    CORE MECHANICS: Nutritional utility upper bound
    ───────────────────────────────────────────────
    Links normalised household–nutrient utility to delivered quantity and
    requirement levels so that utility cannot exceed the achievable ratio.

    Mathematical form:
        u[n,h] ≤ q[n,h] / R[h,n]     ∀ n ∈ N, h ∈ H

    Dial parameter:
        None (structural constraint without a policy dial).

    Promotes:
        Consistent normalisation between allocation decisions and utility
        outcomes, ensuring comparability across constraints.
    """
    def rule(m, n, h):
        return m.u[n, h] <= m.q[n, h] / m.R[h, n]

    m.U_link = pyo.Constraint(m.N, m.H, rule=rule)


@register_constraint("item_supply_limit")
def add_stock_balance(m: pyo.ConcreteModel, params: dict) -> None:
    """
    CORE MECHANICS: Item supply conservation
    ────────────────────────────────────────
    Prevents total allocations of each item from exceeding the available
    quantity (donated stock plus purchases), preserving feasibility of the
    distribution plan.

    Mathematical form:
        Σ_h x[i,h] ≤ Avail[i]     ∀ i ∈ I

    Dial parameter:
        None (structural constraint without a policy dial).

    Promotes:
        Feasible allocation plans that respect physical supply limits.
    """

    def rule(model, i):
        return sum(model.x[i, h] for h in model.H) <= model.Avail[i]

    m.StockBalance = pyo.Constraint(m.I, rule=rule)


@register_constraint("purchase_budget_limit")
def add_purchase_budget(m: pyo.ConcreteModel, params: dict) -> None:
    """
    CORE MECHANICS: Purchase budget enforcement
    ───────────────────────────────────────────
    Couples purchase decisions with the available monetary budget. Ensures
    purchased quantities respect budget limits, activate only when needed,
    and avoid waste when procurement occurs.

    Mathematical form:
        1. Σ_i cost[i] · y[i] ≤ budget
        2. y[i] ≤ M[i] · y_active[i]     ∀ i ∈ I
        3. Avail[i] - Σ_h x[i,h] ≤ S[i] · (1 - y_active[i])     ∀ i ∈ I

    Dial parameter:
        budget: Monetary budget available for purchases (scalar parameter).

    Promotes:
        Efficient use of procurement funds by linking spending to distribution
        outcomes and preventing unnecessary purchases.
    """

    budget = params.get("budget") if isinstance(params, Mapping) else None
    if budget is None:
        budget = _get_model_params(m).get("budget")
    if budget is None:
        raise ValueError("purchase_budget constraint requires a 'budget' value.")

    budget_value = float(budget)

    # 1. BUDGET LIMIT
    """
    Mathematical form:
        Σ_i cost[i] * y[i] ≤ budget
    """
    def _budget_rule(model):
        return sum(model.cost[i] * model.y[i] for i in model.I) <= budget_value
    
    m.PurchaseBudget = pyo.Constraint(rule=_budget_rule)

    # 2. PURCHASE ACTIVATION
    """
    Mathematical form:
        y[i] ≤ M[i] * y_active[i]     ∀ i ∈ I
    where M[i] = budget / cost[i] (with small epsilon to avoid div-by-zero)
    """
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

    # 3. NO WASTE WHEN PURCHASING
    # If purchases are activated (y_active = 1), force full allocation of
    # Avail[i] = S[i] + y[i]. If no purchases (y_active = 0), allow up to
    # S[i] units of donated stock to remain unallocated.
    """
    Mathematical form:
        Avail[i] - Σ_h x[i,h] ≤ S[i] * (1 - y_active[i])     ∀ i ∈ I

    where Avail[i] = S[i] + y[i]
    """

    def _no_waste_rule(model, item_id: str):
        unallocated = model.Avail[item_id] - sum(model.x[item_id, h] for h in model.H)
        max_waste_without_purchase = model.S[item_id]
        return unallocated <= max_waste_without_purchase * (1 - model.y_active[item_id])

    m.PurchaseNoWaste = pyo.Constraint(m.I, rule=_no_waste_rule)


# ═══════════════════════════════════════════════════════════════════
# ALLOCATION EQUITY CONSTRAINTS (α, β, γ)
# ───────────────────────────────────────────────────────────────────
# Enforce proportional fair-share allocations across items, households,
# and their intersections. These caps limit inequality in the physical
# distribution of food items.
# ═══════════════════════════════════════════════════════════════════


@register_constraint("fairshare_deviation_identity")
def add_deviation_identity(m: pyo.ConcreteModel, params: dict) -> None:
    """
    ALLOCATION EQUITY: Fair-share deviation identity
    ────────────────────────────────────────────────
    Linearises proportional allocation deviations by linking actual
    allocation to the fair-share target through positive/negative slack
    variables. Serves as the foundation for allocation equity caps.

    Mathematical form:
        x[i,h] - w[h]·Avail[i] = δ⁺[i,h] - δ⁻[i,h]     ∀ i ∈ I, h ∈ H

    Dial parameter:
        None (auxiliary identity enabling allocation equity caps).

    Promotes:
        Accurate measurement of proportional allocation deviations that
        drive allocation equity constraints.
    """

    def rule(model, i, h):
        fair_target = model.fairshare_weight[h] * model.Avail[i]
        return model.x[i, h] - fair_target == model.dpos[i, h] - model.dneg[i, h]

    m.DeviationIdentity = pyo.Constraint(m.I, m.H, rule=rule)


@register_constraint("item_equity_aggregate_cap")
def add_deviation_item_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """
    ALLOCATION EQUITY: Item-level proportional fairness cap
    ────────────────────────────────────────────────────────
    Limits aggregate deviation from the fair-share target for each item
    across all households, preventing item-specific concentration of the
    food basket.

    Mathematical form:
        Σ_h (δ⁺[i,h] + δ⁻[i,h]) ≤ α_i · Avail[i]     ∀ i ∈ I

    Dial parameter:
        alpha_i: Maximum tolerated deviation as a fraction of item supply.
                  Lower values enforce stricter item-level allocation equity.

    Promotes:
        Horizontal equity by distributing each item proportionally.
    """

    def rule(model, i):
        alpha = _get_dial_value(model, params, "alpha_i", i)
        return sum(model.dpos[i, h] + model.dneg[i, h] for h in model.H) <= alpha * model.Avail[i]

    m.DeviationItemCap = pyo.Constraint(m.I, rule=rule)


@register_constraint("household_equity_aggregate_cap")
def add_deviation_household_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """
    ALLOCATION EQUITY: Household-level proportional fairness cap
    ─────────────────────────────────────────────────────────────
    Caps total deviation from fair-share for each household across all
    items, ensuring allocations scale with household size and weights.

    Mathematical form:
        Σ_i (δ⁺[i,h] + δ⁻[i,h]) ≤ β_h · w[h] · TotSupply     ∀ h ∈ H

    Dial parameter:
        beta_h: Maximum tolerated deviation relative to the household fair-share
                 weight. Lower values enforce stricter vertical allocation equity.

    Promotes:
        Vertical equity by keeping household allocations proportional to need.
    """

    def rule(model, h):
        beta = _get_dial_value(model, params, "beta_h", h)
        fair_target = model.fairshare_weight[h] * model.TotSupply
        return sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I) <= beta * fair_target

    m.DeviationHouseholdCap = pyo.Constraint(m.H, rule=rule)


@register_constraint("pairwise_equity_cap")
def add_deviation_pair_cap(m: pyo.ConcreteModel, params: dict) -> None:
    """
    ALLOCATION EQUITY: Pairwise proportional fairness cap
    ──────────────────────────────────────────────────────
    Restricts deviation for each (item, household) pair relative to its
    fair-share target, preventing extreme concentration or deprivation
    at the most granular allocation level.

    Mathematical form:
        δ⁺[i,h] + δ⁻[i,h] ≤ γ_{i,h} · w[h] · Avail[i]     ∀ i ∈ I, h ∈ H

    Dial parameter:
        gamma_{i,h}: Maximum tolerated pairwise deviation fraction.
                      Legacy aliases ``rho`` and ``gamma`` are accepted for backward compatibility.

    Promotes:
        Fine-grained proportional equity by bounding individual allocation gaps.
    """

    def rule(model, i, h):
        try:
            gamma = _get_dial_value(model, params, "gamma_i_h", (i, h), default=None)
        except (KeyError, ValueError):
            gamma = None
        if gamma is None:
            try:
                gamma = _get_dial_value(model, params, "rho", (i, h), default=None)
            except (KeyError, ValueError):
                gamma = None
        if gamma is None:
            gamma = _get_dial_value(model, params, "gamma", (i, h))
        fair_target = model.fairshare_weight[h] * model.Avail[i]
        return model.dpos[i, h] + model.dneg[i, h] <= gamma * fair_target

    m.DeviationPairCap = pyo.Constraint(m.I, m.H, rule=rule)


@register_constraint("fairshare_cap_house")
def add_fairshare_cap_house(m: pyo.ConcreteModel, params: dict) -> None:
    """
    ALLOCATION EQUITY: Legacy household deviation cap
    ──────────────────────────────────────────────────
    Historical formulation that limits household-level deviation using the
    same β dial as aggregate caps. Retained for compatibility with prior
    catalogues while emphasising proportional allocation equity.

    Mathematical form:
        Σ_i |x[i,h] - fair_share[i,h]| ≤ β · w[h] · TotSupply     ∀ h ∈ H

    Dial parameter:
        beta_h: Household deviation tolerance shared with modern aggregate cap.
                 Legacy alias ``beta`` is accepted for backward compatibility.

    Promotes:
        Vertical allocation equity in legacy catalogues.
    """

    try:
        beta = _get_dial_value(m, params, "beta_h", default=None)
    except (KeyError, ValueError):
        beta = None
    if beta is None:
        beta = _get_dial_value(m, params, "beta", default=0.7)

    def rule(model, h):
        return sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I) <= beta * model.fairshare_weight[h] * model.TotSupply

    m.FairCapHouse = pyo.Constraint(m.H, rule=rule)


# ═══════════════════════════════════════════════════════════════════
# NUTRITIONAL ADEQUACY CONSTRAINTS (κ, ρ, ω)
# ───────────────────────────────────────────────────────────────────
# Guarantee minimum nutritional outcomes relative to the global mean
# utility. These floors prevent deprivation and promote sufficiency
# across nutrients, households, and their intersections.
# ═══════════════════════════════════════════════════════════════════


@register_constraint("household_adequacy_floor")
def add_household_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """
    NUTRITIONAL ADEQUACY: Household minimum utility threshold
    ──────────────────────────────────────────────────────────
    Ensures each household attains a minimum average nutritional utility
    relative to the global mean, preventing household-level deprivation.

    Mathematical form:
        ȳ_h ≥ ρ_h · ū_global - ε     ∀ h ∈ H

    Dial parameter:
        rho_h: Required fraction of the global mean utility for each household.
                 Legacy alias ``omega`` is accepted for backward compatibility.

    Promotes:
        Vertical adequacy by guaranteeing sufficiency for every household.
    """

    slack = _slack_term(m, params)

    def rule(model, h):
        try:
            rho = _get_dial_value(model, params, "rho_h", h, default=None)
        except (KeyError, ValueError):
            rho = None
        if rho is None:
            rho = _get_dial_value(model, params, "omega", h, default=0.0)
        return model.household_mean_utility[h] - rho * model.global_mean_utility >= -slack

    m.HouseholdFloor = pyo.Constraint(m.H, rule=rule)


@register_constraint("nutrient_adequacy_floor")
def add_nutrient_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """
    NUTRITIONAL ADEQUACY: Nutrient minimum utility threshold
    ─────────────────────────────────────────────────────────
    Requires each nutrient, averaged across households, to achieve a
    minimum utility relative to the global mean, maintaining balanced diets.

    Mathematical form:
        ȳ_n ≥ κ_n · ū_global - ε     ∀ n ∈ N

    Dial parameter:
        kappa_n: Minimum fraction of global mean utility per nutrient.
                  Legacy alias ``gamma`` is accepted for backward compatibility.

    Promotes:
        Nutrient-level adequacy by avoiding systemic shortfalls in any nutrient.
    """

    slack = _slack_term(m, params)

    def rule(model, n):
        try:
            kappa = _get_dial_value(model, params, "kappa_n", n, default=None)
        except (KeyError, ValueError):
            kappa = None
        if kappa is None:
            kappa = _get_dial_value(model, params, "gamma", n, default=0.0)
        return model.nutrient_mean_utility[n] - kappa * model.global_mean_utility >= -slack

    m.NutrientFloor = pyo.Constraint(m.N, rule=rule)


@register_constraint("pairwise_adequacy_floor")
def add_pair_floor(m: pyo.ConcreteModel, params: dict) -> None:
    """
    NUTRITIONAL ADEQUACY: Pairwise minimum utility threshold
    ─────────────────────────────────────────────────────────
    Enforces minimum utility for each nutrient–household pair, ensuring
    no beneficiary lacks a critical nutrient even if global averages are met.

    Mathematical form:
        u[n,h] ≥ ω_{n,h} · ū_global - ε     ∀ n ∈ N, h ∈ H

    Dial parameter:
        omega_{n,h}: Minimum acceptable utility fraction per nutrient–household.
                      Legacy alias ``kappa`` is accepted for backward compatibility.

    Promotes:
        Egalitarian adequacy by protecting the most granular nutrition outcomes.
    """

    slack = _slack_term(m, params)

    def rule(model, n, h):
        try:
            omega = _get_dial_value(model, params, "omega_n_h", (n, h), default=None)
        except (KeyError, ValueError):
            omega = None
        if omega is None:
            omega = _get_dial_value(model, params, "kappa", (n, h), default=0.0)
        return model.u[n, h] - omega * model.global_mean_utility >= -slack

    m.PairFloor = pyo.Constraint(m.N, m.H, rule=rule)

# ---------------------------------------------------------------------
# Utility: list registered constraints
# ---------------------------------------------------------------------

def list_constraints() -> None:
    """Print a summary of all registered constraints."""
    print("Registered constraints:")
    for name in sorted(CONSTRAINTS_REGISTRY):
        print(f"  - {name}")
