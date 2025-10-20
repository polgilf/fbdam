from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import pyomo.environ as pyo

try:
    from pyomo.opt import ProblemFormat  # type: ignore
except ImportError:  # pragma: no cover - fallback for older Pyomo releases
    ProblemFormat = None  # type: ignore

from fbdam.engine.domain import DomainIndex

ArtifactRows = Iterable[Sequence[Any]]


def compute_kpis(
    model: pyo.ConcreteModel,
    domain: DomainIndex | None,
    solver_report: Mapping[str, Any],
) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {}

    # Basic counts
    if domain is not None:
        metrics["items"] = len(domain.items)
        metrics["households"] = len(domain.households)
        metrics["nutrients"] = len(domain.nutrients)

    # Objective value
    solver_section = solver_report.get("solver")
    if isinstance(solver_section, Mapping) and "objective_value" in solver_section:
        metrics["objective_value"] = solver_section["objective_value"]

    # Allocation stats
    total_alloc = 0.0
    alloc_count = 0 # Pairs household items
    if hasattr(model, "x"):
        items = sorted(list(model.I), key=str)
        households = sorted(list(model.H), key=str)
        for i in items:
            for h in households:
                value = pyo.value(model.x[i, h], exception=False)
                if value is None:
                    continue
                total_alloc += float(value)
                alloc_count += 1
    metrics["total_allocation"] = total_alloc
    metrics["avg_allocation_per_pair"] = total_alloc / alloc_count if alloc_count else 0.0

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

    # Round all metrics to 4 decimal places
    for k in metrics:
        if isinstance(metrics[k], float):
            metrics[k] = round(metrics[k], 4)
            
    return {"kpi": metrics}
