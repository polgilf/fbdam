# FBDAM Run Report

**Run ID:** `ds-a_dials-fairness_20251021T180309Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1373
- Objective Value: 5.953117794486216
- Best Feasible Objective: 5.953117794486216
- Best Objective Bound: 6.206710507328928
- Gap: 0.042598

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 5.95312 |
| supply.total_allocation | 58.0 |
| supply.avg_allocation_per_pair | 19.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.5 |
| utility.total_nutritional_utility | 5.95312 |
| utility.global_mean_utility | 0.66146 |
| utility.min_mean_utility_per_household | 0.62213 |
| utility.min_mean_utility_per_nutrient | 0.18867 |
| utility.min_overall_utility | 0.154 |
| fairness.global_mean_deviation_from_fair_share | 0.2037 |
| fairness.max_mean_deviation_from_fair_share_per_household | 0.25 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 0.2963 |
| fairness.max_overall_deviation_from_fair_share | 0.44444 |
| fairness.max_relative_deviation_from_fair_share_per_household | 0.06897 |
| fairness.max_relative_deviation_from_fair_share_per_food_item | 0.01533 |
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
