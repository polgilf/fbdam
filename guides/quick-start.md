# Quick-start: running FBDAM experiments

This guide demonstrates the new experiment layout and shows how to launch
single or batched runs that combine datasets, model configurations, and
execution profiles.

## Directory layout refresher

Each run now lives under `runs/<dataset_id>/<config_id>/<run_id>/`. The
`run_id` is a timestamped slug (e.g. `ds-a_alpha-0-4_20250101T120000Z`).  Each
run directory contains the solver manifest, `run_params.yaml`, `atom.yaml`,
`metrics.json`, the solver log, and the report artifacts produced by the
pipeline.

Datasets live under `data/<dataset_id>/` and model configurations under
`configs/<config_id>.yaml`.  Scenarios in `scenarios/` simply pair a dataset
and a model config.

## Running the four example experiments as a batch

The repository includes two datasets (`ds-a`, `ds-b`) and two model
configurations (`alpha-0.4`, `alpha-0.6`).  Combine them with the two provided
execution profiles to produce the eight reference runs:

```bash
# From the repository root
for scenario in \
  scenarios/ds-a_alpha-0.4.yaml \
  scenarios/ds-a_alpha-0.6.yaml \
  scenarios/ds-b_alpha-0.4.yaml \
  scenarios/ds-b_alpha-0.6.yaml
  do
    python -m fbdam.engine.run run "$scenario" --profile time-limited
    python -m fbdam.engine.run run "$scenario" --profile gap-limited
  done
```

Each invocation writes a run directory under `runs/<dataset>/<config>/` and
logs the profile used in `run_params.yaml` and `atom.yaml`.

## Running a single experiment

To run one dataset–config–profile combination, call the CLI with the scenario
and execution profile you want. For example, to solve Dataset B with the
`alpha-0.6` model using the gap-oriented profile:

```bash
python -m fbdam.engine.run run scenarios/ds-b_alpha-0.6.yaml --profile gap-limited
```

The CLI accepts an optional `--outputs` flag if you want to place the `runs/`
tree somewhere else, and `--run-id` when you need to control the run name
explicitly.

Refer to the generated `run_params.yaml` file for a machine-readable snapshot
of the dataset, model configuration, solver options, and execution profile
used for each run.
