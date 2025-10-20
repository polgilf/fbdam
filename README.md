# FBDAM — Food Basket Design and Allocation Model

FBDAM is a minimal yet production-ready optimization pipeline for designing and
allocating food baskets. It combines Pyomo models, YAML-driven configuration,
and a Typer CLI so teams can run end-to-end allocation studies with repeatable
inputs and automatically generated reports.

## Key capabilities

- **Scenario-driven pipeline** – load a YAML scenario, build the Pyomo model,
  solve it with a selected backend, and emit structured reports in one command.
- **Composable catalogs** – reuse vetted objectives and constraints via the
  packaged YAML catalogs under `fbdam.config` and override parameters per
  scenario when needed.
- **Rich reporting artifacts** – collect solver outputs, KPIs, and manifests so
  every run is auditable and easy to hand off.
- **Typed domain layer** – clean dataclasses model items, nutrients, households,
  and requirements before hitting the optimizer.

## Repository layout

```
├── data/demo/                # Sample CSV inputs for experiments and tests
├── guides/                   # Architecture, modeling, and reporting guides
├── src/fbdam/                # Package source (config, engine, CLI)
├── tests/                    # Pytest-based smoke/integration test
└── outputs/example/          # Example run artifacts
```

The Typer CLI entry point lives in `src/fbdam/engine/run.py`, while
`src/fbdam/engine/model.py`, `solver.py`, and `reporting.py` implement the
core build → solve → report workflow.

## Installation

Requirements: Python 3.12+ and a C++ compiler if you plan to build HiGHS from
source.

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
   ```

2. Install FBDAM in editable mode with the HiGHS AppSi extra (default solver):

   ```bash
   pip install -e .[appsi_highs]
   ```

   Use `[highs]` if you prefer the classic command-line HiGHS interface.

After installation, the `fbdam` console script is available on your PATH.

## Running a scenario

1. Prepare a YAML scenario referencing your data and the built-in catalogs.
   Save it anywhere you like (e.g., `scenarios/demo-balanced.yaml`). A minimal
   example targeting the bundled demo CSVs looks like:

   ```yaml
   version: v1.0
   name: Demo balanced allocation
   data:
     items_csv: data/demo/items.csv
     nutrients_csv: data/demo/nutrients.csv
     households_csv: data/demo/households.csv
     requirements_csv: data/demo/requirements.csv
     item_nutrients_csv: data/demo/item_nutrients.csv
     household_item_bounds_csv: data/demo/household_item_bounds.csv
   model:
     dials:
       alpha: 0.25
       beta: 0.15
       gamma: 0.10
       kappa: 0.05
       rho: 0.20
       omega: 0.30
     budget: 1500
     lambda: 0.8
    constraints:
      - ref: nutrition_utility_mapping
      - ref: fairshare_deviation_identity
      - ref: household_equity_aggregate_cap
        override:
          beta: 0.25
     objectives:
       - ref: sum_utility
   solver:
     name: appsi_highs
     options:
       time_limit: 10
   ```

2. Run the pipeline and send outputs to a directory of your choice:

   ```bash
    fbdam run scenarios/demo-balanced.yaml --outputs outputs/demo-run
   ```

   Add `--solver highs` to override the solver at runtime or invoke
   `fbdam version` to print the installed package version.

   All generated artifacts (reports, KPIs, manifest, etc.) are written underneath
`--outputs`. See `outputs/example/` for a reference run.

### End-to-end demo using `params.yaml`

The repository also ships with `scenarios/demo-tnu.yaml`, an end-to-end baseline
that loads every CSV under `data/demo/` plus the dial configuration in
`data/demo/params.yaml`. The parameter file relaxes every fairness dial and
sets the budget and lambda penalty to zero, so the run focuses solely on
maximizing total nutrient utility (TNU).

Execute it with:

```bash
python -m fbdam.engine.run run scenarios/demo-tnu.yaml --outputs outputs/demo-tnu
```

This creates a timestamped folder inside `outputs/demo-tnu/` containing the
manifest, KPIs, solver report, and CSV exports for allocations and variables.
For convenience the repository also includes `outputs/demo-tnu/sample_run/`
as a checked-in reference execution.

## Programmatic usage

You can embed FBDAM in other Python tooling without using the CLI:

```python
from pathlib import Path
from fbdam import build_model, solve_model, write_report

cfg = ...  # Build a config dict or load via fbdam.engine.io.load_scenario
model = build_model(cfg)
results = solve_model(model, solver_name="appsi_highs", options={"time_limit": 10})
write_report(results, Path("outputs/latest"))
```

The `fbdam.engine.domain` module contains the typed entities used in the smoke
test (`tests/test_smoke.py`) if you need to construct scenarios in memory.

## Testing

Run the automated smoke test to verify the full build → solve → report flow:

```bash
pytest
# or
pytest tests/test_smoke.py -vv
```

The test assembles a tiny domain, solves it with HiGHS, and ensures the expected
artifacts are created in a temporary directory.

## Further reading

- `guides/FBDAM-model-builder-guide.md` — high-level modeling overview
- `guides/io-utilization-and-validation.md` — configuration and data validation
- `guides/fbdam-reporting-guide.md` — reporting internals and artifact details

## License

Released under the MIT License. See `pyproject.toml` for authorship details.
