# FBDAM Run Report

**Run ID:** `ds-a_dials-efficiency_20251021T232427Z`

## Solver summary
- Name: appsi_highs
- Status: ok
- Termination: TerminationCondition.optimal
- Elapsed Sec: 0.1742
- Objective Value: 6.679673889268626
- Best Feasible Objective: 6.679673889268626
- Best Objective Bound: 6.735139854636592
- Gap: 0.008304

## KPIs
| Metric | Value |
|---|---|
| basic.items | 4.0 |
| basic.households | 3.0 |
| basic.nutrients | 3.0 |
| basic.objective_value | 6.67967 |
| supply.total_allocation | 60.0 |
| supply.avg_allocation_per_pair | 20.0 |
| supply.undistributed | 0.0 |
| supply.total_cost | 9.3 |
| nutrition.total_nutritional_utility | 6.67967 |
| nutrition.global_mean_utility | 0.74219 |
| nutrition.min_household_mean_utility | 0.58334 |
| nutrition.min_nutrient_mean_utility | 0.39777 |
| nutrition.min_pairwise_utility | 0.2075 |
| allocation_equity.global_mean_deviation_from_fairshare | 1.96296 |
| allocation_equity.max_household_mean_deviation | 2.83333 |
| allocation_equity.max_item_mean_deviation | 3.03704 |
| allocation_equity.max_pairwise_deviation | 4.55556 |
| allocation_equity.max_household_relative_deviation | 0.63333 |
| allocation_equity.max_item_relative_deviation | 0.15185 |
| allocation_equity.max_pairwise_relative_deviation | 0.89474 |
| nutritional_adequacy.min_household_mean_utility | 0.58334 |
| nutritional_adequacy.min_nutrient_mean_utility | 0.39777 |
| nutritional_adequacy.min_pairwise_utility | 0.2075 |
| nutritional_adequacy.household_adequacy_gap | 0.21403 |
| nutritional_adequacy.nutrient_adequacy_gap | 0.46406 |
| nutritional_adequacy.pairwise_adequacy_gap | 0.72042 |

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
- HouseholdFloor: 3
- NutrientFloor: 3
- PairFloor: 9
- DeviationIdentity: 12
- DeviationItemCap: 4
- DeviationHouseholdCap: 3
- DeviationPairCap: 12
