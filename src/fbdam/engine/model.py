"""
model.py — Model builder
------------------------
Constructs the Pyomo model from validated configuration and domain data.

Inputs expected:
- domain: fbdam.engine.domain.DomainIndex      (immutable, typed container)
- model_spec: dict-like with:
    {
      "constraints": [{"id": "<name>", "params": {...}}, ...],
      "objectives":  [{"name": "<name>", "sense": "maximize", "params": {...}}]
    }

Notes:
- Requirements: We expose R[h,n].
- We protect against division-by-zero by flooring R[h,n] with a small epsilon.
- Nutrient delivery q[n,h] is an Expression from x[i,h] and item nutrient content.
- Utility u[n,h] is a variable bounded in [0, 1]; keep it clean and let constraints
  (e.g., u_link) define the linkage.
- We predefine deviation variables (dpos/dneg) frequently used by fairness caps.
- 'household_adequacy_floor' plugins expect mean and global mean utility expressions.

This builder does NOT read files. All I/O/validation should happen in io.py.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple
import pyomo.environ as pyo

from fbdam.engine.domain import (
    DomainIndex,
    Item,
    Nutrient,
    Household,
    Requirement,
    ItemNutrient,
    AllocationBounds,
)
from fbdam.engine.constraints import get_constraint
from fbdam.engine.objectives import get_objective


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def build_model(cfg: dict) -> pyo.ConcreteModel:
    """
    Build a Pyomo model from a validated configuration dictionary.

    Expected cfg shape (minimal):
      cfg = {
        "domain": DomainIndex(...),
        "model_params": {...},
        "model": {
          "constraints": [{"id": "nutrition_utility_mapping", "params": {...}}, ...],
          "objectives":  [{"name": "sum_utility", "sense": "maximize", "params": {...}}]
        }
      }

    The function also accepts the ``ScenarioConfig`` dataclass returned by
    :func:`fbdam.engine.io.load_scenario` and will extract the same pieces.

    Returns:
        Pyomo ConcreteModel, fully assembled (but not solved).
    """
    domain, constraint_specs, objective_specs, model_params = _unpack_config(cfg)
    m = pyo.ConcreteModel(name="FBDAM")

    allow_purchases = _should_enable_purchases(constraint_specs, model_params)

    _build_sets(m, domain)
    _build_params(m, domain)
    _build_variables(m, domain, allow_purchases=allow_purchases)
    _build_expressions(m)

    # Expose raw (non-Pyomo) parameters so plugins can read dials/budget/etc.
    m.model_params = model_params or {}
    m.allow_purchases = allow_purchases

    _apply_constraint_plugins(m, constraint_specs)
    _apply_objective_plugin(m, objective_specs)

    return m


def _unpack_config(cfg: object) -> Tuple[DomainIndex, Sequence[dict], Sequence[dict], Dict[str, Any]]:
    """Normalize configuration input for the builder.

    Supports both the historical dict-based API and the newer ``ScenarioConfig``
    dataclass returned by :func:`fbdam.engine.io.load_scenario`.
    """

    if hasattr(cfg, "domain") and hasattr(cfg, "constraints"):
        domain = getattr(cfg, "domain")
        constraints = [
            {"id": c.id, "params": dict(c.params)}
            for c in getattr(cfg, "constraints", [])
        ]
        objectives = [
            {"name": o.name, "sense": o.sense, "params": o.params}
            for o in getattr(cfg, "objectives", [])
        ]
        model_params = getattr(cfg, "model_params", {})
        return domain, constraints, objectives, model_params

    # Fallback to dict-style configuration
    spec = cfg.get("model", {}) if isinstance(cfg, Mapping) else {}
    domain = cfg["domain"] if isinstance(cfg, Mapping) else getattr(cfg, "domain")
    raw_constraints = spec.get("constraints", [])
    objectives = spec.get("objectives", [])
    model_params = cfg.get("model_params", {}) if isinstance(cfg, Mapping) else {}
    constraints = []
    for entry in raw_constraints:
        if isinstance(entry, Mapping):
            params = entry.get("params", {}) or {}
            if not isinstance(params, Mapping):
                raise ValueError("Constraint 'params' must be a mapping.")
            constraints.append({"id": entry.get("id") or entry.get("type"), "params": dict(params)})
        else:
            constraints.append(entry)
    return domain, constraints, objectives, model_params


# ------------------------------------------------------------
# Internal builders: sets, params, vars, exprs
# ------------------------------------------------------------

def _should_enable_purchases(constraint_specs: Sequence[dict], model_params: Mapping[str, Any] | None) -> bool:
    """Determine whether purchase variables should be active."""

    # Explicit signal from model parameters wins.
    params = model_params or {}
    if isinstance(params, Mapping) and "allow_purchases" in params:
        raw_flag = params.get("allow_purchases")
        if isinstance(raw_flag, str):
            text = raw_flag.strip().lower()
            if text in {"true", "1", "yes", "y", "on"}:
                return True
            if text in {"false", "0", "no", "n", "off"}:
                return False
        if raw_flag is not None:
            return bool(raw_flag)

    # Fall back to detecting plugins that require purchases (currently purchase_budget).
    for spec in constraint_specs:
        name = _get_constraint_name(spec)
        if name in {"purchase_budget_limit", "purchase_budget"}:
            return True

    return False


def _build_sets(m: pyo.ConcreteModel, domain: DomainIndex) -> None:
    """Create fundamental index sets."""
    m.I = pyo.Set(initialize=list(domain.items.keys()), ordered=False, doc="Items")
    m.N = pyo.Set(initialize=list(domain.nutrients.keys()), ordered=False, doc="Nutrients")
    m.H = pyo.Set(initialize=list(domain.households.keys()), ordered=False, doc="Households")

    # Convenience sizes (as numeric Params)
    m.cardI = pyo.Param(initialize=len(m.I), mutable=False)
    m.cardN = pyo.Param(initialize=len(m.N), mutable=False)
    m.cardH = pyo.Param(initialize=len(m.H), mutable=False)


def _build_params(m: pyo.ConcreteModel, domain: DomainIndex) -> None:
    """Create parameters: stock S[i], nutrient content a[i,n], requirements R[h,n], fairshare weights."""

    items: Mapping[str, Item] = domain.items
    nutrients: Mapping[str, Nutrient] = domain.nutrients
    households: Mapping[str, Household] = domain.households
    item_nutrients: Mapping[tuple, ItemNutrient] = domain.item_nutrients
    requirements: Mapping[tuple, Requirement] = domain.requirements

    # Stock per item (>= 0)
    def _S_init(model, i):
        return float(items[i].stock)
    m.S = pyo.Param(m.I, initialize=_S_init, within=pyo.NonNegativeReals, doc="Stock per item")

    # Optional purchase cost per item (>= 0)
    def _cost_init(model, i):
        return float(items[i].cost)

    m.cost = pyo.Param(
        m.I,
        initialize=_cost_init,
        within=pyo.NonNegativeReals,
        doc="Purchase cost per additional unit of item",
    )

    # Household fair-share weight w[h] (>= 0)
    def _fairshare_weight_init(model, h):
        return float(households[h].fairshare_weight)

    m.fairshare_weight = pyo.Param(
        m.H,
        initialize=_fairshare_weight_init,
        within=pyo.NonNegativeReals,
        doc="Household fair-share weight",
    )

    # Nutrient content a[i,n] (>= 0), default 0 if (i,n) pair not present
    def _a_init(model, i, n):
        nutrient_entry = item_nutrients.get((i, n))
        if nutrient_entry is None:
            return 0.0
        return float(nutrient_entry.qty_per_unit)
    m.a = pyo.Param(m.I, m.N, initialize=_a_init, within=pyo.NonNegativeReals, doc="Nutrient content per item-unit")

    # Requirements R[h,n] (>= 0), protect against division by zero with epsilon floor
    EPS_R = 1e-9

    def _R_init(model, h, n):
        req_entry = requirements.get((h, n))
        amt = float(req_entry.amount) if req_entry is not None else 0.0
        return max(amt, EPS_R)

    m.R = pyo.Param(
        m.H, m.N, initialize=_R_init, within=pyo.NonNegativeReals, doc="Requirement amount (floored at eps)"
    )


def _build_variables(
    m: pyo.ConcreteModel, domain: DomainIndex, *, allow_purchases: bool
) -> None:
    """Create decision variables and common auxiliaries."""

    bounds: Mapping[tuple, AllocationBounds] = domain.bounds

    # Item-household allocation x[i,h] with per-(i,h) bounds if provided
    def _x_bounds(model, i, h):
        b = bounds.get((i, h))
        if b is None:
            return (0.0, None)
        lb = float(b.lower)
        ub = None if b.upper is None else float(b.upper)
        return (lb, ub)

    #m.x = pyo.Var(m.I, m.H, domain=pyo.NonNegativeReals, bounds=_x_bounds, doc="Allocation of item i to household h")
    m.x = pyo.Var(m.I, m.H, domain=pyo.NonNegativeIntegers, bounds=_x_bounds, doc="Allocation of item i to household h")

    # Utility u[n,h] in [0,1]
    m.u = pyo.Var(m.N, m.H, bounds=(0.0, 1.0), doc="Nutrient-household utility (normalized)")

    # Purchases y[i] >= 0 (augment donated stock)
    m.y = pyo.Var(m.I, domain=pyo.NonNegativeReals, doc="Purchased quantity of item i")
    if not allow_purchases:
        for var in m.y.values():
            var.fix(0.0)

    # Optional deviation variables used by fairness constraints (kept generic)
    m.dpos = pyo.Var(m.I, m.H, domain=pyo.NonNegativeReals, doc="Positive deviation helper")
    m.dneg = pyo.Var(m.I, m.H, domain=pyo.NonNegativeReals, doc="Negative deviation helper")

    # Global slack epsilon >= 0 (used by soft floors when enabled)
    m.epsilon = pyo.Var(domain=pyo.NonNegativeReals, doc="Global feasibility slack")


def _build_expressions(m: pyo.ConcreteModel) -> None:
    """Create common expressions used by multiple plugins (q, means, etc.)."""

    # ------------------------------------------------------------
    # Basic expressions
    # ------------------------------------------------------------

    # Delivered nutrient quantity q[n,h] := sum_i a[i,n] * x[i,h]
    def _q_expr(model, n, h):
        return sum(model.a[i, n] * model.x[i, h] for i in model.I)
    m.q = pyo.Expression(m.N, m.H, rule=_q_expr)

    # Available supply per item: Avail_i := S_i + y_i
    def _avail_expr(model, i):
        return model.S[i] + model.y[i]
    m.Avail = pyo.Expression(m.I, rule=_avail_expr, doc="Available units of item i (stock + purchase)")

    # Total available supply: TotSupply := sum_i (S_i + y_i)
    def _total_supply_expr(model):
        return sum(model.Avail[i] for i in model.I)
    m.TotSupply = pyo.Expression(rule=_total_supply_expr, doc="Total available supply across all items")

    # Total allocation per household: X_h := sum_i x[i,h]
    def _household_total_expr(model, h):
        return sum(model.x[i, h] for i in model.I)
    m.X = pyo.Expression(m.H, rule=_household_total_expr, doc="Total allocation delivered to household h")

    # ------------------------------------------------------------
    # Aggregate expressions (mainly for reporting)
    # ------------------------------------------------------------

    # Total allocated quantity: TotAllocated := sum_{i,h} x[i,h]
    def _total_allocated_expr(model):
        return sum(model.x[i, h] for i in model.I for h in model.H)
    m.TotAllocated = pyo.Expression(rule=_total_allocated_expr, doc="Total allocated quantity across all items and households")


    # Mean allocated quantity per household: MeanAllocated := (1 / cardH) * TotAllocated
    def _mean_allocated_expr(model):
        if len(model.H) == 0:
            return 0.0
        return model.TotAllocated / model.cardH
    m.MeanAllocated = pyo.Expression(rule=_mean_allocated_expr, doc="Mean allocated quantity per household")


    # Undistributed quantity: Undistributed := TotSupply - TotAllocated
    def _undistributed_expr(model):
        return model.TotSupply - model.TotAllocated
    m.Undistributed = pyo.Expression(rule=_undistributed_expr, doc="Total undistributed quantity across all items")
    

    # Total purchased cost: Cost := sum_i cost[i] * y[i]
    def _total_cost_expr(model):
        return sum(model.cost[i] * model.y[i] for i in model.I)
    m.TotalCost = pyo.Expression(rule=_total_cost_expr, doc="Total purchase cost across all items")


    # ------------------------------------------------------------
    # Nutritional utility expressions
    # ------------------------------------------------------------

    # Total nutritional utility: sum_{n,h} u[n,h]
    def _total_utility_expr(model):
        return sum(model.u[n, h] for n in model.N for h in model.H)
    m.total_nutritional_utility = pyo.Expression(rule=_total_utility_expr, doc="Aggregate nutritional utility")


    # Household mean utility: mean over nutrients
    def _mean_u(model, h):
        return (1.0 / model.cardN) * sum(model.u[n, h] for n in model.N)
    if len(m.N) == 0:
        m.household_mean_utility = pyo.Expression(m.H, initialize=0.0)
    else:
        m.household_mean_utility = pyo.Expression(m.H, rule=_mean_u)


    # Nutrient mean utility: mean over households
    def _mean_u_nutrient(model, n):
        return (1.0 / model.cardH) * sum(model.u[n, h] for h in model.H)
    if len(m.H) == 0:
        m.nutrient_mean_utility = pyo.Expression(m.N, initialize=0.0)
    else:
        m.nutrient_mean_utility = pyo.Expression(m.N, rule=_mean_u_nutrient)


    # Global mean utility: mean over households of household mean utility
    def _global_mean(model):
        if len(model.N) == 0 or len(model.H) == 0:
            return 0.0
        return model.total_nutritionalutility / (model.cardN * model.cardH)
    m.global_mean_utility = pyo.Expression(
        rule=_global_mean, doc="Global mean utility across all nutrient-household pairs"
    )


    # ------------------------------------------------------------
    # Deviation from fair share expressions
    # ------------------------------------------------------------

    # Total deviation from fair share: sum_{i,h} (dpos[i,h] + dneg[i,h])
    def _total_deviation_expr(model):
        return sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I for h in model.H)
    m.total_fairshare_deviation = pyo.Expression(rule=_total_deviation_expr)


    # Household mean deviation from fair share: mean over nutrients
    def _mean_deviation_household(model, h):
        return (1.0 / model.cardI) * sum(model.dpos[i, h] + model.dneg[i, h] for i in model.I)
    m.household_mean_fairshare_deviation = pyo.Expression(m.H, rule=_mean_deviation_household)


    # Item mean deviation from fair share: mean over households
    def _mean_deviation_item(model, i):
        return (1.0 / model.cardH) * sum(model.dpos[i, h] + model.dneg[i, h] for h in model.H)
    m.item_mean_fairshare_deviation = pyo.Expression(m.I, rule=_mean_deviation_item)


    # Global mean deviation from fair share: mean over all nutrient-household pairs
    def _global_mean_deviation(model):
        if len(model.I) == 0 or len(model.H) == 0:
            return 0.0
        return model.total_fairshare_deviation / (model.cardI * model.cardH)
    m.global_mean_fairshare_deviation = pyo.Expression(rule=_global_mean_deviation)

# ------------------------------------------------------------
# Apply plugins (constraints & objective)
# ------------------------------------------------------------


def _get_constraint_name(spec: Mapping[str, Any] | Any) -> str | None:
    if not isinstance(spec, Mapping):
        return None
    raw = spec.get("id") or spec.get("type")
    if isinstance(raw, str):
        name = raw.strip()
        return name or None
    return None


def _apply_constraint_plugins(m: pyo.ConcreteModel, constraint_specs: Iterable[dict]) -> None:
    """
    Apply registered constraint blocks in the order provided.

    Each spec should contain:
      { "id": "<registry name>", "params": {...} }
    """
    for idx, c in enumerate(constraint_specs, start=1):
        name = _get_constraint_name(c)
        params: Dict = c.get("params", {})
        if not name:
            raise ValueError(f"Constraint spec at position {idx} missing 'id' key.")
        handler = get_constraint(name)
        handler(m, params)


def _apply_objective_plugin(m: pyo.ConcreteModel, objective_specs: Iterable[dict]) -> None:
    """
    Apply the (first) registered objective handler.

    Each spec should contain:
      { "name": "<registry name>", "sense": "maximize|minimize", "params": {...} }

    If multiple objectives are supplied, we currently take the first one.
    Weighted or lexicographic combinations can be implemented in the future
    at the builder level.
    """
    specs = list(objective_specs)
    if not specs:
        # Provide a minimal default if none specified
        specs = [{"name": "sum_utility", "sense": "maximize", "params": {}}]

    obj = specs[0]
    name = obj.get("name")
    sense = obj.get("sense", "maximize")
    params: Dict = obj.get("params", {})

    if not name:
        raise ValueError("Objective spec missing 'name' key.")

    handler = get_objective(name)
    handler(m, params=params, sense=sense)
