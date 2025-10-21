"""KPI computation helpers resilient to infeasible solver outcomes."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional

import pyomo.environ as pyo

from fbdam.engine.domain import DomainIndex


def compute_kpis(
    model: pyo.ConcreteModel,
    domain: DomainIndex | None,
    solver_report: Mapping[str, Any],
) -> Dict[str, Any]:
    """Compute KPI aggregates from a solved model.

    KPIs are organised into five categories:
    - basic: model dimensions and objective value
    - supply: physical allocation totals
    - nutrition: aggregate nutritional outcomes
    - allocation_equity: deviations from proportional fair-share
    - nutritional_adequacy: compliance with minimum utility floors

    For infeasible solves a minimal structure is returned so that reporting
    remains functional without evaluating undefined Pyomo expressions.
    """

    solver_section = solver_report.get("solver")
    is_feasible = True
    if isinstance(solver_section, Mapping):
        is_feasible = solver_section.get("is_feasible", True)

    metrics: Dict[str, Dict[str, Any]] = {"basic": {}}
    basic = metrics["basic"]

    basic["items"] = len(domain.items) if domain else None
    basic["households"] = len(domain.households) if domain else None
    basic["nutrients"] = len(domain.nutrients) if domain else None
    if isinstance(solver_section, Mapping):
        basic["objective_value"] = solver_section.get("objective_value")
    else:
        basic["objective_value"] = None

    if not is_feasible:
        basic["objective_value"] = None
        basic["feasibility_status"] = "INFEASIBLE"
        return {"kpi": {"basic": basic}}

    metrics["supply"] = {
        "total_allocation": _safe_value(model.TotAllocated),
        "avg_allocation_per_pair": _safe_value(model.MeanAllocated),
        "undistributed": _safe_value(model.Undistributed),
        "total_cost": _safe_value(model.TotalCost),
    }

    total_utility = _safe_value(model.total_nutritional_utility)
    global_mean = _safe_value(model.global_mean_utility)
    min_household_mean = _safe_min(
        _safe_value(model.household_mean_utility[h]) for h in model.H
    )
    min_nutrient_mean = _safe_min(
        _safe_value(model.nutrient_mean_utility[n]) for n in model.N
    )
    min_pairwise_utility = _safe_min(
        _safe_value(model.u[n, h]) for n in model.N for h in model.H
    )

    metrics["nutrition"] = {
        "total_nutritional_utility": total_utility,
        "global_mean_utility": global_mean,
        "min_household_mean_utility": min_household_mean,
        "min_nutrient_mean_utility": min_nutrient_mean,
        "min_pairwise_utility": min_pairwise_utility,
    }

    metrics["allocation_equity"] = {
        "global_mean_deviation_from_fairshare": _safe_value(model.global_mean_deviation_from_fairshare),
        "max_household_mean_deviation": _safe_max(
            _safe_value(model.household_mean_deviation_from_fairshare[h]) for h in model.H
        ),
        "max_item_mean_deviation": _safe_max(
            _safe_value(model.item_mean_deviation_from_fairshare[i]) for i in model.I
        ),
        "max_pairwise_deviation": _safe_max(
            _safe_value(model.dpos[i, h] + model.dneg[i, h]) for i in model.I for h in model.H
        ),
        "max_household_relative_deviation": _safe_max(
            _safe_value(model.household_mean_relative_deviation_from_fair_share[h]) for h in model.H
        ),
        "max_item_relative_deviation": _safe_max(
            _safe_value(model.item_mean_relative_deviation_from_fair_share[i]) for i in model.I
        ),
        "max_pairwise_relative_deviation": _safe_max(
            _safe_value(model.pair_relative_deviation_from_fair_share[i, h]) for i in model.I for h in model.H
        ),
    }

    metrics["nutritional_adequacy"] = {
        "min_household_mean_utility": min_household_mean,
        "min_nutrient_mean_utility": min_nutrient_mean,
        "min_pairwise_utility": min_pairwise_utility,
    }

    if global_mean is not None and global_mean > 0:
        adequacy = metrics["nutritional_adequacy"]
        min_vals = {
            "household_adequacy_gap": adequacy["min_household_mean_utility"],
            "nutrient_adequacy_gap": adequacy["min_nutrient_mean_utility"],
            "pairwise_adequacy_gap": adequacy["min_pairwise_utility"],
        }
        for key, value in min_vals.items():
            adequacy[key] = (
                (global_mean - value) / global_mean if value is not None else None
            )

    for category in metrics.values():
        for key, value in list(category.items()):
            if isinstance(value, (int, float)):
                category[key] = round(float(value), 5)

    return {"kpi": metrics}


def _safe_value(expr: Any) -> Optional[float]:
    """Evaluate a Pyomo expression returning ``None`` when undefined."""

    try:
        val = pyo.value(expr, exception=False)
    except Exception:  # pragma: no cover - defensive guard
        return None
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):  # pragma: no cover - defensive guard
        return None


def _safe_min(values: Iterable[Optional[float]]) -> Optional[float]:
    """Return the minimum of non-null values from an iterable."""

    filtered = [val for val in values if val is not None]
    if not filtered:
        return None
    return min(filtered)

def _safe_max(values: Iterable[Optional[float]]) -> Optional[float]:
    """Return the maximum of non-null values from an iterable."""

    filtered = [val for val in values if val is not None]
    if not filtered:
        return None
    return max(filtered)