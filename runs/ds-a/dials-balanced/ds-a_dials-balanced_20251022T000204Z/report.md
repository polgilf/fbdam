# FBDAM Run Report

**Run ID:** `ds-a_dials-balanced_20251022T000204Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1503
- Objective Value: 5.484
- Best Feasible Objective: 5.484
- Best Objective Bound: 5.485384615384616
- Gap: 0.000252

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 5.484 |
| supply.total_allocation | 61.0 |
| supply.avg_allocation_per_pair | 20.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.9 |
| nutrition.total_nutritional_utility | 5.484 |
| nutrition.global_mean_utility | 0.60933 |
| nutrition.min_household_mean_utility | 0.42709 |
| nutrition.min_nutrient_mean_utility | 0.37145 |
| nutrition.min_pairwise_utility | 0.3656 |
| allocation_equity.global_mean_deviation_from_fairshare | 0.5963 |
| allocation_equity.max_household_mean_deviation | 0.80556 |
| allocation_equity.max_item_mean_deviation | 0.7037 |
| allocation_equity.max_pairwise_deviation | 1.33333 |
| allocation_equity.max_household_relative_deviation | 0.20656 |
| allocation_equity.max_item_relative_deviation | 0.03461 |
| allocation_equity.max_pairwise_relative_deviation | 0.3 |
| nutritional_adequacy.min_household_mean_utility | 0.42709 |
| nutritional_adequacy.min_nutrient_mean_utility | 0.37145 |
| nutritional_adequacy.min_pairwise_utility | 0.3656 |
| nutritional_adequacy.household_adequacy_gap | 0.29908 |
| nutritional_adequacy.nutrient_adequacy_gap | 0.3904 |
| nutritional_adequacy.pairwise_adequacy_gap | 0.4 |

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
