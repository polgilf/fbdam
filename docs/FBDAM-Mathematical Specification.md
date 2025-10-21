# FBDAM: A Multi-Objective Food Allocation Model

**Mathematical Specification**

**Version:** 1.0 | **Status:** Validated | **Date:** October 2025

---

## 1. Model Overview

FBDAM is a **Mixed-Integer Linear Program** that optimizes food allocation across households while balancing three competing objectives:

* **Nutritional efficiency** : Maximize aggregate utility
* **Distributive equity** : Enforce proportional fairness via L1 deviation constraints
* **Nutritional adequacy** : Guarantee minimum standards relative to global mean

The model features a **six-dimensional control dial system** (α, β, ρ, γ, κ, ω) enabling stakeholders to navigate the Pareto frontier between efficiency, equity, and adequacy objectives.

**Core property:** The base model is always feasible; infeasibility arises from conflicting objectives when dials are overly restrictive.

---

## 2. Mathematical Formulation

### 2.1 Sets and Parameters

**Index sets:**

* $\mathcal{I}$ : Items (food products)
* $\mathcal{N}$ : Nutrients
* $\mathcal{H}$ : Households

**Supply parameters:**

* $S_i \in \mathbb{R}_+$ : Donated stock of item $i$
* $c_i \in \mathbb{R}_+$ : Unit purchase cost

**Nutritional parameters:**

* $a_{i,n} \in \mathbb{R}_+$ : Nutrient $n$ content per unit of item $i$
* $R_{h,n} \in \mathbb{R}_+$ : Requirement of nutrient $n$ for household $h$ (floored at $10^{-9}$)

**Equity parameters:**

* $w_h \in \mathbb{R}_+$ : Fairshare weight (proportionality factor)

**Policy parameters:**

* $B \in \mathbb{R}_+$ : Purchase budget
* $\lambda \in \mathbb{R}_+$ : Slack penalty coefficient

**Control dials:**

* $\alpha_i, \beta_h, \rho_{i,h} \in [0,1]$ : Equity tolerance (item, household, pairwise)
* $\gamma_n, \kappa_{n,h}, \omega_h \in [0,1]$ : Adequacy floors (nutrient, pairwise, household)

---

### 2.2 Decision Variables

**Primary variables:**

$$
\begin{align}
x_{i,h} &\in \mathbb{Z} *+ \text{ or } \mathbb{R}* + && \text{Allocation of item } i \text{ to household } h\
u_{n,h} &\in [0, 1] && \text{Normalized utility of nutrient } n \text{ for household } h
\end{align}
$$

**Purchase variables** (active when budget constraint enabled):

$$
\begin{align}
y_i &\in \mathbb{R}_+ && \text{Purchased quantity of item } i\
y_i^{\text{active}} &\in {0, 1} && \text{Purchase activation indicator}
\end{align}
$$

**Fairness deviation variables:**

$$
\delta^+ *{i,h}, \delta^-* {i,h} \in \mathbb{R}_+ \quad \text{(positive/negative deviation from fairshare)}
$$

**Feasibility slack:**

$$
\varepsilon \in \mathbb{R}_+ \quad \text{(global constraint relaxation variable)}
$$

---

### 2.3 Derived Expressions

**Augmented supply:**

$$
\text{Avail}_i = S_i + y_i
$$

**Delivered nutrients:**

$$
q_{n,h} = \sum_{i \in \mathcal{I}} a_{i,n} \cdot x_{i,h}
$$

**Utility aggregations:**

$$
\begin{align}
\bar{u} *h &= \frac{1}{|\mathcal{N}|} \sum* {n \in \mathcal{N}} u_{n,h} && \text{(household mean)}\\
\bar{u} *n &= \frac{1}{|\mathcal{H}|} \sum* {h \in \mathcal{H}} u_{n,h} && \text{(nutrient mean)}\\
\bar{u}^{\text{global}} &= \frac{1}{|\mathcal{N}| \cdot |\mathcal{H}|} \sum_{n,h} u_{n,h} && \text{(global mean)}
\end{align}
$$

---

### 2.4 Complete Formulation

$$
\begin{align}
\max \quad & \sum_{n \in \mathcal{N}} \sum_{h \in \mathcal{H}} u_{n,h} - \lambda \cdot \varepsilon && \text{(Objective)}\\


\text{s.t.} \quad & u_{n,h} \leq \frac{q_{n,h}}{R_{h,n}} && \forall n, h && \text{(Utility mapping)}\\


& \sum_{h \in \mathcal{H}} x_{i,h} \leq \text{Avail}_i && \forall i && \text{(Supply limit)}\\


& \sum_{i \in \mathcal{I}} c_i \cdot y_i \leq B && && \text{(Budget)}\\
& y_i \leq \frac{B}{c_i} \cdot y_i^{\text{active}} && \forall i && \text{(Purchase activation)}\\
& \text{Avail} *i - \sum_h x* {i,h} \leq S_i (1 - y_i^{\text{active}}) && \forall i && \text{(No-waste on purchase)}\\


& x_{i,h} - w_h \cdot \text{Avail} *i = \delta^+* {i,h} - \delta^- *{i,h} && \forall i, h && \text{(Deviation identity)}\\
& \sum_h (\delta^+* {i,h} + \delta^- *{i,h}) \leq \alpha_i \cdot \text{Avail} *i && \forall i && \text{(Item equity cap)}\\
& \sum_i (\delta^+* {i,h} + \delta^-* {i,h}) \leq \beta_h \cdot \text{TotSupply} && \forall h && \text{(Household equity cap)}\\
& \delta^+ *{i,h} + \delta^-* {i,h} \leq \rho_{i,h} \cdot \text{Avail}_i && \forall i, h && \text{(Pairwise equity cap)}\\

& \bar{u} *h - \omega_h \cdot \bar{u}^{\text{global}} \geq -\varepsilon && \forall h && \text{(Household floor)}\\
& \bar{u} *n - \gamma_n \cdot \bar{u}^{\text{global}} \geq -\varepsilon && \forall n && \text{(Nutrient floor)}\\
& u* {n,h} - \kappa* {n,h} \cdot \bar{u}^{\text{global}} \geq -\varepsilon && \forall n, h && \text{(Pairwise floor)}
\end{align}
$$

**Domain constraints:**

$$
x_{i,h} \geq 0, \quad u_{n,h} \in [0,1], \quad y_i \geq 0, \quad y_i^{\text{active}} \in {0,1}, \quad \delta^\pm_{i,h} \geq 0, \quad \varepsilon \geq 0
$$

---

## 3. Constraint Architecture

### 3.1 Core Mechanics Layer

**Utility mapping** links allocation to nutritional outcomes through a normalized utility function bounded at 1 to prevent over-satisfaction. This creates a **concave relationship** between allocation and marginal benefit.

**Supply limits** enforce physical constraints: total allocation cannot exceed available supply (donated stock plus purchases).

**Purchase system** implements a three-part mechanism:

1. Budget constraint caps total spending
2. Big-M activation forces binary purchase decisions
3. No-waste constraint requires full utilization of purchased items

**Interpretation:** The no-waste constraint prevents purchasing items that would remain unallocated, ensuring efficient budget utilization. Mathematically: if $y_i^{\text{active}} = 1$, then all units of item $i$ (stock + purchase) must be allocated.

---

### 3.2 Equity Layer (L1 Fairness)

The equity system minimizes **L1 deviations** from proportional fairshare targets: $w_h \cdot \text{Avail}_i$.

**Deviation decomposition** splits allocation error into positive/negative components, enabling linear programming formulation of $|x_{i,h} - w_h \cdot \text{Avail}_i|$.

**Three-level control:**

* **Item-level** ($\alpha_i$): Total deviation across households for item $i$
* **Household-level** ($\beta_h$): Total deviation across items for household $h$
* **Pairwise** ($\rho_{i,h}$): Individual (item, household) deviation

**Design rationale:** This hierarchy allows flexible equity enforcement—strict at aggregate level while permitting local optimization, or vice versa.

---

### 3.3 Adequacy Layer (Relative Floors)

Adequacy constraints guarantee **minimum nutritional standards** relative to the endogenous global mean utility. This creates **homogeneity** across heterogeneous nutrients and households.

**Key insight:** Floors are defined as $\text{group_mean} \geq \delta \cdot \bar{u}^{\text{global}}$ rather than absolute thresholds. This ensures:

1. **Scale invariance** : Works across different supply scenarios
2. **Endogenous benchmarking** : Standards adjust to what's achievable
3. **Equity-adequacy coupling** : High adequacy dials push toward equality

**Three-level structure** mirrors equity system:

* **Household-level** ($\omega_h$): Average utility across nutrients for household $h$
* **Nutrient-level** ($\gamma_n$): Average utility across households for nutrient $n$
* **Pairwise** ($\kappa_{n,h}$): Individual (nutrient, household) utility

---

### 3.4 Slack Mechanism

The global slack $\varepsilon$ enables **soft constraint formulation** with tunable enforcement via penalty $\lambda$:

$$
\text{Adequacy constraint: } \quad g(\mathbf{x}, \mathbf{u}) \geq -\varepsilon
$$

**Penalty interpretation:**

| $\lambda$ | Regime     | Constraint type                          |
| ----------- | ---------- | ---------------------------------------- |
| 0           | Diagnostic | Maximizes slack (measures infeasibility) |
| $(0, 1]$  | Soft       | Gentle relaxation preferred              |
| $(1, 10]$ | Moderate   | Balanced trade-off                       |
| $> 10$    | Near-hard  | Strong compliance requirement            |
| $\infty$  | Hard       | No relaxation (omit$\varepsilon$)      |

**Operational use:** Run with $\lambda = 0$ to diagnose constraint conflicts, then incrementally increase to find acceptable feasibility-compliance trade-off.

---

## 4. Mathematical Properties

### 4.1 Problem Classification

**LP formulation** (continuous allocation, no purchases):

* Convex optimization problem
* Global optimum guaranteed
* Polynomial-time solvable

**MILP formulation** (integer allocation or purchases enabled):

* NP-hard in general
* Binary variables: $O(|\mathcal{I}|)$ for purchases
* Integer variables: $O(|\mathcal{I}| \cdot |\mathcal{H}|)$ for allocations
* Practical instances tractable with modern solvers (HiGHS)

---

### 4.2 Fundamental Trade-offs

**Efficiency vs. Equity:**

Maximizing TNU may concentrate allocation on households with favorable requirement-to-utility ratios. Equity constraints force redistribution toward proportionality, potentially reducing aggregate utility.

**Equity vs. Adequacy:**

Proportional allocation (enforced by low $\alpha, \beta, \rho$) may violate nutritional floors for households with high needs but low fairshare weights. Resolution requires either:

* Relaxing equity constraints ($\alpha, \beta, \rho \uparrow$)
* Relaxing adequacy floors ($\gamma, \kappa, \omega \downarrow$)
* Enabling slack ($\varepsilon > 0$, $\lambda$ moderate)
* Increasing supply (purchases or donations)

**Mathematical characterization:**

The Pareto frontier is determined by dial configuration. The model provides a **scalarization** of the multi-objective problem:

$$
\max \quad f(\mathbf{x}) \quad \text{s.t.} \quad g_{\text{equity}}(\mathbf{x}) \leq \alpha, \quad g_{\text{adequacy}}(\mathbf{x}) \geq -\varepsilon
$$

Different $(\alpha, \gamma, \lambda)$ configurations trace out different points on the Pareto surface.

---

### 4.3 Feasibility Landscape

**Base model** (utility mapping + supply limits only): Always feasible (trivial solution $x = 0, u = 0$).

**Infeasibility sources:**

1. **Logical impossibility** : $\omega_h = \gamma_n = \kappa_{n,h} = 1$ simultaneously (all groups cannot be at global mean)
2. **Supply scarcity** : $\sum_i S_i \cdot \max_n a_{i,n} < \sum_h R_{h,n}$ with high adequacy dials
3. **Equity-adequacy conflict** : Strict proportionality ($\alpha, \beta \to 0$) with heterogeneous needs and high floors ($\omega, \gamma \to 1$)
4. **Budget insufficiency** : Low $B$ with purchase-dependent adequacy satisfaction

**Diagnostic protocol:**

1. Solve with $\lambda = 0$: obtain $\varepsilon^* = $ measure of infeasibility
2. Identify binding constraints via shadow prices
3. Systematically relax dials or increase supply until $\varepsilon^* = 0$

---

## 5. Control Dial Semantics

### 5.1 Equity Dials (α, β, ρ)

**Operational interpretation:** Maximum acceptable L1 deviation as fraction of available supply.

**Calibration guidance:**

$$
\begin{align}
\alpha_i &\in [0.1, 0.3]: && \text{Strict item-level proportionality}\
\beta_h &\in [0.3, 0.6]: && \text{Moderate household-level flexibility}\
\rho_{i,h} &\in [0.5, 1.0]: && \text{High local optimization freedom}
\end{align}
$$

**Stakeholder perspectives:**

* **Community-based distribution** : Low $\alpha, \beta$ (accountability to proportional fairness)
* **Efficiency-first programs** : High $\alpha, \beta$ (optimize freely)
* **Hybrid approaches** : Moderate aggregate ($\beta \approx 0.5$), flexible pairwise ($\rho \approx 0.8$)

---

### 5.2 Adequacy Dials (γ, κ, ω)

**Operational interpretation:** Minimum acceptable utility as fraction of global mean.

**Calibration guidance:**

$$
\begin{align}
\omega_h &\in [0.6, 0.8]: && \text{Moderate household floors (emergency response)}\
\gamma_n &\in [0.7, 0.9]: && \text{Strong nutrient floors (public health mandate)}\
\kappa_{n,h} &\in [0.5, 0.7]: && \text{Targeted vulnerability protection}
\end{align}
$$

**Legal/regulatory mapping:**

* **Minimum dietary requirements** : Set $\gamma_n$ per regulatory standard
* **Vulnerable group protection** : Set $\omega_h$ high for identified populations
* **Universal adequacy** : Set $\kappa_{n,h} \geq 0.8$ uniformly

---

### 5.3 Configuration Archetypes

**Pure Efficiency** (no equity/adequacy constraints):

```
dials: {}
```

→ Maximum TNU, potentially highly unequal

**Equity-First** (low equity dials, weak adequacy):

```
α=0.2, β=0.2, ω=0.3
```

→ Near-proportional allocation, moderate nutritional outcomes

**Adequacy-First** (high adequacy, weak equity):

```
γ=0.85, ω=0.85, α=0.8
```

→ High nutritional minimums, flexible distribution

**Balanced** (moderate all dials, soft slack):

```
α=β=γ=ω=0.5, λ=0.5
```

→ Compromise across objectives, soft constraint relaxation

**Diagnostic/Hard** (extreme dials, diagnostic slack):

```
α=β=0, γ=ω=1, λ=0
```

→ Likely infeasible, reveals constraint conflicts via $\varepsilon^*$

---

## 6. Implementation Considerations

### 6.1 Numerical Stability

* Floor $R_{h,n}$ at $10^{-9}$ to prevent division by zero in utility mapping
* Use $\varepsilon_{\text{cost}} = 10^{-9}$ in big-M computation: $M_i = B / (c_i + \varepsilon_{\text{cost}})$
* Recommended solver tolerances: `primal_feasibility: 1e-7`, `dual_feasibility: 1e-7`

---

### 6.2 Solver Configuration

**Primary:** APPSI-HiGHS (fast, modern interface)

**Fallback:** Classic HiGHS (broader compatibility)

**Typical performance:**

* Small (< 1K vars): < 1s
* Medium (1K–10K vars): 1–10s
* Large (10K–100K vars): 10s–5min

**Key options:**

```yaml
solver:
  name: appsi_highs
  options:
    time_limit: 300
    mip_rel_gap: 0.001
```

---

### 6.3 Validation Protocol

Before deployment:

1. **Feasibility test** : Verify solution on representative data
2. **Sensitivity analysis** : Vary dials ±20%, confirm reasonable response
3. **Boundary testing** : Run with extreme dial values (0 and 1)
4. **Purchase logic test** : Confirm no-waste constraint prevents unused purchases
5. **Reproducibility** : Version-control scenario YAML, document solver version

---

## 7. Extensions and Future Directions

 **Multi-period planning** : Add time dimension with inventory dynamics

 **Stochastic requirements** : Two-stage formulation with uncertain $R_{h,n}$

 **Spatial optimization** : Add warehouse locations and transportation costs

 **Preference constraints** : Binary compatibility indicators (cultural/religious/dietary)

 **Bioavailability modeling** : Non-linear nutrient absorption functions (MINLP)

 **Pareto analysis** : Solve parametric family to map efficiency-equity-adequacy frontier

---

## 8. Theoretical Context

### 8.1 Fairness Concepts

 **L1 proportional fairness** : Minimizes total absolute deviation from proportional targets (utilitarian with inequality aversion)

 **Maximin adequacy** : Adequacy floors implement Rawlsian concern for worst-off groups (maximize minimum utility)

 **Hybrid approach** : Model combines both via weighted objective and hierarchical constraints

---

### 8.2 Optimization Theory

 **Scalarization** : Multi-objective problem converted to single-objective via control dials

 **Constraint generation** : Equity/adequacy constraints added modularly (catalog-driven)

 **Penalty methods** : Slack with penalty implements exterior penalty approach to constrained optimization

 **Shadow prices** : Dual variables reveal marginal value of:

* Budget relaxation ($/unit increase in $B$)
* Supply augmentation (utility/unit increase in $S_i$)
* Adequacy floor relaxation (utility/unit decrease in $\gamma, \omega, \kappa$)

---

## Appendix: Notation Summary

| Symbol                                            | Domain                                 | Description                    |
| ------------------------------------------------- | -------------------------------------- | ------------------------------ |
| $\mathcal{I}, \mathcal{N}, \mathcal{H}$         | Index sets                             | Items, nutrients, households   |
| $S_i, c_i$                                      | $\mathbb{R}_+$                       | Stock, unit cost               |
| $a_{i,n}, R_{h,n}$                              | $\mathbb{R}_+$                       | Nutrient content, requirement  |
| $w_h$                                           | $\mathbb{R}_+$                       | Fairshare weight               |
| $\alpha, \beta, \rho$                           | $[0,1]$                              | Equity tolerance dials         |
| $\gamma, \kappa, \omega$                        | $[0,1]$                              | Adequacy floor dials           |
| $B, \lambda$                                    | $\mathbb{R}_+$                       | Budget, slack penalty          |
| $x_{i,h}$                                       | $\mathbb{Z} *+$ or $\mathbb{R}* +$ | Allocation (decision variable) |
| $u_{n,h}$                                       | $[0,1]$                              | Utility (decision variable)    |
| $y_i, y_i^{\text{active}}$                      | $\mathbb{R}_+, {0,1}$                | Purchase quantity, activation  |
| $\delta^{\pm}_{i,h}$                            | $\mathbb{R}_+$                       | Deviation from fairshare       |
| $\varepsilon$                                   | $\mathbb{R}_+$                       | Global slack                   |
| $\bar{u}_h, \bar{u}_n, \bar{u}^{\text{global}}$ | $[0,1]$                              | Mean utilities (expressions)   |

---

**Document Status:** Validated

**Maintained By:** FBDAM Development Team

**Version Control:** See repository changelog

**END OF SPECIFICATION**
