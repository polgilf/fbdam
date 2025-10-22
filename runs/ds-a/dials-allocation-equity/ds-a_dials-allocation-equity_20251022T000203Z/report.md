# FBDAM Run Report

**Run ID:** `ds-a_dials-allocation-equity_20251022T000203Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1441
- Objective Value: 5.953117794486216
- Best Feasible Objective: 5.953117794486216
- Best Objective Bound: 5.953117794486216
- Gap: 0.0

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 5.95312 |
| supply.total_allocation | 58.0 |
| supply.avg_allocation_per_pair | 19.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.5 |
| nutrition.total_nutritional_utility | 5.95312 |
| nutrition.global_mean_utility | 0.66146 |
| nutrition.min_household_mean_utility | 0.62213 |
| nutrition.min_nutrient_mean_utility | 0.18867 |
| nutrition.min_pairwise_utility | 0.154 |
| allocation_equity.global_mean_deviation_from_fairshare | 0.2037 |
| allocation_equity.max_household_mean_deviation | 0.25 |
| allocation_equity.max_item_mean_deviation | 0.2963 |
| allocation_equity.max_pairwise_deviation | 0.44444 |
| allocation_equity.max_household_relative_deviation | 0.06897 |
| allocation_equity.max_item_relative_deviation | 0.01533 |
| allocation_equity.max_pairwise_relative_deviation | 0.1 |
| nutritional_adequacy.min_household_mean_utility | 0.62213 |
| nutritional_adequacy.min_nutrient_mean_utility | 0.18867 |
| nutritional_adequacy.min_pairwise_utility | 0.154 |
| nutritional_adequacy.household_adequacy_gap | 0.05946 |
| nutritional_adequacy.nutrient_adequacy_gap | 0.71477 |
| nutritional_adequacy.pairwise_adequacy_gap | 0.76718 |

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
