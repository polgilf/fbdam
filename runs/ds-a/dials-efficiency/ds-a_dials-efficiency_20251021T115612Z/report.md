# FBDAM Run Report

**Run ID:** `ds-a_dials-efficiency_20251021T115612Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1279
- Objective Value: 6.48229022556391
- Best Feasible Objective: 6.48229022556391
- Best Objective Bound: 6.6568786466165415
- Gap: 0.026933

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.48229 |
| supply.total_allocation | 59.0 |
| supply.avg_allocation_per_pair | 19.66667 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.0 |
| utility.total_nutritional_utility | 6.48229 |
| utility.global_mean_utility | 0.72025 |
| utility.min_mean_utility_per_household | 0.58865 |
| utility.min_mean_utility_per_nutrient | 0.30207 |
| utility.min_overall_utility | 0.027 |
| fairness.global_mean_deviation_from_fair_share | 2.2037 |
| fairness.max_mean_deviation_from_fair_share_per_household | 3.19444 |
| fairness.max_mean_deviation_from_fair_share_per_food_item | 4.44444 |
| fairness.max_overall_deviation_from_fair_share | 6.66667 |

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
