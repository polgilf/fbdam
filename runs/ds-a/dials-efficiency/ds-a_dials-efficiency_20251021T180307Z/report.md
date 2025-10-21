# FBDAM Run Report

**Run ID:** `ds-a_dials-efficiency_20251021T180307Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1356
- Objective Value: 6.740140555935293
- Best Feasible Objective: 6.740140555935293
- Best Objective Bound: 6.762775856325581
- Gap: 0.003358

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.74014 |
| supply.total_allocation | 61.0 |
| supply.avg_allocation_per_pair | 20.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 10.0 |
| utility.total_nutritional_utility | 6.74014 |
| utility.global_mean_utility | 0.7489 |
| utility.min_mean_utility_per_household | 0.58334 |
| utility.min_mean_utility_per_nutrient | 0.4127 |
| utility.min_overall_utility | 0.2075 |
| fairness.global_mean_deviation_from_fair_share | 2.09259 |
| fairness.max_mean_deviation_from_fair_share_per_household | 3.13889 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 3.40741 |
| fairness.max_overall_deviation_from_fair_share | 5.11111 |
| fairness.max_relative_deviation_from_fair_share_per_household | 0.57377 |
| fairness.max_relative_deviation_from_fair_share_per_food_item | 0.16758 |
| fairness.max_relative_deviation_from_fair_share_per_pair | 0.875 |

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
- HouseholdFloor: 3
- NutrientFloor: 3
- PairFloor: 9
- DeviationIdentity: 12
- DeviationItemCap: 4
- DeviationHouseholdCap: 3
- DeviationPairCap: 12
