# FBDAM Run Report

**Run ID:** `20251020T112507Z_demo_efficiency`

## Solver summary
- Name: appsi_highs
- Status: TerminationCondition.optimal
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1468
- Objective Value: 6.646217293233082
- Gap: 3.4e-05

## KPIs
| Metric | Value |
|---|---|
| basic | {'items': 4.0, 'households': 3.0, 'nutrients': 3.0, 'objective_value': 6.64622} |
| supply | {'total_allocation': 60.0, 'avg_allocation_per_pair': 20.0, 'undistributed': 0.0, 'total_cost': 10.0} |
| utility | {'total_nutritional_utility': 6.64622, 'global_mean_utility': 0.73847, 'min_mean_utility_per_household': 0.58804, 'min_mean_utility_per_nutrient': 0.3451, 'min_overall_utility': 0.1475} |
| fairness | {'global_mean_deviation_from_fair_share': 2.05556, 'min_mean_deviation_from_fair_share_per_household': 1.08333, 'min_mean_deviation_from_fair_share_per_nutrient': 0.88889, 'min_overall_deviation_from_fair_share': 0.33333} |

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
