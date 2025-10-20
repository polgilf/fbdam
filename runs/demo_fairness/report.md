# FBDAM Run Report

**Run ID:** `demo_fairness_20251020T131358Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1556
- Objective Value: 3.212000000000005
- Best Feasible Objective: 3.212000000000005
- Best Objective Bound: 3.212000000000005
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 3.212 |
| supply.total_allocation | 59.0 |
| supply.avg_allocation_per_pair | 19.66667 |
| supply.undistributed | 1.0 |
| supply.total_cost | 9.2 |
| utility.total_nutritional_utility | 3.212 |
| utility.global_mean_utility | 0.35689 |
| utility.min_mean_utility_per_household | 0.3212 |
| utility.min_mean_utility_per_nutrient | 0.3212 |
| utility.min_overall_utility | 0.3212 |
| fairness.global_mean_deviation_from_fair_share | 0.28704 |
| fairness.min_mean_deviation_from_fair_share_per_household | 0.16667 |
| fairness.min_mean_deviation_from_fair_share_per_nutrient | 0.0 |
| fairness.min_overall_deviation_from_fair_share | -0.0 |

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
