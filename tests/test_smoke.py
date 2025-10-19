"""
test_smoke.py — Minimal integration test for the FBDAM pipeline
----------------------------------------------------------------
This test executes the full flow:

  Domain (in-memory) → build_model() → solve_model() → write_report()

It checks:
  - Model builds correctly (sets, params, vars)
  - Solver runs successfully (feasible solution)
  - Reporting artifacts are created

It does NOT verify numerical correctness — only integration stability.
"""

from pathlib import Path
import tempfile
import pyomo.environ as pyo

from fbdam.engine.domain import (
    Item, Nutrient, Household, Requirement, ItemNutrient, AllocationBounds, DomainIndex
)
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report


def build_minimal_domain() -> DomainIndex:
    """Create a very small in-memory domain instance."""
    items = {
        "rice": Item(item_id="rice", name="Rice", stock=10.0),
        "beans": Item(item_id="beans", name="Beans", stock=8.0),
    }

    nutrients = {
        "prot": Nutrient(nutrient_id="prot", name="Protein"),
    }

    households = {
        "h1": Household(household_id="h1", name="Household 1"),
        "h2": Household(household_id="h2", name="Household 2"),
    }

    # protein content per item
    item_nutrients = {
        ("rice", "prot"): ItemNutrient(item_id="rice", nutrient_id="prot", qty_per_unit=2.0),
        ("beans", "prot"): ItemNutrient(item_id="beans", nutrient_id="prot", qty_per_unit=5.0),
    }

    # requirements per household/nutrient
    requirements = {
        ("h1", "prot"): Requirement(household_id="h1", nutrient_id="prot", amount=6.0),
        ("h2", "prot"): Requirement(household_id="h2", nutrient_id="prot", amount=4.0),
    }

    # bounds on allocations (optional)
    bounds = {
        ("rice", "h1"): AllocationBounds(item_id="rice", household_id="h1", lower=0, upper=10),
        ("beans", "h1"): AllocationBounds(item_id="beans", household_id="h1", lower=0, upper=10),
        ("rice", "h2"): AllocationBounds(item_id="rice", household_id="h2", lower=0, upper=10),
        ("beans", "h2"): AllocationBounds(item_id="beans", household_id="h2", lower=0, upper=10),
    }

    return DomainIndex(
        items=items,
        nutrients=nutrients,
        households=households,
        item_nutrients=item_nutrients,
        requirements=requirements,
        bounds=bounds,
    )


def build_minimal_cfg(domain: DomainIndex) -> dict:
    """Minimal config dict matching the expected structure for build_model()."""
    cfg = {
        "domain": domain,
        "model": {
            "constraints": [
                {"type": "u_link", "params": {}},
            ],
            "objectives": [
                {"name": "sum_utility", "sense": "maximize", "params": {}}
            ]
        },
    }
    return cfg


def test_full_pipeline(tmp_path: Path = None):
    """Run the full FBDAM pipeline and ensure no exceptions occur."""
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())

    # ---- Build domain and config ----
    domain = build_minimal_domain()
    cfg = build_minimal_cfg(domain)

    # ---- Build model ----
    m = build_model(cfg)
    assert isinstance(m, pyo.ConcreteModel)
    assert len(list(m.I)) > 0 and len(list(m.H)) > 0

    # ---- Solve ----
    results = solve_model(m, solver_name="appsi_highs", options={"time_limit": 5})
    assert "status" in results
    print("\n[SMOKE] Solver results:", results)

    # ---- Report ----
    run_dir = tmp_path / "fbdam_smoke_run"
    manifest = write_report(
        model=m,
        solver_results=results,
        domain=domain,
        cfg_snapshot={"note": "smoke test cfg"},
        run_dir=run_dir,
        include_constraints_activity=False,
    )

    # ---- Assertions ----
    assert run_dir.exists()
    artifacts = {a["path"] for a in manifest.get("artifacts", [])}
    expected = {
        "config_snapshot.yaml",
        "solver_report.json",
        "model_stats.json",
        "kpis.json",
        "variables.parquet",
        "solution.csv",
        "report.md",
        "manifest.json",
    }
    assert expected.issubset(artifacts)
    print(f"\n[SMOKE] Artifacts written to: {run_dir.resolve()}")

    # ---- Read back minimal KPI check ----
    import json
    kpi_path = run_dir / "kpis.json"
    with open(kpi_path, "r", encoding="utf-8") as f:
        kpis = json.load(f)
    assert "kpi" in kpis
    print("\n[SMOKE] KPIs:", kpis["kpi"])


if __name__ == "__main__":
    test_full_pipeline()
    print("\n✅ FBDAM smoke test completed successfully.")
