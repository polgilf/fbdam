# FBDAM Run Report

**Run ID:** `ds-a_dials-efficiency_20251020T211418Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1279
- Objective Value: 6.600400843016632
- Best Feasible Objective: 6.600400843016632
- Best Objective Bound: 6.655368820909041
- Gap: 0.008328

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.6004 |
| supply.total_allocation | 59.0 |
| supply.avg_allocation_per_pair | 19.66667 |
| supply.undistributed | 1.0 |
| supply.total_cost | 10.0 |
| utility.total_nutritional_utility | 6.6004 |
| utility.global_mean_utility | 0.73338 |
| utility.min_mean_utility_per_household | 0.58223 |
| utility.min_mean_utility_per_nutrient | 0.32323 |
| utility.min_overall_utility | 0.0855 |
| fairness.global_mean_deviation_from_fair_share | 2.13889 |
| fairness.max_mean_deviation_from_fair_share_per_household | 3.33333 |
| fairness.max_mean_deviation_from_fair_share_per_nutrient | 3.85185 |
| fairness.max_overall_deviation_from_fair_share | 5.77778 |

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
