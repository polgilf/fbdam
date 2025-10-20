# FBDAM Run Report

**Run ID:** `ds-b_alpha-0-6_20251020T154511Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1326
- Objective Value: 4.0
- Best Feasible Objective: 4.0
- Best Objective Bound: 4.0
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic.items | 3.0 |
| basic.households | 2.0 |
| basic.nutrients | 2.0 |
| basic.objective_value | 4.0 |
| supply.total_allocation | 71.0 |
| supply.avg_allocation_per_pair | 35.5 |
| supply.undistributed | 0.0 |
| supply.total_cost | 2.0 |
| utility.total_nutritional_utility | 4.0 |
| utility.global_mean_utility | 1.0 |
| utility.min_mean_utility_per_household | 1.0 |
| utility.min_mean_utility_per_nutrient | 1.0 |
| utility.min_overall_utility | 1.0 |
| fairness.global_mean_deviation_from_fair_share | 0.16667 |
| fairness.min_mean_deviation_from_fair_share_per_household | 0.16667 |
| fairness.min_mean_deviation_from_fair_share_per_nutrient | 0.0 |
| fairness.min_overall_deviation_from_fair_share | 0.0 |

## Model stats
- Vars Total: 29
- Cons Total: 39

**Vars by domain**
- x: 6
- u: 4
- y: 3
- y_active: 3
- dpos: 6
- dneg: 6
- epsilon: 1

**Constraints by block**
- U_link: 4
- StockBalance: 3
- PurchaseBudget: 1
- PurchaseActivation: 3
- PurchaseAllocationEnforcement: 3
- DeviationIdentity: 6
- DeviationItemCap: 3
- DeviationHouseholdCap: 2
- DeviationPairCap: 6
- HouseholdFloor: 2
- NutrientFloor: 2
- PairFloor: 4
