# FBDAM Run Report

**Run ID:** `ds-a_dials-balanced_20251020T221316Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.179
- Objective Value: 6.5232
- Best Feasible Objective: 6.5232
- Best Objective Bound: 6.5356266798871285
- Gap: 0.001905

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.5232 |
| supply.total_allocation | 61.0 |
| supply.avg_allocation_per_pair | 20.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 6.5232 |
| utility.global_mean_utility | 0.7248 |
| utility.min_mean_utility_per_household | 0.67018 |
| utility.min_mean_utility_per_nutrient | 0.37252 |
| utility.min_overall_utility | 0.3624 |
| fairness.global_mean_deviation_from_fair_share | 1.07407 |
| fairness.max_mean_deviation_from_fair_share_per_household | 1.25 |
| fairness.max_mean_deviation_from_fair_share_per_nutrient | 2.07407 |
| fairness.max_overall_deviation_from_fair_share | 3.11111 |

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
