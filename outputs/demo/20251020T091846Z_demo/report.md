# FBDAM Run Report

**Run ID:** `20251020T091846Z_demo`

## Solver summary
- Name: appsi_highs
- Status: TerminationCondition.optimal
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.407
- Objective Value: 3.2120000000000015
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| items | 4 |
| households | 3 |
| nutrients | 3 |
| objective_value | 3.212 |
| total_allocation | 60.0 |
| avg_allocation_per_pair | 5.0 |
| mean_utility | 0.3569 |
| min_mean_utility_per_household | 0.3212 |
| min_mean_utility_per_nutrient | 0.3212 |
| min_overall_utility | 0.3212 |
| global_mean_deviation_from_fair_share | 0.0476 |
| min_mean_deviation_per_household | 0.0357 |
| min_mean_deviation_per_nutrient | 0.0 |
| min_overall_deviation_from_fair_share | 0.0 |

## Model stats
- Vars Total: 50
- Cons Total: 60

**Vars by domain**
- x: 12
- u: 9
- y: 4
- dpos: 12
- dneg: 12
- epsilon: 1

**Constraints by block**
- U_link: 9
- StockBalance: 4
- PurchaseBudget: 1
- DeviationIdentity: 12
- DeviationItemCap: 4
- DeviationHouseholdCap: 3
- DeviationPairCap: 12
- HouseholdFloor: 3
- NutrientFloor: 3
- PairFloor: 9
