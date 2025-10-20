from __future__ import annotations

from typing import Dict, Mapping

import pyomo.environ as pyo

from fbdam.engine.domain import DomainIndex


def _value(expr: pyo.Component) -> float:
    return float(pyo.value(expr, exception=False) or 0.0)


def compute_metrics(model: pyo.ConcreteModel, domain: DomainIndex, solver_report: Mapping[str, object]) -> Dict[str, object]:
    total_nutrient_utility = _value(model.total_nutrient_utility)
    gap = float(solver_report.get("gap", 0.0) or 0.0)
    wallclock = float(solver_report.get("elapsed_sec", 0.0) or 0.0)
    is_feasible = bool(solver_report.get("is_feasible", True))

    totals = {h: _value(model.household_allocation[h]) for h in model.H}
    weights = {h: float(domain.households[h].fairshare_weight or 1.0) for h in model.H}
    total_weight = sum(weights.values()) or 1.0
    total_distribution = sum(totals.values()) or 1.0

    hoover = 0.0
    for h in model.H:
        share_allocation = totals[h] / total_distribution
        share_weight = weights[h] / total_weight
        hoover += abs(share_allocation - share_weight)
    hoover *= 0.5

    metrics = {
        "tnu": round(total_nutrient_utility, 6),
        "equity_index_hoover": round(hoover, 6),
        "gap": gap,
        "wallclock_s": round(wallclock, 6),
        "n_vars": sum(len(v) for v in model.component_objects(pyo.Var)),
        "n_cons": sum(len(c) for c in model.component_objects(pyo.Constraint)),
        "checks": {"feasible": is_feasible},
    }
    return metrics


__all__ = ["compute_metrics"]
