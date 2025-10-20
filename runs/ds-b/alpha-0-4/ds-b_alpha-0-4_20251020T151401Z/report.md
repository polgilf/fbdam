# FBDAM Run Report

**Run ID:** `ds-b_alpha-0-4_20251020T151401Z`

## Solver summary
- Name: mock
- Status: mock
- Termination: not attempted
- Elapsed Sec: 0.0027
- Objective Value: 0.0
- Best Feasible Objective: 0.0
- Best Objective Bound: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic.items | 3.0 |
| basic.households | 2.0 |
| basic.nutrients | 2.0 |
| basic.objective_value | 0.0 |
| supply.total_allocation | 0.0 |
| supply.avg_allocation_per_pair | 0.0 |
| supply.undistributed | 70.0 |
| supply.total_cost | 0.0 |
| utility.total_nutritional_utility | 0.0 |
| utility.global_mean_utility | 0.0 |
| utility.min_mean_utility_per_household | 0.0 |
| utility.min_mean_utility_per_nutrient | 0.0 |
| utility.min_overall_utility | 0.0 |
| fairness.global_mean_deviation_from_fair_share | 0.0 |
| fairness.min_mean_deviation_from_fair_share_per_household | 0.0 |
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
