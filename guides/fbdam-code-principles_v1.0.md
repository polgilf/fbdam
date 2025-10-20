# FBDAM Code Guide

**Scope:** Apply the general Code Principles (robust · beautiful · useful · minimal) to FBDAM — a machine‑reasoning + OR system for fair, nutritious, and feasible allocations. This guide describes the **target architecture**, modules, scripts, and key conventions so the repository can evolve coherently.

> Write code that a practitioner can configure, a mathematician can audit, and an engineer can extend — without shared state or surprises.

---

## 1) Target Repository Layout

```
├─ /01_SCIENCE/                      # Operational layer
│  └─ fbdam/
│     ├─ config/
│     │  ├─ constraints_v1.1.yaml
│     │  ├─ objectives_v1.0.yaml
│     │  ├─ scenario-demo.yaml
│     │  └─ dials-defaults.yaml
│     ├─ engine/
│     │  ├─ __init__.py
│     │  ├─ domain.py               # dataclasses: Item, Household, Nutrient, Requirement, Scenario
│     │  ├─ schemas.py              # pydantic / voluptuous schemas for IO validation
│     │  ├─ io.py                   # load_scenario(), read_csvs(), write_artifacts()
│     │  ├─ expressions.py          # reusable Pyomo Expressions (S+y, means, totals)
│     │  ├─ variables.py            # build decision vars with tight bounds
│     │  ├─ constraints/
│     │  │  ├─ __init__.py
│     │  │  ├─ registry.py          # @constraint_handler registry
│     │  │  ├─ capacity.py
│     │  │  ├─ balances.py
│     │  │  ├─ equity_dials.py      # A–D equity dials (with slacks when specified)
│     │  │  ├─ nutrition_dials.py   # 1–4 nutritional dials (pure ≥ using u in [0,1])
│     │  │  └─ feasibility.py       # central epsilon ≥ 0 (heavy penalty), optional
│     │  ├─ objectives/
│     │  │  ├─ __init__.py
│     │  │  ├─ registry.py          # @objective_handler registry
│     │  │  └─ maximize_tnu.py      # default objective
│     │  ├─ model.py                # orchestrates build: sets, params, vars, exprs, constraints, objective
│     │  ├─ solver.py               # appsi_highs → fallback highs; logs options + metadata
│     │  ├─ reporting.py            # KPIs, manifests, human report, artifact bundle
│     │  ├─ cli.py                  # `fbdam run ...` entrypoint
│     │  └─ utils.py                # small pure helpers (no IO, no globals)
│     ├─ data/                      # tiny demo datasets + schemas
│     ├─ outputs/
│     │  └─ runs/{run_id}/          # manifest.json, solver_report.json, kpis.json, variables.parquet, report.md
│     └─ tests/
│        ├─ test_units.py
│        ├─ test_model_shape.py     # counts of vars/constraints, bound sanity
│        ├─ test_registries.py
│        └─ test_smoke.py           # end-to-end: domain → model → solve → report
└─ /99_ARCHIVE/                      # immutable, validated history
```

> **Remark:** Mirror math terms 1:1 in names (e.g., `u[n,h]`,`x[i,h]` ). Keep IO at the edges, pure transforms in the core.

---

## 2) Configuration & Metadata

**All tunables live in YAML** under `/fbdam/config/` with minimal headers:

```yaml
version: v1.0
status: validated
maintainer: your_name
purpose: "Baseline allocation model with equity + nutrition dials"
```

- `constraints_v1.1.yaml`: declarative list of constraint IDs with parameters and scopes.
- `objectives_v1.0.yaml`: declarative selection of objective + weights.
- `scenario-*.yaml`: paths to inputs, dial settings, solver options, seed, and output directory.
- `dials-defaults.yaml`: default values for alpha_i, beta_h, gamma_n, omega_h, kappa_{n,h}.

> **Remark:** Version only **stable** catalogs. Scenario files are process-facing (no `_v` suffix).

---

## 3) Module‑by‑Module Guide

### 3.1 `engine/__init__.py`

**Purpose:** define the public API of the engine layer.

- Export `build_model`, `solve_model`, `generate_reports` for external callers.
- No heavy imports at module import time.

**Important:** Include `__all__` to document the public surface.

---

### 3.2 `engine/domain.py`

**Purpose:** *semantic* layer — pure dataclasses with invariants.

```python
@dataclass(frozen=True)
class Item:
    id: str
    name: str
    stock: float        # units available
    unit: str          # e.g., "kg"
    def __post_init__(self):
        if self.stock < 0:
            raise ValueError(f"Item {self.id} stock must be ≥ 0")
```

- Include `Household`, `Nutrient`, `Requirement(h,n,amount,unit)`, `Scenario` (paths + options).
- No Pyomo imports here; this layer is solver-agnostic.

**Important:** All invariants validate here to fail fast (e.g., nonnegative stocks, positive requirements).

---

### 3.3 `engine/schemas.py`

**Purpose:** IO validation (columns, dtypes, allowed sets) independent of the model.

- Use pydantic / python‑schema (or simple custom validators) — minimal dependencies.
- Expose helpers: `validate_items(df)`, `validate_households(df)`, `validate_requirements(df)`.
- Ensure unit consistency and ID uniqueness.

**Important:** Reject early with actionable error messages (which file, which row, expected range).

---

### 3.4 `engine/io.py`

**Purpose:** Edge of the system — read/write only.

- `load_scenario(scn_path) -> Scenario`
- `read_csvs(scn: Scenario) -> DomainData`
- `write_artifacts(run_dir, manifest, solver_report, kpis, variables_frame, human_report)`

**Important:** Never create Pyomo objects here. Resolve relative paths against the scenario file location.

---

### 3.5 `engine/expressions.py`

**Purpose:** Centralize *common expressions* used across constraints for **SSOT** (single source of truth).

- `S_plus_y[i] := S[i] + y[i]` (supply + purchase) — define once, reuse everywhere.
- `mean_u_h[h] := (1/|N|) Σ_n u[n,h]` — household mean utility.
- `mean_u_n[n] := (1/|H|) Σ_h u[n,h]` — nutrient mean utility.
- `global_mean_u := (1/(|N||H|)) Σ_{n,h} u[n,h]` — overall mean utility.

**Important:** Expressions avoid recomputation during rule evaluation and prevent drift.

---

### 3.6 `engine/variables.py`

**Purpose:** Define variables with **tight bounds** and domains; apply names mirroring math.

- Example: `y[i] ≥ 0` (purchases), `x[i,h] ≥ 0` (allocations), `u[n,h] ∈ [0,1]` (capped utilities).
- Central place to define any optional feasibility slack `epsilon ≥ 0` (default excluded unless enabled by config).

**Remark:** Avoid introducing duplicate totals (`T`) if they can be derived via expressions (`S_plus_y`).

---

### 3.7 `engine/constraints/registry.py`

**Purpose:** Declarative plugin system for constraints.

```python
HANDLERS = {}
def constraint_handler(name):
    def _wrap(fn):
        HANDLERS[name] = fn
        return fn
    return _wrap
```

- `apply_constraints(model, catalog_yaml, dials)` — iterates IDs → looks up handlers → applies rules.
- Centralize dial resolution (e.g., `_dial(dials, "alpha", default=0.2)`).

**Important:** No business logic in `model.py`; all constraint specifics live behind handlers.

---

### 3.8 `engine/constraints/*.py`

**Purpose:** Themed constraint packs with **math‑faithful** rules.

- `capacity.py` — stock limits, purchase limits, budget caps.
- `balances.py` — conservation and item‑to‑nutrient linkage via coefficients `a[i,n]`.
- `equity_dials.py` — A–D equity mechanics (with slacks if configured), reuse shared expressions.
- `nutrition_dials.py` — (1)–(4) *pure floors* using `u[n,h] ∈ [0,1]` and `≥` inequalities only, as specified.
- `feasibility.py` — single global `epsilon` slack with **heavy penalty**, only enabled for guardrail runs.

**Remark:** Prefer inline means via `Expression` rather than helper totals; compute once, reuse many.

---

### 3.9 `engine/objectives/registry.py` & `maximize_tnu.py`

**Purpose:** Objective plugins.

- Default: **maximize TNU** (total nutritional utility) or another declared in config.
- Allow weighted objectives: `maximize a*TNU − b*PurchasesCost − c*SlackPenalty` (only if configured).
- Document objective in module docstring and surface in manifest.

**Important:** All penalty weights must be explicit in config; no magic constants.

---

### 3.10 `engine/model.py`

**Purpose:** Pure orchestrator — no business formulas here.

Steps (exact order):

1. Build **sets** and **params** from domain and IO.
2. Create **variables** (via `variables.py`).
3. Register **expressions** (via `expressions.py`).
4. Apply **constraints** (via registry + catalogs).
5. Attach **objective** (via registry).

**Remark:** Return a `ConcreteModel` and a small `BuildInfo` (counts, names, options).

---

### 3.11 `engine/solver.py`

**Purpose:** Deterministic solve + metadata.

- Try `appsi_highs` then fallback to `highs`.
- Fix seed; set tolerances; capture wall‑clock, iterations, nodes, objective, best bound, gap.
- Return `(termination, solver_report, solution_handle)`.

**Important:** Never mutate the model post‑solve. Record solver versions and options in the report.

---

### 3.12 `engine/reporting.py`

**Purpose:** First‑class observability.

Artifacts per run (machine + human):

- `manifest.json` — solver, config versions, seed, start/end time, objective, gap, counts.
- `solver_report.json` — detailed solver metrics.
- `kpis.json` — fairness, adequacy, costs, purchase totals, outliers.
- `variables.parquet` — wide table with `(i,h,n)` coordinates as needed.
- `report.md` — short narrative with dials, anomalies, and next actions.

**Important:** Report any coercions (e.g., clipping `u` to [0,1]) and any slack usage with magnitudes.

---

### 3.13 `engine/cli.py`

**Purpose:** Thin UX layer.

Commands:

- `fbdam run SCENARIO.yaml [--out OUTDIR] [--seed 123] [--profile]`
- `fbdam explain CONSTRAINT_ID` — shows math + code path.
- `fbdam bundle RUN_DIR` — zips artifacts for sharing.

**Remark:** CLI should remain optional; Python API is primary.

---

### 3.14 `engine/utils.py`

**Purpose:** Small, pure helpers only (e.g., deep merges, timer context, hashers). No IO, no Pyomo objects.

---

## 4) Testing Strategy (pyramid)

- **Unit tests** — deterministic helpers, dial resolution, schema validators, expression builders.
- **Model shape tests** — variable & constraint counts vs tiny fixtures; bound checks.
- **Smoke/E2E** — minimal scenario through the full pipeline; assert feasibility and artifact presence.
- **Golden files** — tiny “truth” artifacts for regression (tolerant numeric diffs).

> **Definition of Done (test):** all three layers pass; coverage doesn’t regress on non‑trivial code.

---

## 5) Data & Units (as it should be)

- Keep tiny **demo datasets** under `data/` with CSV headers in `snake_case` and an accompanying `schema.md`.
- Enforce unit consistency at load time; convert once (never inside constraint rules).
- Referential integrity: all IDs in fact tables must exist in dimensions (fail loud).

---

## 6) Naming, Versioning & Logs (governance)

- Snake_case for code & keys; kebab‑case for human‑facing files.
- Only **stable** catalogs are versioned with `_vMAJOR.MINOR.PATCH`.
- Every scenario/run appends a line in `prompt-log.md` (summary + affected artifacts).
- Archive, never delete. Tag validated milestones in Git if applicable.

---

## 7) Performance & Complexity

- Precompute sparse maps (e.g., `I_by_n`, `N_by_i`) and pass as params to avoid dense loops.
- Use `Expression` for repeated aggregates (`S_plus_y`, `mean_u_h`, `global_mean_u`).
- Measure before tuning. Persist counters in `manifest.json` for comparison across runs.
- Keep modules flat; prefer clear functions to deep inheritance trees.

---

## 8) Error Handling & Messages

- Domain‑specific exceptions: `MissingHousehold`, `OutOfRangeRequirement`, `UnknownNutrient` with IDs and row numbers.
- No silent fixes. If clipping or imputing is necessary, record it in the human report + machine logs.
- First failure wins: fail at **schemas** or **domain** before model build.

---

## 9) Reviewer Checklist (PRs)

- Names mirror math & domain; units enforced on input.
- No logic in `model.py`; all rules live in constraint plugins.
- Variables have tight bounds; expressions defined once; no duplicated totals.
- Deterministic solver options recorded; seeds fixed.
- Artifacts generated (`manifest.json`, `report.md`, `variables.parquet`).
- Prompt‑log updated; catalog versions bumped when behavior changes.

---

## 10) Quickstart (ideal)

```bash
# Install
pip install -e .[appsi_highs]

# Run demo
fbdam run 01_SCIENCE/fbdam/config/scenario-demo.yaml --out 01_SCIENCE/fbdam/outputs/runs

# Inspect
less 01_SCIENCE/fbdam/outputs/runs/20251019-1530/manifest.json
```

---

## 11) Appendix — Example Constraint Snippets (canonical)

### (A) Nutrition dials (pure floors, u in [0,1])

```python
# (2N) Per-nutrient floor (aggregate over households): mean_h(u[n,·]) >= gamma[n] * global_mean_u
@constraint_handler("nutrient_floor_mean")
def nutrient_floor_mean(m, gamma):
    return pyo.Constraint(m.N, rule=lambda m,n: m.mean_u_n[n] - gamma[n]*m.global_mean_u >= 0)
```

### (B) Equity dial with reused expressions

```python
# Keep allocations near fair-share weights using S_plus_y and mean allocations
@constraint_handler("equity_item_deviation_roof")
def equity_item_dev_roof(m, alpha):
    # Example structure; actual normalization defined in catalog
    return pyo.Constraint(m.I, rule=lambda m,i: m.item_dev_norm[i] <= alpha[i])
```

### (C) Central feasibility slack (guardrail only)

```python
@constraint_handler("global_feasibility_slack")
def global_slack(m, penalty):
    m.epsilon = pyo.Var(domain=pyo.NonNegativeReals)
    # activated only if configured
    return pyo.Constraint(expr = m.some_infeasible_floor - m.epsilon <= 0)
# Objective plugin must add:  - penalty * m.epsilon
```

---

### Closing

This guide is prescriptive by design. If a future change deviates, document **why** in an ADR and reflect it in the catalogs. Keep the math faithful, the code humane, and the outputs decisively useful.
