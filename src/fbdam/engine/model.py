from __future__ import annotations

from typing import Iterable, Mapping

import pyomo.environ as pyo

from fbdam.constraints import constraint_catalog
from fbdam.engine.domain import DomainIndex


class ModelConfigurationError(ValueError):
    """Raised when the model configuration is invalid."""


def _require_dial(params: Mapping[str, object], name: str) -> float:
    try:
        value = params[name]
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise ModelConfigurationError(f"Missing dial '{name}' in configuration") from exc
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive guard
        raise ModelConfigurationError(f"Dial '{name}' must be numeric (got {value!r})") from exc
    if not 0.0 <= numeric <= 1.0:
        raise ModelConfigurationError(
            f"Dial '{name}' must be within [0, 1] (got {numeric})"
        )
    return numeric


def _validate_configuration(domain: DomainIndex, params: Mapping[str, object]) -> None:
    if "model" not in params:
        raise ModelConfigurationError("Configuration missing 'model' section")

    model_section = params["model"]
    if not isinstance(model_section, Mapping):
        raise ModelConfigurationError("'model' section must be a mapping")

    structure = model_section.get("structure")
    if not isinstance(structure, Mapping):
        raise ModelConfigurationError("model.structure must be a mapping")

    constraints = structure.get("constraints")
    if not isinstance(constraints, Iterable):
        raise ModelConfigurationError("model.structure.constraints must be iterable")

    unknown: list[str] = []
    for cname in constraints:
        if cname not in constraint_catalog:
            unknown.append(str(cname))
    if unknown:
        raise ModelConfigurationError(
            "Unknown constraint id(s): " + ", ".join(sorted(unknown))
        )

    dials = model_section.get("dials")
    if not isinstance(dials, Mapping):
        raise ModelConfigurationError("model.dials must be a mapping")

    # enforce required dials exist and fall within [0, 1]
    for dial_name in ("alpha_i", "beta_h", "gamma_n", "omega_h"):
        _require_dial(dials, dial_name)

    if "objective" not in model_section:
        raise ModelConfigurationError("model.objective must be specified")

    if not domain.items or not domain.households or not domain.nutrients:
        raise ModelConfigurationError("Domain must contain items, households, and nutrients")


def add_core_sets_params_vars(
    model: pyo.ConcreteModel, domain: DomainIndex, params: Mapping[str, object]
) -> None:
    model.I = pyo.Set(initialize=sorted(domain.items.keys()))
    model.H = pyo.Set(initialize=sorted(domain.households.keys()))
    model.N = pyo.Set(initialize=sorted(domain.nutrients.keys()))

    stocks = {i: domain.items[i].stock for i in model.I}
    model.S = pyo.Param(model.I, initialize=stocks, mutable=False)

    requirement_data = {
        (h, n): domain.requirements.get((h, n), None) for h in model.H for n in model.N
    }
    req_map = {
        key: (val.amount if val is not None else 0.0) for key, val in requirement_data.items()
    }
    model.R = pyo.Param(model.H, model.N, initialize=req_map, mutable=False)
    household_totals = {
        h: sum(req_map[(h, n)] for n in model.N) for h in model.H
    }
    model.HouseholdRequirementTotal = pyo.Param(model.H, initialize=household_totals, mutable=False)

    nutrient_content = {}
    for i in model.I:
        for n in model.N:
            nutrient_content[(i, n)] = domain.item_nutrients.get((i, n), None)
    model.A = pyo.Param(
        model.I,
        model.N,
        initialize={
            (i, n): (nutrient_content[(i, n)].qty_per_unit if nutrient_content[(i, n)] else 0.0)
            for i in model.I
            for n in model.N
        },
        mutable=False,
    )

    # Household reference weights (used for Hoover index); fallback to 1.0
    weights = {h: float(domain.households[h].fairshare_weight or 1.0) for h in model.H}
    model.HouseholdWeight = pyo.Param(model.H, initialize=weights, mutable=False)
    total_weight = sum(weights.values())
    if total_weight <= 0:
        share_value = 1.0 / max(len(weights), 1)
        shares = {h: share_value for h in model.H}
    else:
        shares = {h: weights[h] / total_weight for h in model.H}
    model.HouseholdWeightShare = pyo.Param(model.H, initialize=shares, mutable=False)

    model.x = pyo.Var(model.I, model.H, domain=pyo.NonNegativeReals)
    model.s = pyo.Var(model.H, bounds=(0, 1))

    def _q_rule(m: pyo.ConcreteModel, n: str, h: str) -> pyo.Expression:
        return sum(m.A[i, n] * m.x[i, h] for i in m.I)

    model.q = pyo.Expression(model.N, model.H, rule=_q_rule)

    model.total_supply = pyo.Expression(rule=lambda m: sum(m.S[i] for i in m.I))
    model.total_requirement = pyo.Expression(
        rule=lambda m: sum(m.R[h, n] for h in m.H for n in m.N)
    )
    model.total_nutrient_utility = pyo.Expression(
        rule=lambda m: sum(m.q[n, h] for n in m.N for h in m.H)
    )
    model.household_allocation = pyo.Expression(
        model.H, rule=lambda m, h: sum(m.x[i, h] for i in m.I)
    )
    model.total_household_weight = pyo.Expression(
        rule=lambda m: sum(m.HouseholdWeight[h] for h in m.H)
    )

    model.model_params = params


def add_objective(model: pyo.ConcreteModel, objective_name: str, params: Mapping[str, object]) -> None:
    if objective_name != "maximize_TNU":
        raise ModelConfigurationError(f"Unsupported objective '{objective_name}'")

    model.OBJ = pyo.Objective(expr=model.total_nutrient_utility, sense=pyo.maximize)


def build_model(domain: DomainIndex, params: Mapping[str, object]) -> pyo.ConcreteModel:
    _validate_configuration(domain, params)

    model = pyo.ConcreteModel(name="FBDAM")
    add_core_sets_params_vars(model, domain, params)

    active_constraints = params["model"]["structure"]["constraints"]
    for cname in active_constraints:
        constraint_catalog[cname](model, domain, params)

    add_objective(model, params["model"]["objective"], params)
    return model


__all__ = [
    "ModelConfigurationError",
    "add_core_sets_params_vars",
    "add_objective",
    "build_model",
]
