# FBDAM Run Report

**Run ID:** `20251020T112519Z_demo_fairness`

## Solver summary
- Name: appsi_highs
- Status: TerminationCondition.optimal
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.2516
- Objective Value: 3.212000000000001
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic | {'items': 4.0, 'households': 3.0, 'nutrients': 3.0, 'objective_value': 3.212} |
| supply | {'total_allocation': 60.0, 'avg_allocation_per_pair': 20.0, 'undistributed': 0.0, 'total_cost': 9.2} |
| utility | {'total_nutritional_utility': 3.212, 'global_mean_utility': 0.35689, 'min_mean_utility_per_household': 0.3212, 'min_mean_utility_per_nutrient': 0.3212, 'min_overall_utility': 0.3212} |
| fairness | {'global_mean_deviation_from_fair_share': 0.48981, 'min_mean_deviation_from_fair_share_per_household': 0.25, 'min_mean_deviation_from_fair_share_per_nutrient': 0.3, 'min_overall_deviation_from_fair_share': -0.0} |

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
