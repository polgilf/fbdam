Excellent question — this `io.py` module is designed to be  **self-contained and testable** .

Here’s exactly how to **use and validate** it step by step.

---

## 🧩 1️⃣ Prerequisites

Make sure your environment is set up properly:

```bash
pip install -e .[appsi_highs]
```

and that your repo layout looks like this:

```
src/
  fbdam/
    engine/io.py
    config/catalogs/constraints_v1.1.yaml
    config/catalogs/objectives_v1.0.yaml
```

> Those two YAML catalogs must exist, even if they’re empty or contain dummy data.

---

## 🧪 2️⃣ Minimal validation setup

### A. Create a **toy scenario YAML**

Save this in `config/scenarios/demo-balanced.yaml` (or anywhere):

```yaml
version: v1.0
status: draft
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
      override: {}
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

---

### B. Create **dummy catalogs**

Under `src/fbdam/config/catalogs/constraints_v1.1.yaml`:

```yaml
version: v1.0
status: draft
constraints:
  - id: nutrition_utility_mapping
    params: {}
```

And under `src/fbdam/config/catalogs/objectives_v1.0.yaml`:

```yaml
version: v1.0
status: draft
objectives:
  - id: sum_utility
    name: sum_utility
    sense: maximize
    params: {}
```

> These are minimal — just enough for the loader to resolve references.

---

## 🧰 3️⃣ Quick interactive validation

Start a Python shell in your venv (from the repo root):

```bash
python
```

Then:

```python
from pathlib import Path
from fbdam.engine.io import load_scenario

cfg = load_scenario(Path("config/scenarios/demo-balanced.yaml"))
print(cfg)
```

Expected output (simplified):

```
ScenarioConfig(
  data_paths={
    'household_item_bounds_csv': PosixPath('/.../data/demo/household_item_bounds.csv'),
    'households_csv': PosixPath('/.../data/demo/households.csv'),
    'item_nutrients_csv': PosixPath('/.../data/demo/item_nutrients.csv'),
    'items_csv': PosixPath('/.../data/demo/items.csv'),
    'nutrients_csv': PosixPath('/.../data/demo/nutrients.csv'),
    'requirements_csv': PosixPath('/.../data/demo/requirements.csv')
  },
  constraints=[
    MaterializedConstraint(id='nutrition_utility_mapping', params={}),
    MaterializedConstraint(id='household_equity_aggregate_cap', params={'beta': 0.25})
  ],
  objectives=[MaterializedObjective(id='sum_utility', name='sum_utility', sense='maximize', params={})],
  solver=SolverConfig(name='appsi_highs', options={'time_limit': 10}),
  raw=...
)
```

If a required file doesn’t exist, it will raise:

```
IOConfigError: demo-balanced.yaml::data.items_csv: file not found -> /path/to/data/demo/items.csv
```

That’s good — it means validation works.

You can touch empty files to silence this:

```bash
mkdir -p data/demo
touch \
  data/demo/items.csv \
  data/demo/nutrients.csv \
  data/demo/households.csv \
  data/demo/requirements.csv \
  data/demo/item_nutrients.csv \
  data/demo/household_item_bounds.csv
```

Then rerun — now it should succeed.

---

## 🧾 4️⃣ Minimal smoke test (automated)

You can make a quick test file in `tests/test_io_smoke.py`:

```python
from pathlib import Path
from fbdam.engine.io import load_scenario, ScenarioConfig

def test_io_loader_minimal(tmp_path):
    # Prepare dummy files
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "items.csv").write_text(
        "item_id,name,unit,stock,cost\nI1,Rice,kg,10,1.5\n"
    )
    (data_dir / "nutrients.csv").write_text(
        "nutrient_id,name,unit\nN1,Protein,g\n"
    )
    (data_dir / "households.csv").write_text(
        "household_id,name,fairshare_weight\nH1,Demo household,1.0\n"
    )
    (data_dir / "requirements.csv").write_text(
        "household_id,nutrient_id,requirement\nH1,N1,5\n"
    )
    (data_dir / "item_nutrients.csv").write_text(
        "item_id,nutrient_id,qty_per_unit\nI1,N1,10\n"
    )
    (data_dir / "household_item_bounds.csv").write_text(
        "household_id,item_id,lower,upper\nH1,I1,0,10\n"
    )

    # Create dummy scenario YAML
    scenario_path = tmp_path / "scenario.yaml"
    scenario_path.write_text(f"""
version: v1.0
status: draft
data:
  items_csv: {data_dir}/items.csv
  nutrients_csv: {data_dir}/nutrients.csv
  households_csv: {data_dir}/households.csv
  requirements_csv: {data_dir}/requirements.csv
  item_nutrients_csv: {data_dir}/item_nutrients.csv
  household_item_bounds_csv: {data_dir}/household_item_bounds.csv
model:
  constraints:
    - ref: nutrition_utility_mapping
  objectives:
    - ref: sum_utility
solver:
  name: appsi_highs
""")

    cfg = load_scenario(scenario_path)
    assert isinstance(cfg, ScenarioConfig)
    assert cfg.solver.name == "appsi_highs"
    assert cfg.constraints[0].id == "nutrition_utility_mapping"
```

Run it:

```bash
pytest -v
```

If everything is correct, you’ll see:

```
tests/test_io_smoke.py::test_io_loader_minimal PASSED
```

---

## ✅ 5️⃣ Interpreting the output

After calling `load_scenario()`, you’ll have a structured object:

```python
cfg.data_paths         # normalized CSV Paths
cfg.constraints        # list[MaterializedConstraint]
cfg.objectives         # list[MaterializedObjective]
cfg.solver.name        # e.g., "appsi_highs"
cfg.solver.options     # dict of solver options
cfg.raw                # dictionary ready for JSON serialization
```

You can then pass `cfg` to your model builder:

```python
from fbdam.engine.model import build_model
model = build_model(cfg)
```

---

### ✅ TL;DR — Quick command-line check

```bash
python -c "from fbdam.engine.io import load_scenario; from pathlib import Path; print(load_scenario(Path('config/scenarios/demo-balanced.yaml')))"
```

If it prints a `ScenarioConfig` object without errors → everything works.

---

Would you like me to show the next file to implement (`domain.py` with headers and dataclasses)?

That’s the next logical step after validating `io.py`.
