# FBDAM Run Report

**Run ID:** `ds-a_dials-hierarchical_20251021T232434Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.2364
- Objective Value: 6.311888721804512
- Best Feasible Objective: 6.311888721804512
- Best Objective Bound: 6.3535004753077935
- Gap: 0.006593

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.31189 |
| supply.total_allocation | 61.0 |
| supply.avg_allocation_per_pair | 20.33333 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.9 |
| nutrition.total_nutritional_utility | 6.31189 |
| nutrition.global_mean_utility | 0.70132 |
| nutrition.min_household_mean_utility | 0.66888 |
| nutrition.min_nutrient_mean_utility | 0.3568 |
| nutrition.min_pairwise_utility | 0.274 |
| allocation_equity.global_mean_deviation_from_fairshare | 0.77593 |
| allocation_equity.max_household_mean_deviation | 1.01667 |
| allocation_equity.max_item_mean_deviation | 1.34074 |
| allocation_equity.max_pairwise_deviation | 2.0 |
| allocation_equity.max_household_relative_deviation | 0.2 |
| allocation_equity.max_item_relative_deviation | 0.06594 |
| allocation_equity.max_pairwise_relative_deviation | 0.5 |
| nutritional_adequacy.min_household_mean_utility | 0.66888 |
| nutritional_adequacy.min_nutrient_mean_utility | 0.3568 |
| nutritional_adequacy.min_pairwise_utility | 0.274 |
| nutritional_adequacy.household_adequacy_gap | 0.04626 |
| nutritional_adequacy.nutrient_adequacy_gap | 0.49125 |
| nutritional_adequacy.pairwise_adequacy_gap | 0.60931 |

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
