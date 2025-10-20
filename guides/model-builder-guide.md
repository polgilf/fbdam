# 🏗️ FBDAM Model Builder — Usage Guide

## Overview
The **model builder** (`src/fbdam/engine/model.py`) constructs a Pyomo optimization model from:
1. A validated domain data structure (`DomainIndex`)
2. A configuration dictionary specifying active constraints and objectives.

The builder is modular, future-proof, and fully compatible with WISER naming and governance conventions.

---

## 1️⃣ Inputs

### Domain (`DomainIndex`)
This is an immutable data container holding all entities and parameters needed to build the model.  
It is typically created by `io.py` after reading and validating YAML/CSV inputs.

**Contents:**
- `items`: `Dict[item_id, Item]`
- `nutrients`: `Dict[nutrient_id, Nutrient]`
- `households`: `Dict[household_id, Household]`
- `item_nutrients`: nutrient content per item (→ `C[i,n]`)
- `requirements`: nutrient requirements per (household, nutrient) (→ `R[h,n]`)
- `bounds`: lower/upper bounds per (item, household)

### Model specification (`model`)
A dictionary defining which plugins (constraints/objectives) to activate:

```python
cfg = {
  "domain": domain_index,
  "model": {
    "constraints": [
      {"id": "nutrition_utility_mapping", "params": {}},
      {"id": "household_adequacy_floor", "params": {"U_floor": 0.8}}
    ],
    "objectives": [
      {"name": "sum_utility", "sense": "maximize", "params": {}}
    ]
  }
}
```

---

## 2️⃣ Internal structure

The builder creates, in this order:

| Stage | Component | Description |
|:--|:--|:--|
| 1 | **Sets** | I (items), N (nutrients), H (households) |
| 2 | **Params** | S[i] stock, C[i,n] content, R[h,n] requirement, γ[h] weight |
| 3 | **Vars** | x[i,h] allocation, u[n,h] utility [0,1], dpos/dneg fairness aids |
| 4 | **Expr.** | q[n,h] = Σ_i C[i,n]x[i,h], mean_utility[h], global_mean_utility |
| 5 | **Plugins** | Applies registered constraints & objective |

---

## 3️⃣ Example usage

```python
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report
from fbdam.engine.io import load_scenario

# Load YAML/CSV inputs
cfg = load_scenario("config/scenarios/demo-balanced.yaml")

# Build Pyomo model
m = build_model(cfg)

# Solve
results = solve_model(m, solver_name="appsi_highs")

# Report
write_report(results, output_dir="outputs/demo")
```

---

## 4️⃣ Notes and conventions

- `R[h,n]` now replaces the former DRI table (requirement amounts).
  A small epsilon (1e-9) prevents division-by-zero issues.
- Utility bounds: `u[n,h] ∈ [0,1]`.
- Fairness constraints rely on `dpos`/`dneg` variables predeclared by the builder.
- Plugins (registered in `constraints.py` and `objectives.py`) can be extended freely.

### Purchase budget constraints

When the `purchase_budget_limit` plugin is enabled, three complementary
constraints are created inside `constraints.py`:

1. **Budget limit** — \(\sum_i c_i y_i \leq B\). Purchases cannot exceed the
   available budget.
2. **Purchase activation** — \(y_i \leq (B / c_i) y^{\text{active}}_i\). A big-M
   link that forces the binary activation variable `y_active[i]` to turn on when
   any positive purchase is made.
3. **No waste when purchasing** — \((S_i + y_i) - \sum_h x_{i,h} \leq S_i (1 -
   y^{\text{active}}_i)\). If purchases are active the full availability
   (donated stock plus purchases) must be allocated, whereas without purchases up
   to the donated stock may remain unused.

This structure ensures that paid-for items are only bought when they can be
distributed, preventing waste of the monetary budget.

---

## 5️⃣ Extending the builder

You can add custom constraints or objectives simply by registering them:

```python
@register_constraint("nutrient_balance")
def add_nutrient_balance(m, params):
    def rule(m, n):
        return sum(m.q[n, h] for h in m.H) <= params.get("cap", 1000)
    m.NutrientCap = pyo.Constraint(m.N, rule=rule)
```

Then reference it in your YAML:

```yaml
model:
  constraints:
    - ref: nutrient_balance
      override: {cap: 800}
```

---

## 6️⃣ Outputs

After execution, the model object `m` contains:
- All sets, params, variables, constraints and objective.
- Access to computed expressions (`q`, `mean_utility`, etc.).

Typical KPIs are later extracted by the **reporting layer** (`reporting.py`).

---

## 7️⃣ Governance notes (WISER)

- Follow WISER conventions for version headers and status (`draft`, `validated`, `archived`).
- Keep identifiers in `snake_case` and YAML versioned by catalog.
- Document any new model component in the appropriate catalog file.

---

## 8️⃣ Quick checklist

✅ DomainIndex loaded and validated  
✅ Plugins registered (`constraints.py`, `objectives.py`)  
✅ Config YAML references valid plugin names  
✅ R[h,n] nonzero (builder protects with epsilon)  
✅ Model builds without Pyomo errors  

---

**Author:** Pol Gil Figuerola  
**Module:** `src/fbdam/engine/model.py`  
**Version:** v1.0 — October 2025
