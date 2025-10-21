# FBDAM Run Report

**Run ID:** `ds-a_dials-hard-fairness_20251021T115617Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1267
- Objective Value: 6.327255692007798
- Best Feasible Objective: 6.327255692007798
- Best Objective Bound: 6.501736950166806
- Gap: 0.027576

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.32726 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 1.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 6.36505 |
| utility.global_mean_utility | 0.70723 |
| utility.min_mean_utility_per_household | 0.656 |
| utility.min_mean_utility_per_nutrient | 0.38055 |
| utility.min_overall_utility | 0.32925 |
| fairness.global_mean_deviation_from_fair_share | 0.76852 |
| fairness.max_mean_deviation_from_fair_share_per_household | 1.22222 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 1.22222 |
| fairness.max_overall_deviation_from_fair_share | 2.11111 |

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
