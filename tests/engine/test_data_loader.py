"""Unit tests for the CSV data loader utilities."""

from pathlib import Path

import pytest

from fbdam.engine.io import load_scenario


ROOT = Path(__file__).resolve().parents[2]


def test_dataset_a_balanced_is_loaded_correctly():
    scenario_path = ROOT / "scenarios" / "ds-a_dials-balanced.yaml"

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
    h1 = domain.households["H1"]
    total_members = sum(h.members for h in domain.households.values())
    assert h1.members == pytest.approx(1.0)
    assert h1.fairshare_weight == pytest.approx(h1.members / total_members)

    # Requirements and item nutrients
    assert domain.requirements[("H2", "prot")].amount == pytest.approx(1200)
    assert domain.item_nutrients[("beans", "prot")].qty_per_unit == pytest.approx(210)

    # Allocation bounds (item, household)
    bounds = domain.bounds[("beans", "H2")]
    assert bounds.lower == pytest.approx(0)
    assert bounds.upper == pytest.approx(9)

    # Model parameters from scenario
    params = cfg.model_params
    assert params["budget"] == pytest.approx(10.0)
    assert params["lambda"] == pytest.approx(0.0)
    assert params["dials"]["alpha"] == pytest.approx(0.5)
    assert params["dials"]["beta"] == pytest.approx(0.5)
    assert len(params["dials"]) == 6
