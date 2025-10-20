# FBDAM Run Report

**Run ID:** `20251020T112527Z_demo`

## Solver summary
- Name: appsi_highs
- Status: TerminationCondition.optimal
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.2311
- Objective Value: 6.526006140350877
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic | {'items': 4.0, 'households': 3.0, 'nutrients': 3.0, 'objective_value': 6.52601} |
| supply | {'total_allocation': 61.0, 'avg_allocation_per_pair': 20.33333, 'undistributed': 0.0, 'total_cost': 9.9} |
| utility | {'total_nutritional_utility': 6.52601, 'global_mean_utility': 0.72511, 'min_mean_utility_per_household': 0.67018, 'min_mean_utility_per_nutrient': 0.37585, 'min_overall_utility': 0.36275} |
| fairness | {'global_mean_deviation_from_fair_share': 1.11111, 'min_mean_deviation_from_fair_share_per_household': 1.0, 'min_mean_deviation_from_fair_share_per_nutrient': 0.44444, 'min_overall_deviation_from_fair_share': -0.0} |

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
