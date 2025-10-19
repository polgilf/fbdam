"""Unit tests for the CSV data loader utilities."""

from pathlib import Path

import pytest

from fbdam.engine.io import load_scenario


ROOT = Path(__file__).resolve().parents[2]


def test_demo_domain_is_loaded_correctly():
    scenario_path = ROOT / "scenarios" / "demo-balanced.yaml"

    cfg = load_scenario(scenario_path)
    domain = cfg.domain

    # Items
    assert set(domain.items) == {"rice", "beans", "milk", "apples"}
    assert domain.items["rice"].stock == pytest.approx(20.0)
    assert domain.items["beans"].cost == pytest.approx(1.2)

    # Nutrients
    assert set(domain.nutrients) == {"cal", "prot", "calc"}

    # Households and weights
    assert set(domain.households) == {"H1", "H2", "H3"}
    assert domain.households["H2"].fairshare_weight == pytest.approx(0.333333333)

    # Requirements and item nutrients
    assert domain.requirements[("H3", "prot")].amount == pytest.approx(220)
    assert domain.item_nutrients[("beans", "prot")].qty_per_unit == pytest.approx(210)

    # Allocation bounds (item, household)
    bounds = domain.bounds[("rice", "H1")]
    assert bounds.lower == pytest.approx(0)
    assert bounds.upper == pytest.approx(3)

    # Model parameters from scenario
    params = cfg.model_params
    assert params["budget"] == pytest.approx(1500.0)
    assert params["lambda"] == pytest.approx(0.8)
    assert params["dials"]["alpha"] == pytest.approx(0.25)
    assert len(params["dials"]) == 6
