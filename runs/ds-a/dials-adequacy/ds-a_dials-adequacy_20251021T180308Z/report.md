# FBDAM Run Report

**Run ID:** `ds-a_dials-adequacy_20251021T180308Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1258
- Objective Value: 3.6350000000000002
- Best Feasible Objective: 3.6350000000000002
- Best Objective Bound: 3.6812222222222215
- Gap: 0.012716

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 3.635 |
| supply.total_allocation | 61.0 |
| supply.avg_allocation_per_pair | 20.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 3.635 |
| utility.global_mean_utility | 0.40389 |
| utility.min_mean_utility_per_household | 0.3635 |
| utility.min_mean_utility_per_nutrient | 0.3635 |
| utility.min_overall_utility | 0.3635 |
| fairness.global_mean_deviation_from_fair_share | 0.2963 |
| fairness.max_mean_deviation_from_fair_share_per_household | 0.38889 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 0.44444 |
| fairness.max_overall_deviation_from_fair_share | 0.66667 |
| fairness.max_relative_deviation_from_fair_share_per_household | 0.19672 |
| fairness.max_relative_deviation_from_fair_share_per_food_item | 0.02186 |
| fairness.max_relative_deviation_from_fair_share_per_pair | 0.28571 |

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
