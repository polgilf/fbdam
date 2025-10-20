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
└── runs/                     # Scenario run outputs grouped by dataset/config
```

The CLI entry point lives in `src/fbdam/run.py`, while
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

2. Run the pipeline by referencing a scenario identifier:

   ```bash
   python -m fbdam.run --scenario scenario-a1
   ```

   Override solver behaviour using `--time-limit`, `--mip-gap`, or `--threads`
   at the command line. Artifacts are organised under `runs/{dataset}/{config}/{run_id}/`.

## Handling infeasible solutions

Sometimes the configured dials or budgets make the optimisation problem
infeasible. FBDAM keeps the pipeline running so you can analyse the run:

- The CLI emits a yellow warning panel summarising the solver termination
  condition and pointing to saved artifacts.
- `report.md` highlights the infeasibility, suppresses KPIs, and lists
  troubleshooting ideas.
- `solver_report.json`, `solver.log`, and (when enabled) `model.mps` provide
  low-level diagnostics for deeper analysis.

Try `scenarios/demo_infeasible.yaml` to generate an intentionally infeasible
run that exercises the new diagnostics.

### End-to-end demo using `params.yaml`

The repository also ships with `scenarios/demo-tnu.yaml`, an end-to-end baseline
that loads every CSV under `data/demo/` plus the dial configuration in
`data/demo/params.yaml`. The parameter file relaxes every fairness dial and
sets the budget and lambda penalty to zero, so the run focuses solely on
maximizing total nutrient utility (TNU).

Execute it with:

```bash
python -m fbdam.run --scenario scenario-a2 --time-limit 30 --mip-gap 0.0
```

This creates a timestamped folder inside `runs/ds-a/alpha-0.6/` containing the
atom snapshot, metrics, solver log, and QA figures. The repository includes
fixtures under `runs/` produced by `tools/run_matrix.py` for quick inspection.

## Programmatic usage

You can embed FBDAM in other Python tooling without using the CLI:

```python
from pathlib import Path
from fbdam import build_model, solve_model, write_report
from fbdam.utils import build_run_dir

domain = ...  # DomainIndex from CSVs or constructed in memory
config = {...}  # Matches the config schema consumed by build_model
model = build_model(domain, config)
results = solve_model(model, solver_name="appsi_highs", options={"time_limit": 10})
write_report(
    model=model,
    domain=domain,
    solver_report=results,
    run_dir=build_run_dir("demo", "alpha", "example"),
    dataset_id="demo",
    config_id="alpha",
    scenario_id="demo-scenario",
    run_id="example",
    seed=1,
    effective_solver={"time_limit_s": 10, "mip_gap": 0.0, "threads": "auto"},
    dials={"alpha_i": 0.5, "beta_h": 0.3, "gamma_n": 0.9, "omega_h": 0.7},
    constraint_ids=["base_balance"],
    dataset_metadata={},
    scenario_filters={},
)
```

The `fbdam.engine.domain` module contains the typed entities used in the model
tests (`tests/test_paths_and_model.py`) if you need to construct scenarios in
memory.

## Testing

Run the automated suite to verify the build → solve → report flow and CLI wiring:

```bash
pytest
```

## Further reading

- `guides/FBDAM-model-builder-guide.md` — high-level modeling overview
- `guides/io-utilization-and-validation.md` — configuration and data validation
- `guides/fbdam-reporting-guide.md` — reporting internals and artifact details

## License

Released under the MIT License. See `pyproject.toml` for authorship details.
