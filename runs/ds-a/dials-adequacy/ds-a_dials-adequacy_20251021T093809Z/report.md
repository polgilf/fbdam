# FBDAM Run Report

**Run ID:** `ds-a_dials-adequacy_20251021T093809Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1098
- Objective Value: 6.566182604237867
- Best Feasible Objective: 6.566182604237867
- Best Objective Bound: 6.653727117794486
- Gap: 0.013333

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.56618 |
| supply.total_allocation | 59.0 |
| supply.avg_allocation_per_pair | 19.66667 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.0 |
| utility.total_nutritional_utility | 6.56618 |
| utility.global_mean_utility | 0.72958 |
| utility.min_mean_utility_per_household | 0.56137 |
| utility.min_mean_utility_per_nutrient | 0.32468 |
| utility.min_overall_utility | 0.08625 |
| fairness.global_mean_deviation_from_fair_share | 2.12963 |
| fairness.max_mean_deviation_from_fair_share_per_household | 3.19444 |
| fairness.max_mean_deviation_from_fair_share_per_nutrient | 3.85185 |
| fairness.max_overall_deviation_from_fair_share | 5.77778 |

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
