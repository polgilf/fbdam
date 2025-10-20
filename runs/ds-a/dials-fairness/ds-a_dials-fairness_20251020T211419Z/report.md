# FBDAM Run Report

**Run ID:** `ds-a_dials-fairness_20251020T211419Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1159
- Objective Value: 3.6350000000000007
- Best Feasible Objective: 3.6350000000000007
- Best Objective Bound: 3.697777777777776
- Gap: 0.01727

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 3.635 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 1.0 |
| supply.total_cost | 9.9 |
| utility.total_nutritional_utility | 3.635 |
| utility.global_mean_utility | 0.40389 |
| utility.min_mean_utility_per_household | 0.3635 |
| utility.min_mean_utility_per_nutrient | 0.3635 |
| utility.min_overall_utility | 0.3635 |
| fairness.global_mean_deviation_from_fair_share | 0.32407 |
| fairness.max_mean_deviation_from_fair_share_per_household | 0.38889 |
| fairness.max_mean_deviation_from_fair_share_per_nutrient | 0.44444 |
| fairness.max_overall_deviation_from_fair_share | 0.66667 |

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
