from __future__ import annotations

from typing import Mapping

import pyomo.environ as pyo

from fbdam.engine.domain import DomainIndex


def _get_dials(params: Mapping[str, object]) -> Mapping[str, float]:
    model_section = params.get("model", {})
    dials = model_section.get("dials", {}) if isinstance(model_section, Mapping) else {}
    if not isinstance(dials, Mapping):  # pragma: no cover - defensive guard
        raise ValueError("model.dials must be a mapping")
    return dials  # type: ignore[return-value]


def add_base_balance(model: pyo.ConcreteModel, domain: DomainIndex, params: Mapping[str, object]) -> None:
    def _rule(m: pyo.ConcreteModel, i: str) -> pyo.Constraint:
        return sum(m.x[i, h] for h in m.H) <= m.S[i]

    model.BaseBalance = pyo.Constraint(model.I, rule=_rule)


def add_nutrient_floors(
    model: pyo.ConcreteModel, domain: DomainIndex, params: Mapping[str, object]
) -> None:
    gamma = float(_get_dials(params)["gamma_n"])

    def _rule(m: pyo.ConcreteModel, n: str, h: str) -> pyo.Constraint | pyo.Constraint.Skip:
        req = float(m.R[h, n])
        if req <= 0:
            return pyo.Constraint.Skip
        return m.q[n, h] >= gamma * req

    model.NutrientFloors = pyo.Constraint(model.N, model.H, rule=_rule)


def add_equity_dials_item(
    model: pyo.ConcreteModel, domain: DomainIndex, params: Mapping[str, object]
) -> None:
    alpha = float(_get_dials(params)["alpha_i"])

    def _rule(m: pyo.ConcreteModel, i: str, h: str) -> pyo.Constraint:
        return m.x[i, h] <= alpha * m.S[i]

    model.ItemEquityCap = pyo.Constraint(model.I, model.H, rule=_rule)


def add_equity_dials_household(
    model: pyo.ConcreteModel, domain: DomainIndex, params: Mapping[str, object]
) -> None:
    beta = float(_get_dials(params)["beta_h"])

    def _rule(m: pyo.ConcreteModel, h: str) -> pyo.Constraint:
        share = m.HouseholdWeightShare[h]
        return m.household_allocation[h] <= beta * share * m.total_supply

    model.HouseholdEquityCap = pyo.Constraint(model.H, rule=_rule)


def add_nutritional_dials(
    model: pyo.ConcreteModel, domain: DomainIndex, params: Mapping[str, object]
) -> None:
    omega = float(_get_dials(params)["omega_h"])

    def _ratio_rule(m: pyo.ConcreteModel, n: str, h: str) -> pyo.Constraint | pyo.Constraint.Skip:
        req = float(m.R[h, n])
        if req <= 0:
            return pyo.Constraint.Skip
        return m.s[h] <= m.q[n, h] / req

    model.SatisfactionLink = pyo.Constraint(model.N, model.H, rule=_ratio_rule)

    def _floor_rule(m: pyo.ConcreteModel, h: str) -> pyo.Constraint:
        total_req = float(m.HouseholdRequirementTotal[h])
        if total_req <= 0:
            return m.s[h] >= 0
        return sum(m.q[n, h] for n in m.N) >= omega * total_req

    model.SatisfactionFloor = pyo.Constraint(model.H, rule=_floor_rule)


constraint_catalog = {
    "base_balance": add_base_balance,
    "nutrient_floors": add_nutrient_floors,
    "equity_dials_item": add_equity_dials_item,
    "equity_dials_household": add_equity_dials_household,
    "nutritional_dials": add_nutritional_dials,
}


__all__ = [
    "constraint_catalog",
    "add_base_balance",
    "add_nutrient_floors",
    "add_equity_dials_item",
    "add_equity_dials_household",
    "add_nutritional_dials",
]
