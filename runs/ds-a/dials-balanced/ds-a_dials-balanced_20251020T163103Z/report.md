# FBDAM Run Report

**Run ID:** `ds-a_dials-balanced_20251020T163103Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1271
- Objective Value: 6.426000000000001
- Best Feasible Objective: 6.426000000000001
- Best Objective Bound: 6.580279898125231
- Gap: 0.024009

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.426 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 1.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 6.426 |
| utility.global_mean_utility | 0.714 |
| utility.min_mean_utility_per_household | 0.65137 |
| utility.min_mean_utility_per_nutrient | 0.37453 |
| utility.min_overall_utility | 0.357 |
| fairness.global_mean_deviation_from_fair_share | 1.06481 |
| fairness.min_mean_deviation_from_fair_share_per_household | 0.55556 |
| fairness.min_mean_deviation_from_fair_share_per_nutrient | 0.44444 |
| fairness.min_overall_deviation_from_fair_share | -0.0 |

## Model stats
- Vars Total: 54
- Cons Total: 68

**Vars by domain**
- x: 12
- u: 9
- y: 4
- y_active: 4
- dpos: 12
- dneg: 12
- epsilon: 1

**Constraints by block**
- U_link: 9
- StockBalance: 4
- PurchaseBudget: 1
- PurchaseActivation: 4
- PurchaseAllocationEnforcement: 4
- DeviationIdentity: 12
- DeviationItemCap: 4
- DeviationHouseholdCap: 3
- DeviationPairCap: 12
- HouseholdFloor: 3
- NutrientFloor: 3
- PairFloor: 9
