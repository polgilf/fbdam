# FBDAM · Reporting Guide

This guide explains how to generate, store, and consume run artifacts with the `reporting.py` module.
It covers **what is produced**, **where it lives**, **how to use it from code/CLI**, and **how to parse it** later.

---

## 1) What the reporting produces (artifacts layout)

Each run creates a dedicated folder under `outputs/runs/{run_id}/` with the following files:

```
outputs/
└─ runs/
   └─ {run_id}/
      ├─ manifest.json            # index of artifacts + checksums
      ├─ config_snapshot.json     # scenario snapshot (optional)
      ├─ solver_report.json       # solver status, termination, gap, obj...
      ├─ model_stats.json         # variables/constraints counts
      ├─ kpis.json                # KPIs for business/reporting
      ├─ variables.csv            # normalized view of all decision variables
      ├─ constraints.csv          # (optional) constraint activity/slack
      ├─ solution.csv             # lean extract of x[i,h]
      └─ report.md                # markdown summary
```

---

## 2) How to trigger reporting from code

```python
from pathlib import Path
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report

# Build & solve (cfg contains "domain" and "model" sections)
m = build_model(cfg)
res = solve_model(m, solver_name="appsi_highs", options={"time_limit": 5})

# Choose a run directory (unique ID, e.g., timestamp or ULID)
run_dir = Path("outputs/runs/2025-10-19_demo")

# Write all artifacts
manifest = write_report(
    model=m,
    solver_results=res,
    domain=cfg["domain"],
    cfg_snapshot=cfg,                 # or the expanded scenario object
    run_dir=run_dir,
    include_constraints_activity=False  # set True to export constraint activity
)

print("Artifacts written:", run_dir)
print("Manifest keys:", manifest.keys())
```

### Minimal KPIs
If you don't pass `kpis=...`, `write_report()` computes baseline KPIs:
- `objective_value` — lifted from the solver summary (if available)
- `total_allocation` — sum of all `x[i,h]`
- `avg_allocation_per_pair` — arithmetic mean of allocations
- `mean_utility` — average `u[n,h]`
- `items` / `households` / `nutrients` — counts derived from the domain (when provided)

The returned JSON structure is `{ "kpi": {...} }`, so you can extend/override by
merging your own metrics before calling `write_report`.

---

## 3) CLI quickstart (example)

If your CLI (`run.py`) orchestrates build → solve → report, you can expose a command like:
```
fbdam run config/scenarios/demo-balanced.yaml --outputs outputs/runs/demo
```
Ensure `run.py` calls `write_report(...)` with the right args.

---

## 4) Manifest & integrity

- `manifest.json` is the single source of truth for a run.
- It lists all artifacts with **SHA-256** checksums and echoes the solver summary.
- Never modify runs in place; **each execution** must produce a **new** folder.

Example (excerpt):
```json
{
  "run": {"id": "fbdam-20240212T101010Z", "started_at": "2024-02-12T10:10:10Z"},
  "solver": {"name": "highs", "status": "ok", "elapsed_sec": 0.02},
  "artifacts": [
    {"path": "solver_report.json", "sha256": "...", "kind": "metric"},
    {"path": "variables.csv", "sha256": "...", "kind": "table"}
  ]
}
```

---

## 5) Reading the artifacts later (parsers)

### Load KPIs and solver report (Python)
```python
import json
from pathlib import Path

run_dir = Path("outputs/runs/2025-10-19_demo")

solver = json.loads((run_dir / "solver_report.json").read_text(encoding="utf-8"))
kpis   = json.loads((run_dir / "kpis.json").read_text(encoding="utf-8"))["kpi"]

print("Objective:", solver.get("objective_value"))
print("u_mean:", kpis.get("u_mean"))
```

### Load variables as DataFrame
```python
import pandas as pd
run_dir = Path("outputs/runs/2025-10-19_demo")

df = pd.read_csv(run_dir / "variables.csv")
df.head()
```
The variables table has normalized columns: `var, i, h, n, index_extra, value, lb, ub`.

### Load constraints activity (optional)
```python
import pandas as pd
run_dir = Path("outputs/runs/2025-10-19_demo")

path = run_dir / "constraints.csv"
dfc = pd.read_csv(path) if path.exists() else None
```

---

## 6) KPIs best practices

- Keep names **stable** and **flat** (e.g., `tnu`, `nutrition.min_pairwise_utility`, `allocation_equity.max_household_mean_deviation`, `cost_total`).
- Prefer numeric types; avoid strings except for labels.  
- Record the **units** in a sidecar doc if needed (or the KPI YAML catalog).

---

## 7) Troubleshooting

- **Missing CSVs**: ensure the run directory was created and writing permissions exist.
- **Empty variables table**: confirm the model was solved and variables exist.
- **Missing solver metrics**: some backends don’t expose all fields; the report shows `null`.  
- **Reproducibility**: always ship `config_snapshot.json` (expanded scenario).
- **Integrity**: verify file checksums in `manifest.json`.

---

## 8) Extending reporting

- Add domain-specific KPIs: pass `kpis={...}` to `write_report(...)`.  
- Emit **constraint duals** or **reduced costs** if your solver exposes them.  
- Export to **JSON-LD** by wrapping KPIs with a `@context` if you need ontology alignment.

---

## 9) API reference (key functions)

- `write_report(model=..., solver_results=..., run_dir=..., domain=None, cfg_snapshot=None, include_constraints_activity=False)`
  Generates all artifacts and returns a manifest dict.

- `build_manifest(context, artifacts)` — helper used internally (exposed for testing).
- `write_json(path, obj)` — writes JSON with UTF-8 and indentation.
- `write_markdown_summary(path, solver, kpis, model_stats, title)` — human summary.
- `write_variables_csv(model, path)` — variables table.
- `write_constraints_csv(model, path)` — constraint activity (requires `include_constraints_activity=True`).
- `write_solution_csv(model, path, var_name="x")` — compact extract of the primary decision variable.
- `extract_model_stats(model)` — counts variables/constraints.
- `compute_kpis(model, domain, solver_report)` — baseline KPIs used by the Markdown/JSON outputs.

---

## 10) Minimal end-to-end usage pattern

```python
from pathlib import Path
from fbdam.engine.io import load_scenario  # your loader
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report

cfg = load_scenario(Path("config/scenarios/demo-balanced.yaml"))
m = build_model(cfg)
res = solve_model(m, solver_name="appsi_highs", options={"time_limit": 5})

manifest = write_report(
    model=m,
    solver_results=res,
    domain=cfg["domain"],
    cfg_snapshot=cfg,
    run_dir=Path("outputs/runs/2025-10-19_demo"),
    include_constraints_activity=False
)
print("Done. Manifest:", manifest["run_id"])
```
