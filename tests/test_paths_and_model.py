from pathlib import Path

import pyomo.environ as pyo
import pytest

from fbdam.constraints import constraint_catalog
from fbdam.engine.domain import DomainIndex, Household, Item, ItemNutrient, Nutrient, Requirement
from fbdam.engine.model import ModelConfigurationError, build_model
from fbdam.utils import build_run_dir


def test_build_run_dir_creates_hierarchy(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run_dir = build_run_dir("ds", "cfg", "rid")
    assert run_dir.exists()
    assert (tmp_path / "runs" / "ds" / "cfg" / "rid").is_dir()
    assert (run_dir / "logs").is_dir()
    assert (run_dir / "figures").is_dir()


def _domain_fixture() -> DomainIndex:
    items = {
        "item1": Item(item_id="item1", name="Item 1", stock=10.0),
        "item2": Item(item_id="item2", name="Item 2", stock=5.0),
    }
    households = {
        "h1": Household(household_id="h1", name="H1", fairshare_weight=2.0),
        "h2": Household(household_id="h2", name="H2", fairshare_weight=1.0),
    }
    nutrients = {
        "n1": Nutrient(nutrient_id="n1", name="N1"),
    }
    item_nutrients = {
        ("item1", "n1"): ItemNutrient(item_id="item1", nutrient_id="n1", qty_per_unit=3.0),
        ("item2", "n1"): ItemNutrient(item_id="item2", nutrient_id="n1", qty_per_unit=5.0),
    }
    requirements = {
        ("h1", "n1"): Requirement(household_id="h1", nutrient_id="n1", amount=4.0),
        ("h2", "n1"): Requirement(household_id="h2", nutrient_id="n1", amount=3.0),
    }
    return DomainIndex(
        items=items,
        nutrients=nutrients,
        households=households,
        item_nutrients=item_nutrients,
        requirements=requirements,
        bounds={},
    )


def _base_config(constraints):
    return {
        "model": {
            "objective": "maximize_TNU",
            "structure": {"constraints": constraints},
            "dials": {
                "alpha_i": 0.5,
                "beta_h": 0.3,
                "gamma_n": 0.9,
                "omega_h": 0.7,
            },
        }
    }


def test_build_model_applies_catalog():
    domain = _domain_fixture()
    config = _base_config(list(constraint_catalog))
    model = build_model(domain, config)
    assert isinstance(model, pyo.ConcreteModel)
    assert hasattr(model, "BaseBalance")
    assert hasattr(model, "NutrientFloors")
    assert hasattr(model, "ItemEquityCap")
    assert hasattr(model, "HouseholdEquityCap")
    assert hasattr(model, "SatisfactionFloor")


def test_build_model_rejects_unknown_constraint():
    domain = _domain_fixture()
    config = _base_config(["unknown_block"])
    with pytest.raises(ModelConfigurationError):
        build_model(domain, config)


def test_build_model_requires_all_dials():
    domain = _domain_fixture()
    config = _base_config(list(constraint_catalog))
    del config["model"]["dials"]["alpha_i"]
    with pytest.raises(ModelConfigurationError):
        build_model(domain, config)
