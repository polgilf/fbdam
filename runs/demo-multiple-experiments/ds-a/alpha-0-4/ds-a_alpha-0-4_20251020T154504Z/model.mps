* Source:     Pyomo MPS Writer
* Format:     Free MPS
*
NAME FBDAM
OBJSENSE
 MAX
ROWS
 N  OBJ
 L  c_u_U_link(cal_H1)_
 L  c_u_U_link(cal_H2)_
 L  c_u_U_link(prot_H1)_
 L  c_u_U_link(prot_H2)_
 L  c_u_StockBalance(beans)_
 L  c_u_StockBalance(lentils)_
 L  c_u_StockBalance(rice)_
 L  c_u_PurchaseBudget_
 L  c_u_PurchaseActivation(beans)_
 L  c_u_PurchaseActivation(lentils)_
 L  c_u_PurchaseActivation(rice)_
 L  c_u_PurchaseAllocationEnforcement(beans)_
 L  c_u_PurchaseAllocationEnforcement(lentils)_
 L  c_u_PurchaseAllocationEnforcement(rice)_
 E  c_e_DeviationIdentity(beans_H1)_
 E  c_e_DeviationIdentity(beans_H2)_
 E  c_e_DeviationIdentity(lentils_H1)_
 E  c_e_DeviationIdentity(lentils_H2)_
 E  c_e_DeviationIdentity(rice_H1)_
 E  c_e_DeviationIdentity(rice_H2)_
 L  c_u_DeviationItemCap(beans)_
 L  c_u_DeviationItemCap(lentils)_
 L  c_u_DeviationItemCap(rice)_
 L  c_u_DeviationHouseholdCap(H1)_
 L  c_u_DeviationHouseholdCap(H2)_
 L  c_u_DeviationPairCap(beans_H1)_
 L  c_u_DeviationPairCap(beans_H2)_
 L  c_u_DeviationPairCap(lentils_H1)_
 L  c_u_DeviationPairCap(lentils_H2)_
 L  c_u_DeviationPairCap(rice_H1)_
 L  c_u_DeviationPairCap(rice_H2)_
 L  c_u_HouseholdFloor(H1)_
 L  c_u_HouseholdFloor(H2)_
 L  c_u_NutrientFloor(cal)_
 L  c_u_NutrientFloor(prot)_
 L  c_u_PairFloor(cal_H1)_
 L  c_u_PairFloor(cal_H2)_
 L  c_u_PairFloor(prot_H1)_
 L  c_u_PairFloor(prot_H2)_
COLUMNS
     x(beans_H1) c_u_U_link(cal_H1)_ -0.083333333333333329
     x(beans_H1) c_u_U_link(prot_H1)_ -0.20000000000000001
     x(beans_H1) c_u_StockBalance(beans)_ 1
     x(beans_H1) c_u_PurchaseAllocationEnforcement(beans)_ -1
     x(beans_H1) c_e_DeviationIdentity(beans_H1)_ -1
     x(beans_H2) c_u_U_link(cal_H2)_ -0.099999999999999992
     x(beans_H2) c_u_U_link(prot_H2)_ -0.22222222222222224
     x(beans_H2) c_u_StockBalance(beans)_ 1
     x(beans_H2) c_u_PurchaseAllocationEnforcement(beans)_ -1
     x(beans_H2) c_e_DeviationIdentity(beans_H2)_ -1
     x(lentils_H1) c_u_U_link(cal_H1)_ -0.10000000000000001
     x(lentils_H1) c_u_U_link(prot_H1)_ -0.23999999999999999
     x(lentils_H1) c_u_StockBalance(lentils)_ 1
     x(lentils_H1) c_u_PurchaseAllocationEnforcement(lentils)_ -1
     x(lentils_H1) c_e_DeviationIdentity(lentils_H1)_ -1
     x(lentils_H2) c_u_U_link(cal_H2)_ -0.12
     x(lentils_H2) c_u_U_link(prot_H2)_ -0.26666666666666666
     x(lentils_H2) c_u_StockBalance(lentils)_ 1
     x(lentils_H2) c_u_PurchaseAllocationEnforcement(lentils)_ -1
     x(lentils_H2) c_e_DeviationIdentity(lentils_H2)_ -1
     x(rice_H1) c_u_U_link(cal_H1)_ -0.1111111111111111
     x(rice_H1) c_u_U_link(prot_H1)_ -0.080000000000000002
     x(rice_H1) c_u_StockBalance(rice)_ 1
     x(rice_H1) c_u_PurchaseAllocationEnforcement(rice)_ -1
     x(rice_H1) c_e_DeviationIdentity(rice_H1)_ -1
     x(rice_H2) c_u_U_link(cal_H2)_ -0.13333333333333333
     x(rice_H2) c_u_U_link(prot_H2)_ -0.088888888888888892
     x(rice_H2) c_u_StockBalance(rice)_ 1
     x(rice_H2) c_u_PurchaseAllocationEnforcement(rice)_ -1
     x(rice_H2) c_e_DeviationIdentity(rice_H2)_ -1
     u(cal_H1) OBJ 1
     u(cal_H1) c_u_U_link(cal_H1)_ 1
     u(cal_H1) c_u_HouseholdFloor(H1)_ -0.34999999999999998
     u(cal_H1) c_u_HouseholdFloor(H2)_ 0.14999999999999999
     u(cal_H1) c_u_NutrientFloor(cal)_ -0.34999999999999998
     u(cal_H1) c_u_NutrientFloor(prot)_ 0.14999999999999999
     u(cal_H1) c_u_PairFloor(cal_H1)_ -0.84999999999999998
     u(cal_H1) c_u_PairFloor(cal_H2)_ 0.14999999999999999
     u(cal_H1) c_u_PairFloor(prot_H1)_ 0.14999999999999999
     u(cal_H1) c_u_PairFloor(prot_H2)_ 0.14999999999999999
     u(cal_H2) OBJ 1
     u(cal_H2) c_u_U_link(cal_H2)_ 1
     u(cal_H2) c_u_HouseholdFloor(H1)_ 0.14999999999999999
     u(cal_H2) c_u_HouseholdFloor(H2)_ -0.34999999999999998
     u(cal_H2) c_u_NutrientFloor(cal)_ -0.34999999999999998
     u(cal_H2) c_u_NutrientFloor(prot)_ 0.14999999999999999
     u(cal_H2) c_u_PairFloor(cal_H1)_ 0.14999999999999999
     u(cal_H2) c_u_PairFloor(cal_H2)_ -0.84999999999999998
     u(cal_H2) c_u_PairFloor(prot_H1)_ 0.14999999999999999
     u(cal_H2) c_u_PairFloor(prot_H2)_ 0.14999999999999999
     u(prot_H1) OBJ 1
     u(prot_H1) c_u_U_link(prot_H1)_ 1
     u(prot_H1) c_u_HouseholdFloor(H1)_ -0.34999999999999998
     u(prot_H1) c_u_HouseholdFloor(H2)_ 0.14999999999999999
     u(prot_H1) c_u_NutrientFloor(cal)_ 0.14999999999999999
     u(prot_H1) c_u_NutrientFloor(prot)_ -0.34999999999999998
     u(prot_H1) c_u_PairFloor(cal_H1)_ 0.14999999999999999
     u(prot_H1) c_u_PairFloor(cal_H2)_ 0.14999999999999999
     u(prot_H1) c_u_PairFloor(prot_H1)_ -0.84999999999999998
     u(prot_H1) c_u_PairFloor(prot_H2)_ 0.14999999999999999
     u(prot_H2) OBJ 1
     u(prot_H2) c_u_U_link(prot_H2)_ 1
     u(prot_H2) c_u_HouseholdFloor(H1)_ 0.14999999999999999
     u(prot_H2) c_u_HouseholdFloor(H2)_ -0.34999999999999998
     u(prot_H2) c_u_NutrientFloor(cal)_ 0.14999999999999999
     u(prot_H2) c_u_NutrientFloor(prot)_ -0.34999999999999998
     u(prot_H2) c_u_PairFloor(cal_H1)_ 0.14999999999999999
     u(prot_H2) c_u_PairFloor(cal_H2)_ 0.14999999999999999
     u(prot_H2) c_u_PairFloor(prot_H1)_ 0.14999999999999999
     u(prot_H2) c_u_PairFloor(prot_H2)_ -0.84999999999999998
     y(beans) c_u_StockBalance(beans)_ -1
     y(beans) c_u_PurchaseBudget_ 1.5
     y(beans) c_u_PurchaseActivation(beans)_ 1
     y(beans) c_u_PurchaseAllocationEnforcement(beans)_ 1
     y(beans) c_e_DeviationIdentity(beans_H1)_ 0.59999999999999998
     y(beans) c_e_DeviationIdentity(beans_H2)_ 0.40000000000000002
     y(beans) c_u_DeviationItemCap(beans)_ -0.40000000000000002
     y(beans) c_u_DeviationHouseholdCap(H1)_ -0.5
     y(beans) c_u_DeviationHouseholdCap(H2)_ -0.5
     y(beans) c_u_DeviationPairCap(beans_H1)_ -0.5
     y(beans) c_u_DeviationPairCap(beans_H2)_ -0.5
     y(lentils) c_u_StockBalance(lentils)_ -1
     y(lentils) c_u_PurchaseBudget_ 1.8
     y(lentils) c_u_PurchaseActivation(lentils)_ 1
     y(lentils) c_u_PurchaseAllocationEnforcement(lentils)_ 1
     y(lentils) c_e_DeviationIdentity(lentils_H1)_ 0.59999999999999998
     y(lentils) c_e_DeviationIdentity(lentils_H2)_ 0.40000000000000002
     y(lentils) c_u_DeviationItemCap(lentils)_ -0.40000000000000002
     y(lentils) c_u_DeviationHouseholdCap(H1)_ -0.5
     y(lentils) c_u_DeviationHouseholdCap(H2)_ -0.5
     y(lentils) c_u_DeviationPairCap(lentils_H1)_ -0.5
     y(lentils) c_u_DeviationPairCap(lentils_H2)_ -0.5
     y(rice) c_u_StockBalance(rice)_ -1
     y(rice) c_u_PurchaseBudget_ 1
     y(rice) c_u_PurchaseActivation(rice)_ 1
     y(rice) c_u_PurchaseAllocationEnforcement(rice)_ 1
     y(rice) c_e_DeviationIdentity(rice_H1)_ 0.59999999999999998
     y(rice) c_e_DeviationIdentity(rice_H2)_ 0.40000000000000002
     y(rice) c_u_DeviationItemCap(rice)_ -0.40000000000000002
     y(rice) c_u_DeviationHouseholdCap(H1)_ -0.5
     y(rice) c_u_DeviationHouseholdCap(H2)_ -0.5
     y(rice) c_u_DeviationPairCap(rice_H1)_ -0.5
     y(rice) c_u_DeviationPairCap(rice_H2)_ -0.5
     y_active(beans) c_u_PurchaseActivation(beans)_ -80
     y_active(beans) c_u_PurchaseAllocationEnforcement(beans)_ 30
     y_active(lentils) c_u_PurchaseActivation(lentils)_ -66.666666666666671
     y_active(lentils) c_u_PurchaseAllocationEnforcement(lentils)_ 20
     y_active(rice) c_u_PurchaseActivation(rice)_ -120
     y_active(rice) c_u_PurchaseAllocationEnforcement(rice)_ 40
     dpos(beans_H1) c_e_DeviationIdentity(beans_H1)_ 1
     dpos(beans_H1) c_u_DeviationItemCap(beans)_ 1
     dpos(beans_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(beans_H1) c_u_DeviationPairCap(beans_H1)_ 1
     dpos(beans_H2) c_e_DeviationIdentity(beans_H2)_ 1
     dpos(beans_H2) c_u_DeviationItemCap(beans)_ 1
     dpos(beans_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(beans_H2) c_u_DeviationPairCap(beans_H2)_ 1
     dpos(lentils_H1) c_e_DeviationIdentity(lentils_H1)_ 1
     dpos(lentils_H1) c_u_DeviationItemCap(lentils)_ 1
     dpos(lentils_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(lentils_H1) c_u_DeviationPairCap(lentils_H1)_ 1
     dpos(lentils_H2) c_e_DeviationIdentity(lentils_H2)_ 1
     dpos(lentils_H2) c_u_DeviationItemCap(lentils)_ 1
     dpos(lentils_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(lentils_H2) c_u_DeviationPairCap(lentils_H2)_ 1
     dpos(rice_H1) c_e_DeviationIdentity(rice_H1)_ 1
     dpos(rice_H1) c_u_DeviationItemCap(rice)_ 1
     dpos(rice_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(rice_H1) c_u_DeviationPairCap(rice_H1)_ 1
     dpos(rice_H2) c_e_DeviationIdentity(rice_H2)_ 1
     dpos(rice_H2) c_u_DeviationItemCap(rice)_ 1
     dpos(rice_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(rice_H2) c_u_DeviationPairCap(rice_H2)_ 1
     dneg(beans_H1) c_e_DeviationIdentity(beans_H1)_ -1
     dneg(beans_H1) c_u_DeviationItemCap(beans)_ 1
     dneg(beans_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(beans_H1) c_u_DeviationPairCap(beans_H1)_ 1
     dneg(beans_H2) c_e_DeviationIdentity(beans_H2)_ -1
     dneg(beans_H2) c_u_DeviationItemCap(beans)_ 1
     dneg(beans_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(beans_H2) c_u_DeviationPairCap(beans_H2)_ 1
     dneg(lentils_H1) c_e_DeviationIdentity(lentils_H1)_ -1
     dneg(lentils_H1) c_u_DeviationItemCap(lentils)_ 1
     dneg(lentils_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(lentils_H1) c_u_DeviationPairCap(lentils_H1)_ 1
     dneg(lentils_H2) c_e_DeviationIdentity(lentils_H2)_ -1
     dneg(lentils_H2) c_u_DeviationItemCap(lentils)_ 1
     dneg(lentils_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(lentils_H2) c_u_DeviationPairCap(lentils_H2)_ 1
     dneg(rice_H1) c_e_DeviationIdentity(rice_H1)_ -1
     dneg(rice_H1) c_u_DeviationItemCap(rice)_ 1
     dneg(rice_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(rice_H1) c_u_DeviationPairCap(rice_H1)_ 1
     dneg(rice_H2) c_e_DeviationIdentity(rice_H2)_ -1
     dneg(rice_H2) c_u_DeviationItemCap(rice)_ 1
     dneg(rice_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(rice_H2) c_u_DeviationPairCap(rice_H2)_ 1
     epsilon OBJ -0.5
     epsilon c_u_HouseholdFloor(H1)_ -1
     epsilon c_u_HouseholdFloor(H2)_ -1
     epsilon c_u_NutrientFloor(cal)_ -1
     epsilon c_u_NutrientFloor(prot)_ -1
     epsilon c_u_PairFloor(cal_H1)_ -1
     epsilon c_u_PairFloor(cal_H2)_ -1
     epsilon c_u_PairFloor(prot_H1)_ -1
     epsilon c_u_PairFloor(prot_H2)_ -1
RHS
     RHS c_u_U_link(cal_H1)_ 0
     RHS c_u_U_link(cal_H2)_ 0
     RHS c_u_U_link(prot_H1)_ 0
     RHS c_u_U_link(prot_H2)_ 0
     RHS c_u_StockBalance(beans)_ 30
     RHS c_u_StockBalance(lentils)_ 20
     RHS c_u_StockBalance(rice)_ 40
     RHS c_u_PurchaseBudget_ 120
     RHS c_u_PurchaseActivation(beans)_ 0
     RHS c_u_PurchaseActivation(lentils)_ 0
     RHS c_u_PurchaseActivation(rice)_ 0
     RHS c_u_PurchaseAllocationEnforcement(beans)_ 0
     RHS c_u_PurchaseAllocationEnforcement(lentils)_ 0
     RHS c_u_PurchaseAllocationEnforcement(rice)_ 0
     RHS c_e_DeviationIdentity(beans_H1)_ -18
     RHS c_e_DeviationIdentity(beans_H2)_ -12
     RHS c_e_DeviationIdentity(lentils_H1)_ -12
     RHS c_e_DeviationIdentity(lentils_H2)_ -8
     RHS c_e_DeviationIdentity(rice_H1)_ -24
     RHS c_e_DeviationIdentity(rice_H2)_ -16
     RHS c_u_DeviationItemCap(beans)_ 12
     RHS c_u_DeviationItemCap(lentils)_ 8
     RHS c_u_DeviationItemCap(rice)_ 16
     RHS c_u_DeviationHouseholdCap(H1)_ 45
     RHS c_u_DeviationHouseholdCap(H2)_ 45
     RHS c_u_DeviationPairCap(beans_H1)_ 15
     RHS c_u_DeviationPairCap(beans_H2)_ 15
     RHS c_u_DeviationPairCap(lentils_H1)_ 10
     RHS c_u_DeviationPairCap(lentils_H2)_ 10
     RHS c_u_DeviationPairCap(rice_H1)_ 20
     RHS c_u_DeviationPairCap(rice_H2)_ 20
     RHS c_u_HouseholdFloor(H1)_ 0
     RHS c_u_HouseholdFloor(H2)_ 0
     RHS c_u_NutrientFloor(cal)_ 0
     RHS c_u_NutrientFloor(prot)_ 0
     RHS c_u_PairFloor(cal_H1)_ 0
     RHS c_u_PairFloor(cal_H2)_ 0
     RHS c_u_PairFloor(prot_H1)_ 0
     RHS c_u_PairFloor(prot_H2)_ 0
BOUNDS
 LI BOUND x(beans_H1) 0
 UI BOUND x(beans_H1) 15
 LI BOUND x(beans_H2) 0
 UI BOUND x(beans_H2) 15
 LI BOUND x(lentils_H1) 0
 UI BOUND x(lentils_H1) 10
 LI BOUND x(lentils_H2) 0
 UI BOUND x(lentils_H2) 10
 LI BOUND x(rice_H1) 0
 UI BOUND x(rice_H1) 20
 LI BOUND x(rice_H2) 0
 UI BOUND x(rice_H2) 20
 LO BOUND u(cal_H1) 0
 UP BOUND u(cal_H1) 1
 LO BOUND u(cal_H2) 0
 UP BOUND u(cal_H2) 1
 LO BOUND u(prot_H1) 0
 UP BOUND u(prot_H1) 1
 LO BOUND u(prot_H2) 0
 UP BOUND u(prot_H2) 1
 LO BOUND y(beans) 0
 LO BOUND y(lentils) 0
 LO BOUND y(rice) 0
 BV BOUND y_active(beans)
 BV BOUND y_active(lentils)
 BV BOUND y_active(rice)
 LO BOUND dpos(beans_H1) 0
 LO BOUND dpos(beans_H2) 0
 LO BOUND dpos(lentils_H1) 0
 LO BOUND dpos(lentils_H2) 0
 LO BOUND dpos(rice_H1) 0
 LO BOUND dpos(rice_H2) 0
 LO BOUND dneg(beans_H1) 0
 LO BOUND dneg(beans_H2) 0
 LO BOUND dneg(lentils_H1) 0
 LO BOUND dneg(lentils_H2) 0
 LO BOUND dneg(rice_H1) 0
 LO BOUND dneg(rice_H2) 0
 LO BOUND epsilon 0
ENDATA
