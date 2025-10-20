from __future__ import annotations
from typing import Any, Dict, Iterable, Mapping, Sequence
import pyomo.environ as pyo

from fbdam.engine.domain import DomainIndex

ArtifactRows = Iterable[Sequence[Any]]


def compute_kpis(
    model: pyo.ConcreteModel,
    domain: DomainIndex | None,
    solver_report: Mapping[str, Any],
) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {}

    # Basic counts
    metrics["basic"]=  {}
    if domain is not None:
        metrics["basic"]["items"] = len(domain.items)
        metrics["basic"]["households"] = len(domain.households)
        metrics["basic"]["nutrients"] = len(domain.nutrients)

    # Objective value
    solver_section = solver_report.get("solver")
    if isinstance(solver_section, Mapping) and "objective_value" in solver_section:
        metrics["basic"]["objective_value"] = solver_section["objective_value"]

    # ------------------------------------------------------------
    # Allocation stats (TotalAllocated, MeanAllocated, Undistributed, TotalCost)
    # ------------------------------------------------------------
    metrics["supply"] = {}
    metrics["supply"]["total_allocation"] = pyo.value(model.TotAllocated, exception=False)
    metrics["supply"]["avg_allocation_per_pair"] = pyo.value(model.MeanAllocated, exception=False)
    metrics["supply"]["undistributed"] = pyo.value(model.Undistributed, exception=False)
    metrics["supply"]["total_cost"] = pyo.value(model.TotalCost, exception=False)

    # ------------------------------------------------------------
    # Utility stats (total_utility, global_mean_utility, min(household_mean_utility), min(nutrient_mean_utility), min_overall_utility)
    # ------------------------------------------------------------
    metrics["utility"] = {}
    metrics["utility"]["total_nutritional_utility"] = pyo.value(model.total_nutritional_utility, exception=False)
    metrics["utility"]["global_mean_utility"] = pyo.value(model.global_mean_utility, exception=False)
    metrics["utility"]["min_mean_utility_per_household"] = min(
        pyo.value(model.household_mean_utility[h], exception=False) for h in model.H)
    metrics["utility"]["min_mean_utility_per_nutrient"] = min(
        pyo.value(model.nutrient_mean_utility[n], exception=False) for n in model.N)
    metrics["utility"]["min_overall_utility"] = min(
        pyo.value(model.u[n, h], exception=False) for n in model.N for h in model.H)

    # ------------------------------------------------------------
    # Fairness deviation stats (global_mean_deviation_from_fair_share, min_mean_deviation_per_household, min_mean_deviation_per_nutrient, min_overall_deviation_from_fair_share)
    # ------------------------------------------------------------
    metrics["fairness"] = {}
    metrics["fairness"]["global_mean_deviation_from_fair_share"] = pyo.value(model.global_mean_deviation_from_fairshare, exception=False)
    metrics["fairness"]["min_mean_deviation_from_fair_share_per_household"] = min(
        pyo.value(model.household_mean_deviation_from_fairshare[h], exception=False) for h in model.H)
    metrics["fairness"]["min_mean_deviation_from_fair_share_per_nutrient"] = min(
        pyo.value(model.item_mean_deviation_from_fairshare[n], exception=False) for n in model.I)
    metrics["fairness"]["min_overall_deviation_from_fair_share"] = min(
        pyo.value(model.dpos[i, h] + model.dneg[i, h], exception=False) for i in model.I for h in model.H)

    # Round all metrics to 4 decimal places
    for cat, sub in metrics.items():
        if isinstance(sub, dict):
            for k, v in sub.items():
                if isinstance(v, (int, float)):
                    sub[k] = round(float(v), 5)

    return {"kpi": metrics}









'''





    # Utility stats
    util_sum = 0.0
    util_count = 0
    min_single = None
    if hasattr(model, "u"):
        nutrients = sorted(list(model.N), key=str)
        households = sorted(list(model.H), key=str)

        house_sums: Dict[Any, float] = {h: 0.0 for h in households}
        house_counts: Dict[Any, int] = {h: 0 for h in households}
        nut_sums: Dict[Any, float] = {n: 0.0 for n in nutrients}
        nut_counts: Dict[Any, int] = {n: 0 for n in nutrients}

        for n in nutrients:
            for h in households:
                value = pyo.value(model.u[n, h], exception=False)
                if value is None:
                    continue
                val = float(value)
                util_sum += val
                util_count += 1
                if min_single is None or val < min_single:
                    min_single = val
                house_sums[h] += val
                house_counts[h] += 1
                nut_sums[n] += val
                nut_counts[n] += 1

        house_means: List[float] = [
            (house_sums[h] / house_counts[h]) if house_counts[h] else 0.0
            for h in households
        ]
        nut_means: List[float] = [
            (nut_sums[n] / nut_counts[n]) if nut_counts[n] else 0.0
            for n in nutrients
        ]
    else:
        house_means = []
        nut_means = []
        min_single = None

    metrics["mean_utility"] = util_sum / util_count if util_count else 0.0
    metrics["min_mean_utility_per_household"] = min(house_means) if house_means else 0.0
    metrics["min_mean_utility_per_nutrient"] = min(nut_means) if nut_means else 0.0
    metrics["min_overall_utility"] = float(min_single) if min_single is not None else 0.0



    # Deviation from fair share stats (global mean deviation, min mean deviation per household, min mean deviation per nutrient, min overall deviation)
    if hasattr(model, "u"):
        nutrients = sorted(list(model.N), key=str)
        households = sorted(list(model.H), key=str)

        # Fair share per nutrient = mean utility for that nutrient across households
        fair_share: Dict[Any, float] = {}
        for n in nutrients:
            s = 0.0
            c = 0
            for h in households:
                v = pyo.value(model.u[n, h], exception=False)
                if v is None:
                    continue
                s += float(v)
                c += 1
            fair_share[n] = (s / c) if c else 0.0

        deviations: List[float] = []
        house_dev_lists: Dict[Any, List[float]] = {h: [] for h in households}
        nut_dev_lists: Dict[Any, List[float]] = {n: [] for n in nutrients}

        for n in nutrients:
            fs = fair_share[n]
            for h in households:
                v = pyo.value(model.u[n, h], exception=False)
                if v is None:
                    continue
                d = abs(float(v) - fs)
                deviations.append(d)
                house_dev_lists[h].append(d)
                nut_dev_lists[n].append(d)

        global_mean_deviation = sum(deviations) / len(deviations) if deviations else 0.0
        house_mean_devs: List[float] = [
            (sum(lst) / len(lst)) if lst else 0.0 for lst in (house_dev_lists[h] for h in households)
        ]
        nut_mean_devs: List[float] = [
            (sum(lst) / len(lst)) if lst else 0.0 for lst in (nut_dev_lists[n] for n in nutrients)
        ]
        min_mean_dev_household = min(house_mean_devs) if house_mean_devs else 0.0
        min_mean_dev_nutrient = min(nut_mean_devs) if nut_mean_devs else 0.0
        min_overall_deviation = min(deviations) if deviations else 0.0
    else:
        global_mean_deviation = 0.0
        min_mean_dev_household = 0.0
        min_mean_dev_nutrient = 0.0
        min_overall_deviation = 0.0

    metrics["global_mean_deviation_from_fair_share"] = global_mean_deviation
    metrics["min_mean_deviation_per_household"] = min_mean_dev_household
    metrics["min_mean_deviation_per_nutrient"] = min_mean_dev_nutrient
    metrics["min_overall_deviation_from_fair_share"] = min_overall_deviation

'''

