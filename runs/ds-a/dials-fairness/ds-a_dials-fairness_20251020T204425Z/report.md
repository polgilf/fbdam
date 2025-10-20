# FBDAM Run Report

**Run ID:** `ds-a_dials-fairness_20251020T204425Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1148
- Objective Value: 3.612000000000001
- Best Feasible Objective: 3.612000000000001
- Best Objective Bound: 3.6977777777777776
- Gap: 0.023748

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 3.612 |
| supply.total_allocation | 59.0 |
| supply.avg_allocation_per_pair | 19.66667 |
| supply.undistributed | 2.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 3.612 |
| utility.global_mean_utility | 0.40133 |
| utility.min_mean_utility_per_household | 0.3612 |
| utility.min_mean_utility_per_nutrient | 0.3612 |
| utility.min_overall_utility | 0.3612 |
| fairness.global_mean_deviation_from_fair_share | 0.46296 |
| fairness.min_mean_deviation_from_fair_share_per_household | 0.38889 |
| fairness.min_mean_deviation_from_fair_share_per_nutrient | 0.33333 |
| fairness.min_overall_deviation_from_fair_share | 0.0 |

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
