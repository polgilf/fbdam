"""Unit tests for the CSV data loader utilities."""

from pathlib import Path

import pytest

from fbdam.engine.io import load_scenario


ROOT = Path(__file__).resolve().parents[2]


def test_dataset_a_alpha_04_is_loaded_correctly():
    scenario_path = ROOT / "scenarios" / "ds-a_alpha-0.4.yaml"

    cfg = load_scenario(scenario_path)
    domain = cfg.domain

    # Items
    assert set(domain.items) == {"rice", "beans", "lentils"}
    assert domain.items["rice"].stock == pytest.approx(40.0)
    assert domain.items["beans"].cost == pytest.approx(1.5)

    # Nutrients
    assert set(domain.nutrients) == {"cal", "prot"}

    # Households and weights
    assert set(domain.households) == {"H1", "H2"}
    assert domain.households["H1"].fairshare_weight == pytest.approx(0.6)

    # Requirements and item nutrients
    assert domain.requirements[("H1", "prot")].amount == pytest.approx(50)
    assert domain.item_nutrients[("lentils", "prot")].qty_per_unit == pytest.approx(12)

    # Allocation bounds (item, household)
    bounds = domain.bounds[("beans", "H2")]
    assert bounds.lower == pytest.approx(0)
    assert bounds.upper == pytest.approx(15)

    # Model parameters from scenario
    params = cfg.model_params
    assert params["budget"] == pytest.approx(120.0)
    assert params["lambda"] == pytest.approx(0.5)
    assert params["dials"]["alpha"] == pytest.approx(0.4)
    assert params["dials"]["beta"] == pytest.approx(0.5)
    assert len(params["dials"]) == 6
