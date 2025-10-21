# Semantic Framework for Equity and Adequacy Terminology in FBDAM

**Version:** 1.0

**Date:** October 2025

**Author:** Pol Gil Figuerola

**Status:** Validated

---

## 1. Introduction

This document establishes the **semantic guiding principles** for terminology used in the Food Basket Design and Allocation Model (FBDAM). Given the project's emphasis on mathematical rigor and operational research precision, clear and consistent terminology is essential to avoid ambiguity between colloquial usage and technical meaning.

FBDAM addresses  **two orthogonal dimensions of distributional justice** : how physical items are allocated and how nutritional outcomes are achieved. Each dimension employs distinct mechanisms and serves different equity goals. This framework ensures that every term maps unambiguously to its underlying mathematical concept.

---

## 2. Core Conceptual Hierarchy

### 2.1 The Umbrella: Equity

**Definition:** Equity is the overarching concept of distributional justice—ensuring that the allocation process produces outcomes that are just, proportional, or adequate according to normative criteria.

**Scope in FBDAM:** Equity encompasses both dimensions of the model:

* How items are distributed among households (allocation)
* How nutritional outcomes are achieved across populations (nutrition)

**Usage Rule:** Use "equity" when:

* Referring to both dimensions collectively
* Discussing distributional justice as a general principle
* Framing the model's ethical foundation

**Never use "equity" when:** Describing procedural mechanisms (e.g., "the equity algorithm" is incorrect; say "the allocation mechanism" or "the optimization procedure").

---

### 2.2 The Two Dimensions

FBDAM enforces equity through two complementary and independent mechanisms:

#### **Dimension 1: Allocation Equity**

* **What it controls:** Inequality in physical distribution of items (decision variable x[i,h])
* **Mathematical mechanism:** L1 deviation constraints (currently L1, but the framework is agnostic to the specific norm or index used) from proportional targets
* **Normative principle:** Proportional fairness (vertical equity)
* **Dials:** α (item), β (household), ρ (pairwise)
* **Constraints:** Equations (3a–3d) (see Model Appendix) in the mathematical model

#### **Dimension 2: Nutritional Adequacy**

* **What it controls:** Inequality in nutritional outcomes (utility variable u[n,h])
* **Mathematical mechanism:** Minimum utility floor constraints
* **Normative principle:** Sufficiency, egalitarian minimums
* **Dials:** γ (nutrient), κ (pairwise), ω (household)
* **Constraints:** Equations (4a–4c) (see Model Appendix) in the mathematical model

---

## 3. Term-by-Term Semantic Definitions

### 3.1 Fairness

**Technical Definition:** A property of allocation mechanisms or rules that ensures impartial, consistent, and justified treatment according to predefined principles.

**In FBDAM Context:** Fairness refers specifically to the **proportional allocation principle** embodied in the fair-share target:

```
fair_share[i,h] = w[h] × Avail[i]
```

where `w[h]` is the household's proportional weight (normalized by total household size).

**Usage Rules:**

✅ **Correct usage:**

* "The fair-share target ensures proportional fairness"
* "Fairness constraints limit deviations from proportional allocation"
* "This policy emphasizes fairness (proportional distribution)"
* Configuration file: `dials-fairness.yaml` (colloquial, policy-oriented)

❌ **Incorrect usage:**

* "The fairness constraint ensures adequate nutrition" (confuses dimensions)
* "Adjust fairness dials to improve outcomes" (ambiguous—which dials?)
* "The fairness floor prevents malnutrition" (floors are adequacy, not fairness)

**Relationship to Other Terms:**

* Fairness is the **normative principle** underlying allocation equity (default meaning of 'equity' in this document)
* The fair-share target is the **mathematical operationalization** of fairness
* Allocation equity constraints are the **mechanism** enforcing fairness

**Context Sensitivity:**

* **Colloquial/policy contexts:** Use "fairness" freely when discussing proportional allocation goals
* **Technical/mathematical contexts:** Prefer "allocation equity (default meaning of 'equity' in this document)" or "proportional allocation constraints"
* **User-facing materials:** "fairness" is acceptable and more accessible than "allocation equity (default meaning of 'equity' in this document)"

---

### 3.2 Equity

**Technical Definition:** A normative property of outcomes where resources, costs, or benefits are distributed according to principles of justice—either proportional (vertical equity) or equal (horizontal equity).

**In FBDAM Context:** Equity has two distinct meanings depending on dimension:

#### **Allocation Equity**

Proportional distribution of physical items according to household size/need.

**Key characteristics:**

* **Mechanism:** L1 deviation caps (α, β, ρ)
* **Target:** Fair-share baseline (`w[h] × Avail[i]`)
* **Type:** Vertical equity (proportional) + horizontal equity (consistency)
* **Measurement:** Sum of absolute deviations from fair-share

**Usage:**

* "Allocation equity constraints limit inequality in distribution"
* "Lower α values enforce stricter allocation equity (default meaning of 'equity' in this document)"
* "The model balances allocation equity (default meaning of 'equity' in this document) with efficiency"

#### **Nutritional Equity**

Achieved through nutritional adequacy constraints (see Section 3.3).

**Usage Rules:**

✅ **Correct usage:**

* "The model enforces two forms of equity: allocation and nutritional"
* "Equity dials control distributional outcomes"
* "Allocation equity promotes proportional treatment"

❌ **Incorrect usage:**

* "The equity algorithm optimizes fairness" (equity is outcome, not procedure)
* "Equity constraints ensure fairness" (too vague—specify dimension)
* Using "equity" when "allocation equity (default meaning of 'equity' in this document)" or "nutritional adequacy" is more precise

**Golden Rule:** When using "equity" in technical writing, **always specify which dimension** unless referring to both collectively.

---

### 3.3 Adequacy

**Technical Definition:** The property of outcomes meeting minimum acceptable thresholds or standards—ensuring sufficiency rather than equality or proportionality.

**In FBDAM Context:** Adequacy refers exclusively to **nutritional outcomes** (utility u[n,h]), never to physical allocation.

**Key characteristics:**

* **Mechanism:** Minimum utility floor constraints (γ, κ, ω)
* **Target:** Fraction of global mean utility
* **Type:** Egalitarian equity (everyone meets minimum)
* **Measurement:** Distance below adequacy thresholds

**Mathematical Form:**

```
mean_utility[dimension] ≥ dial × global_mean_utility - ε
```

**Usage Rules:**

✅ **Correct usage:**

* "Nutritional adequacy constraints ensure minimum utility"
* "Adequacy floors prevent nutritional deprivation"
* "The γ dial controls nutrient-level adequacy"
* "Higher ω values enforce stricter household adequacy"
* Configuration file: `dials-adequacy.yaml`

❌ **Incorrect usage:**

* "Allocation adequacy constraints" (allocation uses equity, not adequacy)
* "Adequacy caps limit deviations" (caps are for equity; floors are for adequacy)
* "The adequacy target is fair-share" (fair-share is allocation; adequacy is nutrition)

**Relationship to Equity:**
Adequacy is a **form of equity** (specifically, egalitarian equity through minimum standards). The distinction:

* **Allocation equity** asks: "Is the distribution proportional?"
* **Nutritional adequacy** asks: "Does everyone meet minimum standards?"

**Semantic Precision:** While adequacy promotes equity (in the broad sense), use "adequacy" for the specific nutritional dimension and "allocation equity (default meaning of 'equity' in this document)" for the distribution dimension.

---

### 3.4 Fair-Share

**Technical Definition:** The proportional allocation target for household h receiving item i, calculated as the household's weight multiplied by total available supply.

**Mathematical Notation:**

```
fair_share[i,h] = w[h] × Avail[i]
where w[h] = members[h] / Σ_k members[k]
```

**Usage Rules:**

✅ **Correct usage:**

* "Deviation from fair-share" (mathematical precision)
* "Fair-share weight w[h]" (the proportional weight)
* "Fair-share target" (the allocation baseline)
* Variable/expression names: `fairshare_weight`, `fairshare_deviation_identity`

❌ **Incorrect usage:**

* "Fair-share utility" (utility is nutritional; fair-share is allocation)
* "Fair-share adequacy" (adequacy is not proportional; fair-share is)

**Semantic Status:** "Fair-share" is a **composite term** (hyphenated) referring to a specific mathematical concept. It is not interchangeable with "fairness" (the principle) or "allocation equity (default meaning of 'equity' in this document)" (the outcome).

**Context:** Fair-share is the **operationalization** of the fairness principle in allocation. It provides the baseline against which allocation equity (default meaning of 'equity' in this document) is measured.

---

### 3.5 Proportional vs. Egalitarian

These adjectives distinguish two types of equity:

#### **Proportional Equity**

* **Definition:** Distribution proportional to a relevant attribute (e.g., household size, need)
* **In FBDAM:** Allocation equity via fair-share (w[h] × Avail[i])
* **Principle:** Vertical equity—unequals treated proportionally to their differences
* **Usage:** "Proportional fairness," "proportional allocation," "proportional targets"

#### **Egalitarian Equity**

* **Definition:** Equal treatment or equal minimums for all, regardless of differences
* **In FBDAM:** Nutritional adequacy floors (everyone ≥ threshold)
* **Principle:** Equal minimums (floors) rather than proportional distribution
* **Usage:** "Egalitarian floors," "egalitarian adequacy," "equal minimum standards"

**Usage Rule:** Use these adjectives to **clarify which type of equity** a constraint enforces:

* "Proportional allocation equity (default meaning of 'equity' in this document)" (α, β, ρ)
* "Egalitarian nutritional adequacy" (γ, κ, ω)

---

## 4. Dimensional Classification Rules

### 4.1 The Two-Question Test

When writing about any model component, ask:

**Question 1:** Which dimension does this belong to?

* **Allocation** (physical distribution, x[i,h], dials α/β/ρ (caps on L1 deviation; lower values = stricter allocation equity))
* **Nutrition** (outcomes, u[n,h], dials γ/κ/ω (floors on utility; higher values = stricter adequacy requirements))

**Question 2:** What is being controlled?

* **Equity** (inequality, deviations, proportionality)
* **Adequacy** (minimums, thresholds, sufficiency)

**Mapping:**

| Dimension  | What's Controlled | Term                 | Dials      |
| ---------- | ----------------- | -------------------- | ---------- |
| Allocation | Equity            | Allocation Equity    | α, β, ρ |
| Nutrition  | Adequacy          | Nutritional Adequacy | γ, κ, ω |

### 4.2 Naming Convention Matrix

Use this matrix to construct technically precise names:

```
<dimension>_<concept>_<scope>_<mechanism>

Examples:
- item_allocation_equity_cap         (allocation + equity + item + cap)
- household_adequacy_floor           (nutrition + adequacy + household + floor)
- pairwise_allocation_equity_cap     (allocation + equity + pairwise + cap)
- nutrient_adequacy_floor            (nutrition + adequacy + nutrient + floor)
```

**Mechanism vocabulary:**

* **Caps/limits:** allocation equity (default meaning of 'equity' in this document) constraints (upper bounds on deviation)
* **Floors:** adequacy constraints (lower bounds on utility)
* **Deviation:** allocation equity (default meaning of 'equity' in this document) measurement (δ⁺ + δ⁻)
* **Utility:** adequacy measurement (u[n,h])

---

## 5. Contextual Usage Guidelines

### 5.1 Code and Mathematical Contexts

**Precision is paramount.** Use full, dimensional terminology:

✅ **Preferred:**

```python
# ALLOCATION EQUITY constraint (α)
@register_constraint("item_allocation_equity_cap")

# NUTRITIONAL ADEQUACY constraint (ω)
@register_constraint("household_adequacy_floor")
```

❌ **Avoid:**

```python
# Vague/ambiguous
@register_constraint("fairness_constraint")
@register_constraint("equity_floor")
```

### 5.2 Documentation and Papers

**Balance precision with readability.** Use full terms on first mention, then abbreviate:

✅ **Good pattern:**

> "FBDAM enforces two forms of equity: **allocation equity (default meaning of 'equity' in this document)** through proportional fair-share constraints (α, β, ρ), and **nutritional adequacy** through minimum utility floors (γ, κ, ω). The allocation equity (default meaning of 'equity' in this document) constraints limit deviations from..."

### 5.3 User-Facing Materials (Configuration, CLI, Reports)

**Accessibility matters.** Use intuitive language with brief clarifications:

✅ **Good pattern:**

```yaml
# configs/dials-fairness.yaml
name: Fairness (Proportional Allocation)
description: |
  Enforces strict proportional allocation. Households receive items
  proportional to their size (allocation equity (default meaning of 'equity' in this document)).
```

### 5.4 Colloquial Discussion

**Shortcuts are acceptable in informal contexts:**

✅ **Acceptable:**

* "The fairness constraints" (when α, β, ρ context is clear)
* "Adequacy floors" (shorthand for nutritional adequacy floors)
* "Equity-efficiency trade-off" (standard OR phrasing)

❌ **Never acceptable (always ambiguous):**

* "The equity constraints" (which dimension?)
* "Fairness floors" (fairness uses caps, not floors)
* "Adequacy caps" (adequacy uses floors, not caps)

---

## 6. Common Pitfalls and Corrections

### Pitfall 1: Conflating Dimensions

❌ "The fairness constraints ensure adequate nutrition"

✅ "The allocation equity (default meaning of 'equity' in this document) constraints enforce proportional distribution, while nutritional adequacy constraints ensure minimum utility"

### Pitfall 2: Mechanism-Goal Confusion

❌ "The fair-share constraint promotes fairness"

✅ "The L1 deviation constraint enforces allocation equity (default meaning of 'equity' in this document) by limiting deviations from the fair-share target"

### Pitfall 3: Vague Dial References

❌ "Adjust the equity dials"

✅ "Adjust the allocation equity (default meaning of 'equity' in this document) dials (α, β, ρ)" OR "Adjust the adequacy dials (γ, κ, ω)"

### Pitfall 4: Mismatched Constraint Names

❌ "The adequacy cap limits inequality"

✅ "The allocation equity (default meaning of 'equity' in this document) cap limits deviations" (caps are for equity, not adequacy)

### Pitfall 5: Procedural vs. Outcome Confusion

❌ "The equity algorithm optimizes fairness"

✅ "The optimization algorithm balances efficiency with allocation equity (default meaning of 'equity' in this document) and nutritional adequacy"

---

## 7. Quick Reference: Terminology Lookup Table

| If You're Describing...                            | Use This Term                    | Never Use         |
| -------------------------------------------------- | -------------------------------- | ----------------- |
| Physical item distribution (x[i,h])                | Allocation equity                | Adequacy          |
| Nutritional outcomes (u[n,h])                      | Nutritional adequacy             | Fairness          |
| Proportional target (w[h] × Avail[i])             | Fair-share                       | Adequacy target   |
| L1 deviation limits (α, β, ρ)                   | Allocation equity constraints    | Fairness floors   |
| Minimum utility thresholds (γ, κ, ω)            | Nutritional adequacy constraints | Equity caps       |
| The normative principle of proportional allocation | Fairness, proportional fairness  | Adequacy          |
| The outcome of enforced proportionality            | Allocation equity                | Fairness          |
| Preventing nutritional deprivation                 | Nutritional adequacy             | Allocation equity |
| Constraint upper bounds                            | Caps                             | Floors            |
| Constraint lower bounds                            | Floors                           | Caps              |

---

## 8. Implementation Mandate

All FBDAM materials—code, documentation, papers, presentations—must adhere to this semantic framework. When ambiguity arises:

1. **Identify the dimension** (allocation vs. nutrition)
2. **Identify the concept** (equity vs. adequacy)
3. **Use the full, precise term** from this framework
4. **Abbreviate only when context is unambiguous**

**Versioning:** This is a  **living document** . If new model components require terminology clarification, update this framework before implementing code changes.

---

## 9.

## Synonym Guardrail (quick reference)

| Say this                        | Not that      |
| ------------------------------- | ------------- |
| **allocation equity cap** | fairness cap  |
| **adequacy floor**        | equity floor  |
| **fair-share target**     | equity target |

Conclusion

Precise terminology is not pedantic—it is  **essential for scientific reproducibility and mathematical coherence** . FBDAM's dual-dimensional equity framework requires clear linguistic boundaries between allocation and nutrition, between proportionality and sufficiency, between fairness as principle and equity as outcome.

By consistently applying these semantic principles, we ensure that:

* **Mathematicians** can map every term to a precise model component
* **Practitioners** understand policy levers without ambiguity
* **Reviewers** can critique the model without linguistic confusion
* **Future developers** extend the system coherently

This framework transforms vocabulary from a communication tool into a **formal specification** of the model's conceptual architecture.

---

**End of Document**
