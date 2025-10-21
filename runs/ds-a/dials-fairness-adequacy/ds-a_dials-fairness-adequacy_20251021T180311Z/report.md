# FBDAM Run Report

**Run ID:** `ds-a_dials-fairness-adequacy_20251021T180311Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1221
- Objective Value: 1.5400000000000003
- Best Feasible Objective: 1.5400000000000003
- Best Objective Bound: 1.5400000000000003
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 1.54 |
| supply.total_allocation | 56.0 |
| supply.avg_allocation_per_pair | 18.66667 |
| supply.undistributed | 1.0 |
| supply.total_cost | 8.3 |
| utility.total_nutritional_utility | 1.54 |
| utility.global_mean_utility | 0.17111 |
| utility.min_mean_utility_per_household | 0.154 |
| utility.min_mean_utility_per_nutrient | 0.154 |
| utility.min_overall_utility | 0.154 |
| fairness.global_mean_deviation_from_fair_share | 0.23148 |
| fairness.max_mean_deviation_from_fair_share_per_household | 0.36111 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 0.59259 |
| fairness.max_overall_deviation_from_fair_share | 0.88889 |
| fairness.max_relative_deviation_from_fair_share_per_household | 0.05263 |
| fairness.max_relative_deviation_from_fair_share_per_food_item | 0.03119 |
| fairness.max_relative_deviation_from_fair_share_per_pair | 0.1 |

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
