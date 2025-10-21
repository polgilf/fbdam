# FBDAM Run Report

**Run ID:** `ds-a_dials-balanced_20251021T093805Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1228
- Objective Value: 6.594431704260652
- Best Feasible Objective: 6.594431704260652
- Best Objective Bound: 6.641027009189641
- Gap: 0.007066

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.59443 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.6 |
| utility.total_nutritional_utility | 6.59443 |
| utility.global_mean_utility | 0.73271 |
| utility.min_mean_utility_per_household | 0.6043 |
| utility.min_mean_utility_per_nutrient | 0.36158 |
| utility.min_overall_utility | 0.20975 |
| fairness.global_mean_deviation_from_fair_share | 1.55556 |
| fairness.max_mean_deviation_from_fair_share_per_household | 2.33333 |
| fairness.max_mean_deviation_from_fair_share_per_nutrient | 2.66667 |
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
