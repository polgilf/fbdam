# FBDAM Backbone Model (Final)

**Purpose.** A compact, implementation-ready mathematical backbone for FBDAM.  
- Clear for practitioners (what it enforces), precise for mathematicians (linear, well-defined), and modular for developers (plug-in dials).  
- **No unnecessary helper variables** are introduced. We do, however, define a few **Expressions** `:=` (not Vars) to name shared linear aggregates; this improves clarity and consistency **without** enlarging the LP.

---

## Sets
- $I$: items (foods).  
- $H$: households.  
- $N$: nutrients.

---

## Parameters (nonnegative unless noted)
- $a_{i,n}$: nutrient $n$ per unit of item $i$.  
- $R_{n,h} > 0$: adequacy requirement for nutrient $n$ and household $h$.  
- $S_i$: donated stock (units) available of item $i$.  
- $w_h \ge 0$: **fair-share weight** for household $h$, with $\sum_{h\in H} w_h = 1$.  
- $c_i$ (optional): purchase cost per unit of $i$.  
- $B$ (optional): total purchase budget.

**Dial parameters** (scenario-tunable; may be indexed or uniform scalars):

- $\rho_{i,h } \in [0,1]$ per-pair **deviation cap** (L1) around fair-share.   
- $\kappa_{n,h} \in [0,1]$: per-pair **floor** (no adequacy outliers vs global mean).  
- $\lambda \gg 0$ (optional): penalty for the feasibility slack $\varepsilon$ (if enabled).

> For a simplified start, you can use uniform scalars $\rho$ and  $\kappa$.

---

## Decision variables
- $x_{i,h} \ge 0$: units of item $i$ allocated to household $h$.  
- $y_i \ge 0$: units of item $i$ purchased (to augment donated stock).  
- $u_{n,h} \in [0,1]$: **capped nutritional utility/adequacy** for pair $(n,h)$.  
- $\delta^+_{i,h} \ge 0,\ \delta^-_{i,h} \ge 0$: **L1 deviation variables** for equity-in-quantities dials.  
- $\varepsilon \ge 0$ (optional): single **global slack** to soften floors (enable only if needed).

---

## Expressions `:=` (named linear aggregates, **not** variables)

We define these once and reuse them; they do **not** add rows/columns to the solver model.

- **Means of utility**
  $$
  \bar u_h \;:=\; \frac{1}{|N|}\sum_{n\in N} u_{n,h},\qquad
  \bar u_n \;:=\; \frac{1}{|H|}\sum_{h\in H} u_{n,h},\qquad
  \bar u_{\mathrm{all}} \;:=\; \frac{1}{|N||H|}\sum_{n\in N}\sum_{h\in H} u_{n,h}.
  $$

- **Supply and totals**
  $$
  \text{Avail}_i \;:=\; S_i + y_i,\qquad
  \text{TotSupply} \;:=\; \sum_{i\in I}(S_i + y_i),\qquad
  X_h \;:=\; \sum_{i\in I} x_{i,h},\qquad
  q_{n,h} \;:=\; \sum_{i\in I} a_{i,n}\,x_{i,h}.
  $$

**Why Expressions?** They encode domain semantics (e.g., “available supply”) and prevent copy-paste errors, while keeping the matrix size unchanged. **Trade-off:** a few more Python objects vs. much cleaner and safer model-building code.

---

## Objective (efficiency with optional feasibility penalty)
$$
\max\quad \mathbf{TNU} \;-\; \lambda\,\varepsilon
\qquad\text{where}\qquad
\mathbf{TNU} \;:=\; \sum_{n\in N}\sum_{h\in H} u_{n,h}.
$$
> If no softening is desired, set $\lambda=0$ and omit $\varepsilon$.

---

## Constraints

### A) Stock, purchase, and mass balance
Allocation of each item cannot exceed available stock plus purchases:
$$
\sum_{h\in H} x_{i,h} \;\le\; S_i + y_i \;=\; \text{Avail}_i,\qquad \forall i\in I.
$$

Optional purchase budget:
$$
\sum_{i\in I} c_i\,y_i \;\le\; B.
$$

### B) Nutrition mapping and capped utilities
Map intake to capped utilities (linearized min by upper bounds):
$$
u_{n,h} \;\le\; \frac{1}{R_{n,h}} \sum_{i\in I} a_{i,n}\,x_{i,h} \;=\; \frac{q_{n,h}}{R_{n,h}},\qquad \forall n\in N,\; h\in H,
$$
$$
0 \;\le\; u_{n,h} \;\le\; 1,\qquad \forall n\in N,\; h\in H.
$$

### C) Nutritional dials — **pure floors** (all are “$\ge$” type)

1. **Per‑pair floor (no adequacy outliers vs global mean):**
$$
u_{n,h} \;-\; \kappa_{n,h}\,\bar u_{\text{all}} \;\ge\; -\varepsilon,\qquad \forall n\in N,\; h\in H.
$$

> Use $\varepsilon=0$ for hard floors; enable $\varepsilon$ (with large $\lambda$) only as a feasibility safety valve in tight scenarios.

### D) Equity dials (quantities) — **L1 deviation linearization** around fair-share $w_h$

Control absolute deviations from the fair-share target $w_h\,(S_i+y_i)$ using $\delta^\pm_{i,h}\ge 0$.

**Per-pair deviation identity:**
$$
x_{i,h} - w_h\,(S_i + y_i) \;=\; \delta^+_{i,h} - \delta^-_{i,h},
\qquad \forall i\in I,\; h\in H.
$$

**Per-pair cap (no quantity outliers):**
$$
\delta^+_{i,h} + \delta^-_{i,h} \;\le\; \rho_{i,h}\,(S_i + y_i),
\qquad \forall i\in I,\; h\in H.
$$

> The $\ell_1$ (absolute deviation) caps provide aggregate equity control that is more flexible and robust than hard per-pair bands, while remaining linear and solver-friendly.

---

## Recommended **simplified start**
- Objective: maximize $\mathbf{TNU}$ (omit $\varepsilon$).  
- Uniform dials:  $\kappa_{n,h}\equiv\kappa$; $\rho_{i,h}\equiv\rho$
- Include the budget constraint only if needed.  
- Keep $w_h$ exogenous and normalized (e.g., proportional to need/size).

---

## Implementation notes (for developers)
- Model is **linear**; domains are nonnegative with tight bounds (e.g., $0\le u_{n,h}\le 1$).  
- Use **Expressions** (not Vars) for $\text{Avail}_i$, $\text{TotSupply}$, $X_h$, $q_{n,h}$, and $\bar u$’s to keep the code DRY and auditable with **no solver-size penalty**.  
- Implement each dial block (C1–C3, D) as a toggleable **plugin**.  
- If $\varepsilon$ is enabled, add $-\lambda\varepsilon$ to the objective and **report** $\varepsilon$ and binding rates.  
- For numerical scaling, you may multiply mean constraints by $|H|$ or $|N|$ if desired; solutions are unchanged.

---

## Minimal data dictionary
- **items.csv**: `item_id`, `name`, `unit`, `stock`, `cost` (optional).
- **nutrients.csv**: `nutrient_id`, `name`, `unit` (optional).
- **households.csv**: `household_id`, `name`, `fairshare_weight` (normalized to 1).
- **requirements.csv**: `household_id`, `nutrient_id`, `requirement`.
- **item_nutrients.csv**: `item_id`, `nutrient_id`, `qty_per_unit`.
- **household_item_bounds.csv**: `household_id`, `item_id`, `lower`, `upper`.
- **scenario YAML**: dial overrides (`alpha`, `beta`, `gamma`, `kappa`, `rho`, `omega`) plus optional `lambda` and budget $B$.

---

**End of document.**
