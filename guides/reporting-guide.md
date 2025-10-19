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
      ├─ manifest.json               # index of artifacts + checksums
      ├─ config_snapshot.yaml        # scenario snapshot (expanded)
      ├─ domain_snapshot.json        # counts of I/N/H, bounds, requirements...
      ├─ solver_report.json          # solver status, termination, gap, obj...
      ├─ model_stats.json            # variables/constraints counts
      ├─ kpis.json                   # KPIs for business/reporting
      ├─ variables.parquet           # long table of all variables (Parquet) *
      ├─ constraints_activity.parquet# activity/slacks by constraint (optional) *
      ├─ variables.csv               # CSV fallback if Parquet not available
      ├─ constraints_activity.csv    # CSV fallback (optional)
      ├─ solution.csv                # human-oriented extract (x[i,h], totals)
      ├─ report.md                   # markdown summary
      ├─ run.log                     # human-readable log
      └─ run.ndjson                  # structured JSONL log
```
\* Uses `pyarrow` for Parquet; if not installed, CSV fallback is written.

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
If you don't pass `kpis=...`, `write_report()` will compute minimal KPIs:
- `kpi.tnu` (total sum of u[n,h])  
- `kpi.u_min` (minimum utility)  
- `kpi.u_mean` (mean utility)

You can pass your own KPIs dict to override/extend.

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
- It lists all artifacts with **SHA-256** checksums and captures environment info (Python, Pyomo, platform).  
- Never modify runs in place; **each execution** must produce a **new** folder.

Example (excerpt):
```json
{
  "run_id": "2025-10-19T12-34-56Z_01HF2...",
  "environment": {"python": "3.11.6", "pyomo": "6.7.0", "platform": "..."},
  "artifacts": [
    {"path": "solver_report.json", "sha256": "..."}
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

path = run_dir / "variables.parquet"
if path.exists():
    df = pd.read_parquet(path)
else:
    df = pd.read_csv(run_dir / "variables.csv")

df.head()
```
The variables table has normalized columns: `var, i, h, n, k, value, lower, upper`.

### Load constraints activity (optional)
```python
import pandas as pd
run_dir = Path("outputs/runs/2025-10-19_demo")

path = run_dir / "constraints_activity.parquet"
if path.exists():
    dfc = pd.read_parquet(path)
elif (run_dir / "constraints_activity.csv").exists():
    dfc = pd.read_csv(run_dir / "constraints_activity.csv")
else:
    dfc = None
```

---

## 6) KPIs best practices

- Keep names **stable** and **flat** (e.g., `tnu`, `u_min`, `u_mean`, `fairness_L1_house`, `cost_total`).  
- Prefer numeric types; avoid strings except for labels.  
- Record the **units** in a sidecar doc if needed (or the KPI YAML catalog).

---

## 7) Troubleshooting

- **No Parquet file**: install `pyarrow` or use the CSV fallback.  
- **Empty variables table**: confirm the model was solved and variables exist.  
- **Missing solver metrics**: some backends don’t expose all fields; the report shows `null`.  
- **Reproducibility**: always ship `config_snapshot.yaml` (expanded scenario).  
- **Integrity**: verify file checksums in `manifest.json`.

---

## 8) Extending reporting

- Add domain-specific KPIs: pass `kpis={...}` to `write_report(...)`.  
- Emit **constraint duals** or **reduced costs** if your solver exposes them.  
- Export to **JSON-LD** by wrapping KPIs with a `@context` if you need ontology alignment.

---

## 9) API reference (key functions)

- `write_report(model, solver_results, domain, cfg_snapshot, run_dir, run_id=None, kpis=None, include_constraints_activity=False)`  
  Generates all artifacts and returns a manifest dict.

- `write_json(path, obj)` — writes JSON with UTF-8 and indentation.  
- `write_markdown_summary(path, solver, kpis, model_stats, run_id)` — human summary.  
- `write_variables_parquet(model, path)` — variables table to Parquet (True/False).  
- `write_constraints_parquet(model, path)` — constraints activity to Parquet (True/False).  
- `save_manifest(path, manifest)` — persist manifest to disk.  
- `log_event_ndjson(path, event)` — append one event to NDJSON logs.  
- `extract_model_stats(model)` — counts variables/constraints.  
- `snapshot_domain(domain)` — minimal domain summary.

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
