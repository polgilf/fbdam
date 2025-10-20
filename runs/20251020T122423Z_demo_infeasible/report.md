# FBDAM Run Report

**Run ID:** `20251020T122423Z_demo_infeasible`

⚠️ **WARNING: MODEL IS INFEASIBLE** ⚠️

The solver could not find a feasible solution. Review the constraints and dials.

## Solver summary
- Name: appsi_highs
- Status: error
- Termination: error
- Elapsed Sec: 0.1072
**Error:** A feasible solution was not found, so no solution can be loaded. If using the appsi.solvers.Highs interface, you can set opt.config.load_solution=False. If using the environ.SolverFactory interface, you can set opt.solve(model, load_solutions = False). Then you can check results.termination_condition and results.best_feasible_objective before loading a solution.

## KPIs
*KPIs not available for infeasible solutions.*

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

## Troubleshooting suggestions
- Check the solver log for detailed infeasibility analysis
- Review constraint dial values (alpha, beta, gamma, kappa, rho, omega)
- Verify that requirements are achievable with available stock + budget
- Consider relaxing adequacy floors or equity caps
- Enable epsilon slack with a small lambda penalty
