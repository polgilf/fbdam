# FBDAM Run Report

**Run ID:** `ds-a_dials-gradual_20251021T180312Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1241
- Objective Value: 2.63
- Best Feasible Objective: 2.63
- Best Objective Bound: 2.646374240257418
- Gap: 0.006226

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 2.63 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.3 |
| utility.total_nutritional_utility | 2.63 |
| utility.global_mean_utility | 0.29222 |
| utility.min_mean_utility_per_household | 0.263 |
| utility.min_mean_utility_per_nutrient | 0.263 |
| utility.min_overall_utility | 0.263 |
| fairness.global_mean_deviation_from_fair_share | 0.11111 |
| fairness.max_mean_deviation_from_fair_share_per_household | 0.16667 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 0.22222 |
| fairness.max_overall_deviation_from_fair_share | 0.33333 |
| fairness.max_relative_deviation_from_fair_share_per_household | 0.1 |
| fairness.max_relative_deviation_from_fair_share_per_food_item | 0.01111 |
| fairness.max_relative_deviation_from_fair_share_per_pair | 0.25 |

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
- PurchaseNoWaste: 4
- DeviationIdentity: 12
- DeviationItemCap: 4
- DeviationHouseholdCap: 3
- DeviationPairCap: 12
- HouseholdFloor: 3
- NutrientFloor: 3
- PairFloor: 9
