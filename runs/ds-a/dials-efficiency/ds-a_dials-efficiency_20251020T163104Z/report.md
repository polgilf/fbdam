# FBDAM Run Report

**Run ID:** `ds-a_dials-efficiency_20251020T163104Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1173
- Objective Value: 6.5061041353383455
- Best Feasible Objective: 6.5061041353383455
- Best Objective Bound: 6.649522965566202
- Gap: 0.022044

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.5061 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 6.5061 |
| utility.global_mean_utility | 0.7229 |
| utility.min_mean_utility_per_household | 0.54054 |
| utility.min_mean_utility_per_nutrient | 0.32482 |
| utility.min_overall_utility | 0.08425 |
| fairness.global_mean_deviation_from_fair_share | 2.22222 |
| fairness.min_mean_deviation_from_fair_share_per_household | 1.08333 |
| fairness.min_mean_deviation_from_fair_share_per_nutrient | 0.88889 |
| fairness.min_overall_deviation_from_fair_share | 0.33333 |

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
