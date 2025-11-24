# FBDAM Repository Analysis

## 1. Quick Orientation
- **Project one-liner:** FBDAM is a configurable MILP framework for equitable and nutritious food distribution, combining Pyomo modeling with YAML-driven scenarios and a Typer CLI to build, solve, and report allocation plans.【F:README.md†L3-L41】
- **Primary optimization problem(s):**
  - **Decision variables:** item-to-household allocations `x[i,h]` (integer or continuous), optional purchases `y[i]` with activation binaries `y_active[i]`, normalized utilities `u[n,h]`, deviation auxiliaries `dpos/dneg`, and global slack `epsilon`.【F:src/fbdam/engine/model.py†L91-L177】【F:src/fbdam/engine/model.py†L199-L246】
  - **Objectives:** default objective maximizes total nutritional utility (sum of `u[n,h]`), optionally penalizing slack via λ.【F:src/fbdam/engine/objectives.py†L61-L102】
  - **Constraints:** nutrient utility mapping; item supply and purchase budget; fair-share deviation identities plus equity caps (item, household, pairwise); and nutritional adequacy floors (household, nutrient, pairwise), with optional shared slack driven by λ.【F:src/fbdam/engine/constraints.py†L63-L218】【F:src/fbdam/engine/constraints.py†L220-L360】
- **Intended users and usage mode:** Scenario-driven CLI (`fbdam run`), programmatic API (`build_model`, `solve_model`, `write_report`), and YAML catalogs for reusing constraint/objective blocks.【F:README.md†L38-L117】【F:README.md†L166-L181】 Main entrypoint is `src/fbdam/engine/run.py`, which wires loading, solving, and reporting.

## 2. Domain and Problem Framing
- **Domain:** Humanitarian food basket design and allocation across households with nutrient requirements.
- **Entities:** Items with stock/cost; nutrients; households with member counts and fair-share weights; nutrient requirements per household; item–nutrient content; optional per-(item, household) allocation bounds, captured in immutable dataclasses (`Item`, `Nutrient`, `Household`, `Requirement`, `ItemNutrient`, `AllocationBounds`) aggregated in `DomainIndex`.【F:src/fbdam/engine/domain.py†L13-L130】
- **Problem hardness:** Mixed-integer structure (integer/continuous `x`, binary `y_active`), proportional fairness caps, and adequacy floors create a combinatorial, multi-objective tuning space controlled by dials.

## 3. Architecture Map
- **Folders:**
  - `src/fbdam/engine`: pipeline components (domain dataclasses, data loading, model builder, constraints/objectives registries, solver wrapper, reporting, CLI).
  - `src/fbdam/config`: packaged YAML catalogs and schemas for constraint/objective definitions.
  - `guides/`: architecture, modeling, I/O, reporting guides.
  - `tests/`: Pytest smoke test exercising end-to-end flow.
- **Key modules:**
  - `engine/io.py`: loads scenario YAML, merges catalogs, resolves data paths, and materializes constraints/objectives into a `ScenarioConfig` for the builder.【F:src/fbdam/engine/io.py†L1-L126】
  - `engine/data_loader.py`: reads CSV datasets into domain entities (not reproduced here) and pairs them with model parameters.
  - `engine/model.py`: builds Pyomo model (sets, params, vars, expressions) and applies constraint/objective plugins.【F:src/fbdam/engine/model.py†L34-L166】【F:src/fbdam/engine/model.py†L248-L336】
  - `engine/constraints.py` & `engine/objectives.py`: registries plus implementations; YAML catalogs resolve to these names.
  - `engine/solver.py`: solver selection (HiGHS AppSi or classic), execution, and result normalization.【F:src/fbdam/engine/solver.py†L14-L121】
  - `engine/reporting.py`/`engine/kpis.py`: postprocessing and artifact generation (not detailed here).
  - `engine/run.py`: Typer CLI dispatching `run` and `version` commands.
- **Dependency direction:** Data (CSV→`data_loader`) → domain dataclasses (`domain.py`) → model builder (`model.py`) → constraints/objective plugins (`constraints.py`, `objectives.py`) → solver (`solver.py`) → reporting (`reporting.py`). CLI orchestrates end-to-end via `io.load_scenario` then `build_model`/`solve_model`/`write_report`.

## 4. Optimization Model(s) in Detail
- **Modeling framework & solvers:** Pyomo ConcreteModel with support for AppSi HiGHS or classic HiGHS; falls back to mock solver if unavailable.【F:src/fbdam/engine/model.py†L60-L166】【F:src/fbdam/engine/solver.py†L18-L76】
- **Sets & indices:** Items `I`, Nutrients `N`, Households `H`; sizes `cardI/cardN/cardH` stored as Params.【F:src/fbdam/engine/model.py†L107-L132】
- **Parameters:** Stock `S[i]`, cost `cost[i]`, fair-share weights `fairshare_weight[h]`, nutrient content `a[i,n]`, requirements `R[h,n]` with epsilon floor.【F:src/fbdam/engine/model.py†L134-L177】
- **Decision variables:**
  - `x[i,h]` allocation (bounds optional per pair).【F:src/fbdam/engine/model.py†L185-L205】
  - `u[n,h]` normalized utility in [0,1].【F:src/fbdam/engine/model.py†L207-L208】
  - Purchases `y[i]` and activation binaries `y_active[i]` (fixed to 0 if purchases disabled).【F:src/fbdam/engine/model.py†L210-L221】
  - Deviation helpers `dpos/dneg[i,h]` and global slack `epsilon`.【F:src/fbdam/engine/model.py†L223-L246】
- **Expressions:** Nutrient delivery `q[n,h]`, available supply `Avail[i]`, totals (`TotSupply`, `TotAllocated`, `Undistributed`, `TotalCost`), household/nutrient/global mean utilities, and deviation aggregates/ratios for fairness metrics.【F:src/fbdam/engine/model.py†L252-L362】【F:src/fbdam/engine/model.py†L364-L455】
- **Objective:** `sum_utility` maximizes weighted total utility minus λ·ε when λ provided; sense configurable but defaults to maximize.【F:src/fbdam/engine/objectives.py†L61-L102】 Only first objective applied; future extensions could combine multiple.
- **Constraints:**
  - *Core mechanics:* nutrient-utility mapping `u <= q/R`; item supply limits; purchase budget with activation and no-waste logic (big-M on purchases).【F:src/fbdam/engine/constraints.py†L63-L133】【F:src/fbdam/engine/constraints.py†L135-L218】
  - *Allocation equity (α, β, γ/ρ):* deviation identity linking `x` to fair-share targets; item, household, and pairwise deviation caps using dial values; legacy household cap retained.【F:src/fbdam/engine/constraints.py†L220-L344】
  - *Nutritional adequacy (ρ/ω, κ/γ):* floors on household mean utility, nutrient mean utility, and pairwise utility relative to global mean, with optional slack driven by λ or explicit flags.【F:src/fbdam/engine/constraints.py†L346-L414】
- **Parameters & calibration:** Dial values resolved with priority (constraint params → model_params.dials → defaults) and support scalar or indexed mappings; slack activation controlled by λ or `use_slack` flag.【F:src/fbdam/engine/constraints.py†L29-L110】 Model parameters also include `x_integrality`, `allow_purchases`, and `budget` to toggle integrality, purchases, and procurement spend.【F:src/fbdam/engine/model.py†L68-L104】【F:src/fbdam/engine/constraints.py†L135-L174】

## 5. Data, Configuration, and I/O Flow
- **Input data sources:** CSV files for items, nutrients, households (with members to derive fair-share), requirements, item–nutrient content, and optional household-item bounds; paths resolved relative to a dataset root in the scenario/config YAML (handled by `load_domain_and_params`).【F:README.md†L66-L104】【F:src/fbdam/engine/io.py†L1-L126】
- **Configuration system:** Scenario YAML references a dataset block and config block; config YAML holds model/solver defaults and dials. Catalog references (`ref`) resolve to packaged YAML catalogs, with per-scenario overrides applied in `io._materialize_constraints/_materialize_objectives`. The resulting `ScenarioConfig` carries normalized paths, domain index, model params, constraint/objective specs, solver config, and raw manifest for traceability.【F:src/fbdam/engine/io.py†L1-L126】
- **Outputs:** Reporting module writes manifest, KPIs, solver report/logs, MPS (optional), allocation/variable CSVs under user-provided `--outputs` path; README lists example outputs and infeasibility diagnostics.【F:README.md†L106-L164】

## 6. Execution Pipeline and Entry Points
- **CLI:** `fbdam run <scenario.yaml> --outputs <dir> [--solver highs]` loads scenario, builds model, solves, and emits reports; `fbdam version` prints package version.【F:README.md†L106-L165】
- **Execution sequence:** (1) `io.load_scenario` parses YAMLs, catalogs, and CSVs into `ScenarioConfig`; (2) `model.build_model` constructs Pyomo model with plugins; (3) `solver.solve_model` picks HiGHS backend, solves, and collates status/gaps/vars; (4) reporting module generates human-readable and machine artifacts (per README description).【F:README.md†L38-L165】【F:src/fbdam/engine/model.py†L60-L166】【F:src/fbdam/engine/solver.py†L18-L121】
- **Experimentation:** Dials in model params and constraint overrides enable scenario sweeps; multiple scenario YAMLs (e.g., demo balanced vs. infeasible vs. TNU) illustrate differing equity/adequacy regimes.【F:README.md†L66-L165】

## 7. Modularity and Extension Points
- **Plugin registries:** `register_constraint` and `register_objective` enable adding new constraint/objective blocks referenced from catalogs without modifying the builder.【F:src/fbdam/engine/constraints.py†L7-L58】【F:src/fbdam/engine/objectives.py†L1-L46】
- **Configurable integrality/purchases/budget:** `model_params` allow toggling `x` integrality, enabling purchases, and setting budgets; builder detects constraints needing purchases to activate relevant variables.【F:src/fbdam/engine/model.py†L68-L104】【F:src/fbdam/engine/model.py†L185-L221】
- **Catalog overrides:** Scenario YAML can override dial values per constraint/objective, supporting rapid policy experimentation without code changes.【F:README.md†L66-L104】【F:src/fbdam/engine/io.py†L1-L126】
- **Extension steps:** To add a new constraint family, implement a Pyomo-building function, decorate with `@register_constraint("name")`, add catalog entry, and reference via scenario `constraints`. Similar steps for objectives using `register_objective` and catalog updates.【F:src/fbdam/engine/constraints.py†L7-L58】【F:src/fbdam/engine/objectives.py†L1-L46】

## 8. Assumptions, Invariants, and Constraints
- **Domain assumptions (explicit):** Nonnegative stock/cost/requirements/quantities; household members/weights nonnegative; allocation bounds honor lower≤upper; enforced in dataclass `__post_init__` validations.【F:src/fbdam/engine/domain.py†L13-L130】
- **Model invariants (explicit):** Requirements floored at epsilon to avoid division by zero; utility bounded [0,1]; purchases fixed to 0 when disabled; slack optionally activated by λ or `use_slack`.【F:src/fbdam/engine/model.py†L144-L177】【F:src/fbdam/engine/model.py†L207-L221】【F:src/fbdam/engine/constraints.py†L80-L110】
- **Technical assumptions (explicit):** Python 3.12+, HiGHS availability preferred; YAML scenarios structured as mappings; supported solvers limited to AppSi HiGHS/classic HiGHS (else mock).【F:README.md†L42-L64】【F:src/fbdam/engine/solver.py†L18-L76】
- **Implicit hypotheses:** Datasets provide complete mappings (no missing keys) since `DomainIndex` expects total mappings; fairness weights derived from household members as default per README.

## 9. Design Decisions and Trade-offs
- **Plugin-based constraints/objectives:** Registry plus catalogs decouple policy definitions from model builder, easing experimentation but requiring disciplined naming and catalog maintenance.【F:src/fbdam/engine/model.py†L60-L166】【F:src/fbdam/engine/constraints.py†L7-L58】 Hypothesis: chosen for configurability and reuse across scenarios; trade-off is single-objective limitation and need for catalog synchronization.
- **Shared slack with λ penalty:** Slack variable `epsilon` used across adequacy constraints with optional λ penalty in objective, preserving feasibility diagnostics when constraints are relaxed. Trade-off: single slack aggregates violations, potentially obscuring which constraint is tight.【F:src/fbdam/engine/model.py†L223-L246】【F:src/fbdam/engine/objectives.py†L90-L102】【F:src/fbdam/engine/constraints.py†L80-L110】
- **Purchasing activation via big-M:** Uses `y_active` binaries with budget-derived big-M and no-waste constraint to avoid purchasing without allocation. Hypothesis: balances realism of procurement decisions with MILP complexity; big-M scaling tied to budget/cost ensures reasonable bounds.【F:src/fbdam/engine/constraints.py†L135-L218】
- **Single-objective application:** Builder takes first objective only, simplifying pipeline but limiting multi-objective scalarization; future extension hinted in code comments.【F:src/fbdam/engine/model.py†L418-L449】【F:src/fbdam/engine/objectives.py†L61-L102】

## 10. Testing, Reliability, and Observability
- **Testing:** Pytest smoke test exercises full pipeline with tiny domain; run via `pytest`.【F:README.md†L183-L195】 No extensive unit tests observed for individual plugins.
- **Validation:** Dataclass `__post_init__` checks for nonnegativity and required IDs; `io.py` enforces YAML structure and path existence; requirements floored to epsilon to avoid divide-by-zero.【F:src/fbdam/engine/domain.py†L13-L130】【F:src/fbdam/engine/model.py†L144-L177】【F:src/fbdam/engine/io.py†L1-L126】
- **Logging/diagnostics:** Solver wrapper captures termination/status/gap, logs infeasibility warnings, and returns variable snapshots; README documents saved artifacts (solver_report.json, logs, MPS) for troubleshooting.【F:src/fbdam/engine/solver.py†L18-L121】【F:README.md†L132-L145】

## 11. Re-use or Re-implementation Guide
- **Run as-is:**
  1. Install with `pip install -e .[appsi_highs]` (or `[highs]`).【F:README.md†L42-L64】
  2. Execute `fbdam run scenarios/demo-balanced.yaml --outputs outputs/demo-run` or the provided demo scenarios.【F:README.md†L66-L165】
  3. Inspect outputs under the chosen directory; reference `outputs/example/` as template.
- **Port/re-implement concepts:**
  - Replicate domain dataclasses (`domain.py`), plugin registries (`constraints.py`, `objectives.py`), model builder structure (`model.py` sets/params/vars/expressions), and solver/result normalization (`solver.py`). The CLI/reporting are infrastructure and can be swapped.
- **Adapt to related problems:**
  - Add or modify constraint plugins for new equity/adequacy notions; adjust objective handlers; extend data loader/domain to include new entities (e.g., facilities or routes) while keeping `DomainIndex` mappings consistent; update catalogs and scenario YAML to reference new components.

## 12. Limitations and Open Questions
- **Limits:** Single-objective support only; slack aggregates violations; solver options limited to HiGHS (others would need extensions); scalability of big-M purchases and dense deviations may be challenging for large instance sizes.
- **Uncertainties:** Full data loader and reporting details not covered here; precise catalog schemas and additional guides should be consulted. Extent of validation beyond structural checks is unclear.
- **Ethical considerations:** Equity and adequacy dials reflect fairness intentions, but weighting choices affect distribution outcomes; societal impacts depend on dial calibration and data quality.

