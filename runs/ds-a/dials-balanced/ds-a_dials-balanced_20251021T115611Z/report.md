# FBDAM Run Report

**Run ID:** `ds-a_dials-balanced_20251021T115611Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1216
- Objective Value: 6.469062087035772
- Best Feasible Objective: 6.469062087035772
- Best Objective Bound: 6.641027009189641
- Gap: 0.026583

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.46906 |
| supply.total_allocation | 58.0 |
| supply.avg_allocation_per_pair | 19.33333 |
| supply.undistributed | 1.0 |
| supply.total_cost | 8.4 |
| utility.total_nutritional_utility | 6.46906 |
| utility.global_mean_utility | 0.71878 |
| utility.min_mean_utility_per_household | 0.56251 |
| utility.min_mean_utility_per_nutrient | 0.36017 |
| utility.min_overall_utility | 0.2055 |
| fairness.global_mean_deviation_from_fair_share | 1.71296 |
| fairness.max_mean_deviation_from_fair_share_per_household | 2.69444 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 2.66667 |
| fairness.max_overall_deviation_from_fair_share | 4.0 |

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
