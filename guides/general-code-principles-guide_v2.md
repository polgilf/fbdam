# Code Principles Guide (v2.0)

**Goal:** unify semantics & practitioner meaning, mathematical rigor & OR knowledge, and software engineering best practices.

The project must produce systems that are **robust, beautiful, useful, and minimal** — high output per unit of effort.

---

## 1. Philosophy & Scope

### 1.1 Intent
Design every line of code as a bridge between **domain semantics**, **mathematical truth**, and **engineering clarity**.

> *Reason over ritual · Convention over configuration · Automation over repetition*

### 1.2 Principles
| Pillar | Meaning | Why it matters |
|:--|:--|:--|
| **Robust** | Deterministic, validated, fail-loud systems | Guarantees scientific and operational reproducibility |
| **Beautiful** | Code reads like an explanation | Long-term maintainability and onboarding clarity |
| **Useful** | Deliver actionable artifacts | Real-world impact beyond computation |
| **Minimal** | Only generalize when reused twice | Focus, elegance, and performance |

---

## 2. Architecture & Semantics

### 2.1 Separation of Concerns
Each layer speaks its own language:
- **Domain** — practitioner semantics (`Item`, `Household`, `Nutrient`)
- **Model** — mathematical translation (variables, constraints, objectives)
- **Solver** — algorithm and metadata collection
- **Reporting** — metrics, KPIs, and human insight

> *If you can’t swap HiGHS for Gurobi without touching domain logic, separation has failed.*

### 2.2 Semantic Source of Truth (SSOT)
- Represent each domain concept once — names, symbols, and units reused across layers.
- Mathematical names (e.g. \(u_{n,h}, w_h\)) → code mirrors (`u[n,h]`, `w[h]`).
- Store and validate **units**; convert only at load time.

### 2.3 Declarative Modeling
- Express mathematical *intent*, not procedural steps.
- Avoid hidden side effects during model construction.
- Use tight variable bounds and centralized slacks.

```python
# ✅ Declarative intent
def fair_share_rule(m, h):
    return m.alloc[h] >= m.w[h] * m.mean_alloc
m.FairShare = pyo.Constraint(m.H, rule=fair_share_rule)
```

### 2.4 One Concept = One Definition
Never duplicate logic.
- Common expressions → `Expression()` not recomputed loops.
- Shared formulas → referenced, not copied.
- Derived totals (`S + y`) defined once and reused.

### 2.5 Determinism
- Fix seeds and solver tolerances.
- Record version, seed, solver, and time in the **manifest**.

---

## 3. Codecraft & Modeling

### 3.1 Explicit Over Clever
Prefer verbosity that teaches.
```python
# ❌ Opaque
m.R = pyo.Param(m.H, m.N, initialize=lambda m,h,n: reqs.get((h,n),0)+1e-9)

# ✅ Explicit, auditable
EPS_R = 1e-9  # Avoid divide-by-zero
m.R = pyo.Param(m.H, m.N, initialize=_init_R, doc="Requirement amount floored")
```

### 3.2 Config-Driven, Schema-Validated
- Validate every input schema early.
- All tunables live in YAML (`version`, `status`, `maintainer`, `purpose`).
- Immutable inputs → timestamped outputs.

### 3.3 Performance as Design
- Precompute expressions; avoid N×H×I loops.
- Profile before optimizing; measure before tuning.
- Vectorize and cache domain mappings.

### 3.4 Testing Pyramid
| Layer | Purpose | Example |
|:--|:--|:--|
| Unit | Core helpers, aggregations | `test_utils.py` |
| Model | Constraint/variable counts | `test_model_build.py` |
| Smoke | End-to-end run | `pytest tests/test_smoke.py` |

Golden small datasets detect drift better than synthetic stress tests.

### 3.5 No Magic State
- Pure functions, immutable dataclasses.
- No globals that mutate after import.
- Registries only for declarative plugins.

---

## 4. Testing, Reporting & Observability

### 4.1 Run Manifest
Each execution yields a structured manifest:
```json
{
  "solver": "highs",
  "runtime_sec": 1.23,
  "objective": 42.5,
  "gap": 0.0001,
  "seed": 123,
  "config_version": "v1.2"
}
```
**Why:** makes runs reproducible and comparable.

### 4.2 Reporting Discipline
- **Machine report:** JSON/NDJSON of all metrics.
- **Human report:** Markdown summary (KPIs, fairness, anomalies).
- Bundle manifest, logs, KPIs, and artifacts → `/outputs/runs/{run_id}/`.

### 4.3 Error Handling
- Fail with context (`MissingHousehold: H42 not found in households.csv`).
- No silent coercions; log and surface corrections.

### 4.4 Observability Metrics
Track variable count, constraint count, objective value, runtime, gap, and solver iterations.
Expose via `reporting.py`.

---

## 5. Governance, Versioning & Collaboration

### 5.1 Versioning & Metadata
Follow **SemVer-lite** (MAJOR.MINOR.PATCH). Only stable artifacts carry `_v`.
```yaml
version: v2.0
status: validated
maintainer: your_name
purpose: "Baseline allocation model"
```

### 5.2 Logs & Traceability
- Append every AI-assisted or structural change to `prompt-log.md`.
- Never delete history — archive validated files under `/99_ARCHIVE/`.

### 5.3 Collaboration & Reviews
- **PRs:** small, atomic, narrative (`What / Why / How / Impact`).
- **Reviewers check:** naming, tests, docs, rationale, version bump.
- **AI contribution:** append short note in `prompt-log.md`.

### 5.4 Documentation Minimums
- Docstrings express *intent and contract* (inputs, outputs, invariants).
- Headers carry version and maintainer.
- Small runnable examples preferred over long prose.

### 5.5 Definition of Done
A change is done when:
- Tests (unit/model/smoke) pass.
- Manifest and report generated.
- Naming, version, and metadata validated.
- Prompt-log updated.
- Rationale recorded (PR, ADR, or comment).

---

## 6. Lightweight ADR Template
```markdown
**Title:** Add fairness floor constraint
**Context:** Distribution equity must exceed baseline.
**Decision:** Introduce \(u_{n,h} \geq \omega_h \cdot \text{mean}(u_{n,h})\)
**Why:** Increases nutritional fairness consistency.
**Implications:** Update constraint catalog + tests.
**Links:** PR #42, prompt-log 2025-10-19
```

---

## 7. Practical Heuristics
- If it isn’t tested → it’s a prototype.
- If a name needs a comment → rename it.
- If a function does two things → split it.
- If logic repeats → extract a helper.
- If the math term exists → mirror it in code.
- If config alters behavior → bump MINOR and explain why.

---

### Closing
These principles ensure that mathematical rigor, operational research semantics, and industrial code quality **converge**.  
Code should stay faithful to the model, humane to the reader, and decisive in output — always aiming for **clarity, reproducibility, and impact**.

