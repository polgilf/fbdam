# FBDAM Run Report

**Run ID:** `ds-a_dials-equity-adequacy_20251021T232433Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1841
- Objective Value: 1.5400000000000003
- Best Feasible Objective: 1.5400000000000003
- Best Objective Bound: 1.5837575757575761
- Gap: 0.028414

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 1.54 |
| supply.total_allocation | 57.0 |
| supply.avg_allocation_per_pair | 19.0 |
| supply.undistributed | 0.0 |
| supply.total_cost | 8.3 |
| nutrition.total_nutritional_utility | 1.54 |
| nutrition.global_mean_utility | 0.17111 |
| nutrition.min_household_mean_utility | 0.154 |
| nutrition.min_nutrient_mean_utility | 0.154 |
| nutrition.min_pairwise_utility | 0.154 |
| allocation_equity.global_mean_deviation_from_fairshare | 0.12963 |
| allocation_equity.max_household_mean_deviation | 0.16667 |
| allocation_equity.max_item_mean_deviation | 0.2963 |
| allocation_equity.max_pairwise_deviation | 0.44444 |
| allocation_equity.max_household_relative_deviation | 0.05263 |
| allocation_equity.max_item_relative_deviation | 0.01559 |
| allocation_equity.max_pairwise_relative_deviation | 0.1 |
| nutritional_adequacy.min_household_mean_utility | 0.154 |
| nutritional_adequacy.min_nutrient_mean_utility | 0.154 |
| nutritional_adequacy.min_pairwise_utility | 0.154 |
| nutritional_adequacy.household_adequacy_gap | 0.1 |
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
