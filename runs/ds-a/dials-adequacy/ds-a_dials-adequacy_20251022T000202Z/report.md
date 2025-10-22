# FBDAM Run Report

**Run ID:** `ds-a_dials-adequacy_20251022T000202Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1852
- Objective Value: 3.659999999999999
- Best Feasible Objective: 3.659999999999999
- Best Objective Bound: 3.661538461538459
- Gap: 0.00042

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 3.66 |
| supply.total_allocation | 61.0 |
| supply.avg_allocation_per_pair | 20.33333 |
| supply.undistributed | -0.0 |
| supply.total_cost | 9.9 |
| nutrition.total_nutritional_utility | 3.66 |
| nutrition.global_mean_utility | 0.40667 |
| nutrition.min_household_mean_utility | 0.37067 |
| nutrition.min_nutrient_mean_utility | 0.366 |
| nutrition.min_pairwise_utility | 0.366 |
| allocation_equity.global_mean_deviation_from_fairshare | 0.88889 |
| allocation_equity.max_household_mean_deviation | 1.33333 |
| allocation_equity.max_item_mean_deviation | 1.25926 |
| allocation_equity.max_pairwise_deviation | 1.88889 |
| allocation_equity.max_household_relative_deviation | 0.34426 |
| allocation_equity.max_item_relative_deviation | 0.06193 |
| allocation_equity.max_pairwise_relative_deviation | 0.55 |
| nutritional_adequacy.min_household_mean_utility | 0.37067 |
| nutritional_adequacy.min_nutrient_mean_utility | 0.366 |
| nutritional_adequacy.min_pairwise_utility | 0.366 |
| nutritional_adequacy.household_adequacy_gap | 0.08852 |
| nutritional_adequacy.nutrient_adequacy_gap | 0.1 |
| nutritional_adequacy.pairwise_adequacy_gap | 0.1 |

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
