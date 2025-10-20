from __future__ import annotations

import pyomo.environ as pyo
import pytest

from fbdam.engine.model import build_model
from fbdam.engine.domain import (
    AllocationBounds,
    DomainIndex,
    Household,
    Item,
    ItemNutrient,
    Nutrient,
    Requirement,
)


def _make_domain() -> DomainIndex:
    items = {
        "rice": Item(item_id="rice", name="Rice", stock=10.0, cost=2.5),
        "beans": Item(item_id="beans", name="Beans", stock=5.0, cost=3.0),
    }
    nutrients = {
        "protein": Nutrient(nutrient_id="protein", name="Protein"),
    }
    households = {
        "h1": Household(household_id="h1", name="H1", fairshare_weight=0.6),
        "h2": Household(household_id="h2", name="H2", fairshare_weight=0.4),
    }
    item_nutrients = {
        ("rice", "protein"): ItemNutrient(item_id="rice", nutrient_id="protein", qty_per_unit=2.0),
        ("beans", "protein"): ItemNutrient(item_id="beans", nutrient_id="protein", qty_per_unit=4.0),
    }
    requirements = {
        ("h1", "protein"): Requirement(household_id="h1", nutrient_id="protein", amount=5.0),
        ("h2", "protein"): Requirement(household_id="h2", nutrient_id="protein", amount=3.0),
    }
    bounds: dict[tuple[str, str], AllocationBounds] = {}
    return DomainIndex(
        items=items,
        nutrients=nutrients,
        households=households,
        item_nutrients=item_nutrients,
        requirements=requirements,
        bounds=bounds,
    )


def _make_config() -> dict:
    domain = _make_domain()
    model_params = {
        "dials": {
            "alpha": 0.25,
            "beta": 0.15,
            "rho": 0.2,
            "gamma": 0.1,
            "kappa": 0.05,
            "omega": 0.3,
        },
        "budget": 100.0,
        "lambda": 1.5,
    }
    constraint_ids = [
        "item_supply_limit",
        "purchase_budget_limit",
        "nutrition_utility_mapping",
        "household_adequacy_floor",
        "nutrient_adequacy_floor",
        "pairwise_adequacy_floor",
        "fairshare_deviation_identity",
        "item_equity_aggregate_cap",
        "household_equity_aggregate_cap",
        "pairwise_equity_cap",
    ]
    constraints = [{"id": name, "params": {}} for name in constraint_ids]
    objectives = [{"name": "sum_utility", "sense": "maximize", "params": {}}]
    return {
        "domain": domain,
        "model_params": model_params,
        "model": {
            "constraints": constraints,
            "objectives": objectives,
        },
    }


def test_backbone_components_evaluate() -> None:
    cfg = _make_config()
    model = build_model(cfg)

    # Basic components exist
    assert hasattr(model, "y")
    assert hasattr(model, "epsilon")
    assert hasattr(model, "Avail")
    assert hasattr(model, "TotSupply")
    assert hasattr(model, "mean_utility_nutrient")

    items = sorted(model.I)
    households = sorted(model.H)
    nutrients = sorted(model.N)

    item = items[0]
    nutrient = nutrients[0]
    household = households[0]
    other_household = households[1]

    for i in model.I:
        model.y[i].set_value(0.0)
        for h in model.H:
            model.x[i, h].set_value(0.0)
            model.dpos[i, h].set_value(0.0)
            model.dneg[i, h].set_value(0.0)

    model.y[item].set_value(2.0)
    model.x[item, household].set_value(3.0)
    model.dpos[item, household].set_value(0.5)
    model.dneg[item, household].set_value(0.25)
    model.u[nutrient, household].set_value(0.6)
    model.u[nutrient, other_household].set_value(0.4)
    model.epsilon.set_value(0.1)

    avail_value = pyo.value(model.Avail[item])
    assert pytest.approx(avail_value) == model.S[item] + model.y[item].value

    total_supply = pyo.value(model.TotSupply)
    manual_total = sum(model.S[i] + model.y[i].value for i in model.I)
    assert pytest.approx(total_supply) == manual_total

    household_total = pyo.value(model.X[household])
    manual_household = sum(model.x[i, household].value for i in model.I)
    assert pytest.approx(household_total) == manual_household

    mean_nutrient = pyo.value(model.mean_utility_nutrient[nutrient])
    expected_mean = sum(model.u[nutrient, h].value for h in model.H) / len(model.H)
    assert pytest.approx(mean_nutrient) == expected_mean

    global_mean = pyo.value(model.global_mean_utility)
    total_u = sum(model.u[nutrient, h].value for h in model.H)
    assert pytest.approx(global_mean) == total_u / (len(model.N) * len(model.H))

    # Objective should include lambda penalty
    obj_value = pyo.value(model.OBJ.expr)
    expected_obj = total_u - cfg["model_params"]["lambda"] * model.epsilon.value
    assert pytest.approx(obj_value) == expected_obj

    # Constraints use dial values
    item_cap = model.DeviationItemCap[item]
    expected_item_rhs = cfg["model_params"]["dials"]["alpha"] * avail_value
    item_cap_body = pyo.value(item_cap.body)
    lhs_item = sum(model.dpos[item, h].value + model.dneg[item, h].value for h in model.H)
    assert item_cap_body == pytest.approx(lhs_item - expected_item_rhs)

    household_cap = model.DeviationHouseholdCap[household]
    expected_household_rhs = cfg["model_params"]["dials"]["beta"] * total_supply
    household_cap_body = pyo.value(household_cap.body)
    lhs_household = sum(model.dpos[i, household].value + model.dneg[i, household].value for i in model.I)
    assert household_cap_body == pytest.approx(lhs_household - expected_household_rhs)

    pair_cap = model.DeviationPairCap[item, household]
    rho = cfg["model_params"]["dials"]["rho"]
    pair_cap_body = pyo.value(pair_cap.body)
    lhs_pair = model.dpos[item, household].value + model.dneg[item, household].value
    assert pair_cap_body == pytest.approx(lhs_pair - rho * avail_value)

    hh_floor = model.HouseholdFloor[household]
    omega = cfg["model_params"]["dials"]["omega"]
    hh_mean = pyo.value(model.mean_utility[household])
    body_hh = pyo.value(hh_floor.body)
    assert body_hh == pytest.approx(
        -model.epsilon.value - (hh_mean - omega * global_mean)
    )

    nutrient_floor = model.NutrientFloor[nutrient]
    gamma = cfg["model_params"]["dials"]["gamma"]
    nutrient_mean = pyo.value(model.mean_utility_nutrient[nutrient])
    body_nutrient = pyo.value(nutrient_floor.body)
    assert body_nutrient == pytest.approx(
        -model.epsilon.value - (nutrient_mean - gamma * global_mean)
    )

    pair_floor = model.PairFloor[nutrient, household]
    kappa = cfg["model_params"]["dials"]["kappa"]
    pair_body = pyo.value(pair_floor.body)
    assert pair_body == pytest.approx(
        -model.epsilon.value - (model.u[nutrient, household].value - kappa * global_mean)
    )


def test_purchases_disabled_without_budget_constraint() -> None:
    domain = _make_domain()
    cfg = {
        "domain": domain,
        "model_params": {"dials": {}},
        "model": {
            "constraints": [
                {"id": "item_supply_limit", "params": {}},
                {"id": "nutrition_utility_mapping", "params": {}},
            ],
            "objectives": [
                {"name": "sum_utility", "sense": "maximize", "params": {}},
            ],
        },
    }

    model = build_model(cfg)

    assert not model.allow_purchases
    for var in model.y.values():
        assert var.fixed
        assert pytest.approx(var.value or 0.0) == 0.0

    for item in model.I:
        assert pytest.approx(pyo.value(model.Avail[item])) == model.S[item]
