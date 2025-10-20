# FBDAM Run Report

**Run ID:** `20251020T101858Z_demo`

## Solver summary
- Name: appsi_highs
- Status: TerminationCondition.optimal
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1873
- Objective Value: 3.211999999999999
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic | {'items': 4, 'households': 3, 'nutrients': 3, 'objective_value': 3.211999999999999} |
| supply | {'total_allocation': 59.0, 'avg_allocation_per_pair': 19.666666666666668, 'undistributed': 1.6800000020160013, 'total_cost': 10.0} |
| total_nutritional_utility | 3.212 |
| global_mean_utility | 0.3569 |
| min_mean_utility_per_household | 0.3212 |

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
