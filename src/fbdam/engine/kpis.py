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

    metrics["utility"] = {
        "total_nutritional_utility": _safe_value(model.total_nutritional_utility),
        "global_mean_utility": _safe_value(model.global_mean_utility),
        "min_mean_utility_per_household": _safe_min(
            _safe_value(model.household_mean_utility[h]) for h in model.H
        ),
        "min_mean_utility_per_nutrient": _safe_min(
            _safe_value(model.nutrient_mean_utility[n]) for n in model.N
        ),
        "min_overall_utility": _safe_min(
            _safe_value(model.u[n, h]) for n in model.N for h in model.H
        ),
    }

    metrics["fairness"] = {
        "global_mean_deviation_from_fair_share": _safe_value(model.global_mean_deviation_from_fairshare),
        "min_mean_deviation_from_fair_share_per_household": _safe_min(
            _safe_value(model.household_mean_deviation_from_fairshare[h]) for h in model.H
        ),
        "min_mean_deviation_from_fair_share_per_nutrient": _safe_min(
            _safe_value(model.item_mean_deviation_from_fairshare[n]) for n in model.I
        ),
        "min_overall_deviation_from_fair_share": _safe_min(
            _safe_value(model.dpos[i, h] + model.dneg[i, h]) for i in model.I for h in model.H
        ),
    }

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
