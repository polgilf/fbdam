* Source:     Pyomo MPS Writer
* Format:     Free MPS
*
NAME FBDAM
OBJSENSE
 MAX
ROWS
 N  OBJ
 L  c_u_U_link(cal_A1)_
 L  c_u_U_link(cal_A2)_
 L  c_u_U_link(prot_A1)_
 L  c_u_U_link(prot_A2)_
 L  c_u_StockBalance(maize)_
 L  c_u_StockBalance(oil)_
 L  c_u_StockBalance(peas)_
 L  c_u_PurchaseBudget_
 L  c_u_PurchaseActivation(maize)_
 L  c_u_PurchaseActivation(oil)_
 L  c_u_PurchaseActivation(peas)_
 L  c_u_PurchaseAllocationEnforcement(maize)_
 L  c_u_PurchaseAllocationEnforcement(oil)_
 L  c_u_PurchaseAllocationEnforcement(peas)_
 E  c_e_DeviationIdentity(maize_A1)_
 E  c_e_DeviationIdentity(maize_A2)_
 E  c_e_DeviationIdentity(oil_A1)_
 E  c_e_DeviationIdentity(oil_A2)_
 E  c_e_DeviationIdentity(peas_A1)_
 E  c_e_DeviationIdentity(peas_A2)_
 L  c_u_DeviationItemCap(maize)_
 L  c_u_DeviationItemCap(oil)_
 L  c_u_DeviationItemCap(peas)_
 L  c_u_DeviationHouseholdCap(A1)_
 L  c_u_DeviationHouseholdCap(A2)_
 L  c_u_DeviationPairCap(maize_A1)_
 L  c_u_DeviationPairCap(maize_A2)_
 L  c_u_DeviationPairCap(oil_A1)_
 L  c_u_DeviationPairCap(oil_A2)_
 L  c_u_DeviationPairCap(peas_A1)_
 L  c_u_DeviationPairCap(peas_A2)_
 L  c_u_HouseholdFloor(A1)_
 L  c_u_HouseholdFloor(A2)_
 L  c_u_NutrientFloor(cal)_
 L  c_u_NutrientFloor(prot)_
 L  c_u_PairFloor(cal_A1)_
 L  c_u_PairFloor(cal_A2)_
 L  c_u_PairFloor(prot_A1)_
 L  c_u_PairFloor(prot_A2)_
COLUMNS
     x(maize_A1) c_u_U_link(cal_A1)_ -0.13750000000000001
     x(maize_A1) c_u_U_link(prot_A1)_ -0.11111111111111112
     x(maize_A1) c_u_StockBalance(maize)_ 1
     x(maize_A1) c_u_PurchaseAllocationEnforcement(maize)_ -1
     x(maize_A1) c_e_DeviationIdentity(maize_A1)_ -1
     x(maize_A2) c_u_U_link(cal_A2)_ -0.12941176470588234
     x(maize_A2) c_u_U_link(prot_A2)_ -0.10000000000000001
     x(maize_A2) c_u_StockBalance(maize)_ 1
     x(maize_A2) c_u_PurchaseAllocationEnforcement(maize)_ -1
     x(maize_A2) c_e_DeviationIdentity(maize_A2)_ -1
     x(oil_A1) c_u_U_link(cal_A1)_ -0.25
     x(oil_A1) c_u_StockBalance(oil)_ 1
     x(oil_A1) c_u_PurchaseAllocationEnforcement(oil)_ -1
     x(oil_A1) c_e_DeviationIdentity(oil_A1)_ -1
     x(oil_A2) c_u_U_link(cal_A2)_ -0.23529411764705879
     x(oil_A2) c_u_StockBalance(oil)_ 1
     x(oil_A2) c_u_PurchaseAllocationEnforcement(oil)_ -1
     x(oil_A2) c_e_DeviationIdentity(oil_A2)_ -1
     x(peas_A1) c_u_U_link(cal_A1)_ -0.087500000000000008
     x(peas_A1) c_u_U_link(prot_A1)_ -0.24444444444444446
     x(peas_A1) c_u_StockBalance(peas)_ 1
     x(peas_A1) c_u_PurchaseAllocationEnforcement(peas)_ -1
     x(peas_A1) c_e_DeviationIdentity(peas_A1)_ -1
     x(peas_A2) c_u_U_link(cal_A2)_ -0.082352941176470587
     x(peas_A2) c_u_U_link(prot_A2)_ -0.22
     x(peas_A2) c_u_StockBalance(peas)_ 1
     x(peas_A2) c_u_PurchaseAllocationEnforcement(peas)_ -1
     x(peas_A2) c_e_DeviationIdentity(peas_A2)_ -1
     u(cal_A1) OBJ 1
     u(cal_A1) c_u_U_link(cal_A1)_ 1
     u(cal_A1) c_u_HouseholdFloor(A1)_ -0.34999999999999998
     u(cal_A1) c_u_HouseholdFloor(A2)_ 0.14999999999999999
     u(cal_A1) c_u_NutrientFloor(cal)_ -0.34999999999999998
     u(cal_A1) c_u_NutrientFloor(prot)_ 0.14999999999999999
     u(cal_A1) c_u_PairFloor(cal_A1)_ -0.84999999999999998
     u(cal_A1) c_u_PairFloor(cal_A2)_ 0.14999999999999999
     u(cal_A1) c_u_PairFloor(prot_A1)_ 0.14999999999999999
     u(cal_A1) c_u_PairFloor(prot_A2)_ 0.14999999999999999
     u(cal_A2) OBJ 1
     u(cal_A2) c_u_U_link(cal_A2)_ 1
     u(cal_A2) c_u_HouseholdFloor(A1)_ 0.14999999999999999
     u(cal_A2) c_u_HouseholdFloor(A2)_ -0.34999999999999998
     u(cal_A2) c_u_NutrientFloor(cal)_ -0.34999999999999998
     u(cal_A2) c_u_NutrientFloor(prot)_ 0.14999999999999999
     u(cal_A2) c_u_PairFloor(cal_A1)_ 0.14999999999999999
     u(cal_A2) c_u_PairFloor(cal_A2)_ -0.84999999999999998
     u(cal_A2) c_u_PairFloor(prot_A1)_ 0.14999999999999999
     u(cal_A2) c_u_PairFloor(prot_A2)_ 0.14999999999999999
     u(prot_A1) OBJ 1
     u(prot_A1) c_u_U_link(prot_A1)_ 1
     u(prot_A1) c_u_HouseholdFloor(A1)_ -0.34999999999999998
     u(prot_A1) c_u_HouseholdFloor(A2)_ 0.14999999999999999
     u(prot_A1) c_u_NutrientFloor(cal)_ 0.14999999999999999
     u(prot_A1) c_u_NutrientFloor(prot)_ -0.34999999999999998
     u(prot_A1) c_u_PairFloor(cal_A1)_ 0.14999999999999999
     u(prot_A1) c_u_PairFloor(cal_A2)_ 0.14999999999999999
     u(prot_A1) c_u_PairFloor(prot_A1)_ -0.84999999999999998
     u(prot_A1) c_u_PairFloor(prot_A2)_ 0.14999999999999999
     u(prot_A2) OBJ 1
     u(prot_A2) c_u_U_link(prot_A2)_ 1
     u(prot_A2) c_u_HouseholdFloor(A1)_ 0.14999999999999999
     u(prot_A2) c_u_HouseholdFloor(A2)_ -0.34999999999999998
     u(prot_A2) c_u_NutrientFloor(cal)_ 0.14999999999999999
     u(prot_A2) c_u_NutrientFloor(prot)_ -0.34999999999999998
     u(prot_A2) c_u_PairFloor(cal_A1)_ 0.14999999999999999
     u(prot_A2) c_u_PairFloor(cal_A2)_ 0.14999999999999999
     u(prot_A2) c_u_PairFloor(prot_A1)_ 0.14999999999999999
     u(prot_A2) c_u_PairFloor(prot_A2)_ -0.84999999999999998
     y(maize) c_u_StockBalance(maize)_ -1
     y(maize) c_u_PurchaseBudget_ 0.80000000000000004
     y(maize) c_u_PurchaseActivation(maize)_ 1
     y(maize) c_u_PurchaseAllocationEnforcement(maize)_ 1
     y(maize) c_e_DeviationIdentity(maize_A1)_ 0.5
     y(maize) c_e_DeviationIdentity(maize_A2)_ 0.5
     y(maize) c_u_DeviationItemCap(maize)_ -0.40000000000000002
     y(maize) c_u_DeviationHouseholdCap(A1)_ -0.5
     y(maize) c_u_DeviationHouseholdCap(A2)_ -0.5
     y(maize) c_u_DeviationPairCap(maize_A1)_ -0.5
     y(maize) c_u_DeviationPairCap(maize_A2)_ -0.5
     y(oil) c_u_StockBalance(oil)_ -1
     y(oil) c_u_PurchaseBudget_ 2
     y(oil) c_u_PurchaseActivation(oil)_ 1
     y(oil) c_u_PurchaseAllocationEnforcement(oil)_ 1
     y(oil) c_e_DeviationIdentity(oil_A1)_ 0.5
     y(oil) c_e_DeviationIdentity(oil_A2)_ 0.5
     y(oil) c_u_DeviationItemCap(oil)_ -0.40000000000000002
     y(oil) c_u_DeviationHouseholdCap(A1)_ -0.5
     y(oil) c_u_DeviationHouseholdCap(A2)_ -0.5
     y(oil) c_u_DeviationPairCap(oil_A1)_ -0.5
     y(oil) c_u_DeviationPairCap(oil_A2)_ -0.5
     y(peas) c_u_StockBalance(peas)_ -1
     y(peas) c_u_PurchaseBudget_ 1.2
     y(peas) c_u_PurchaseActivation(peas)_ 1
     y(peas) c_u_PurchaseAllocationEnforcement(peas)_ 1
     y(peas) c_e_DeviationIdentity(peas_A1)_ 0.5
     y(peas) c_e_DeviationIdentity(peas_A2)_ 0.5
     y(peas) c_u_DeviationItemCap(peas)_ -0.40000000000000002
     y(peas) c_u_DeviationHouseholdCap(A1)_ -0.5
     y(peas) c_u_DeviationHouseholdCap(A2)_ -0.5
     y(peas) c_u_DeviationPairCap(peas_A1)_ -0.5
     y(peas) c_u_DeviationPairCap(peas_A2)_ -0.5
     y_active(maize) c_u_PurchaseActivation(maize)_ -125
     y_active(maize) c_u_PurchaseAllocationEnforcement(maize)_ 30
     y_active(oil) c_u_PurchaseActivation(oil)_ -50
     y_active(oil) c_u_PurchaseAllocationEnforcement(oil)_ 15
     y_active(peas) c_u_PurchaseActivation(peas)_ -83.333333333333343
     y_active(peas) c_u_PurchaseAllocationEnforcement(peas)_ 25
     dpos(maize_A1) c_e_DeviationIdentity(maize_A1)_ 1
     dpos(maize_A1) c_u_DeviationItemCap(maize)_ 1
     dpos(maize_A1) c_u_DeviationHouseholdCap(A1)_ 1
     dpos(maize_A1) c_u_DeviationPairCap(maize_A1)_ 1
     dpos(maize_A2) c_e_DeviationIdentity(maize_A2)_ 1
     dpos(maize_A2) c_u_DeviationItemCap(maize)_ 1
     dpos(maize_A2) c_u_DeviationHouseholdCap(A2)_ 1
     dpos(maize_A2) c_u_DeviationPairCap(maize_A2)_ 1
     dpos(oil_A1) c_e_DeviationIdentity(oil_A1)_ 1
     dpos(oil_A1) c_u_DeviationItemCap(oil)_ 1
     dpos(oil_A1) c_u_DeviationHouseholdCap(A1)_ 1
     dpos(oil_A1) c_u_DeviationPairCap(oil_A1)_ 1
     dpos(oil_A2) c_e_DeviationIdentity(oil_A2)_ 1
     dpos(oil_A2) c_u_DeviationItemCap(oil)_ 1
     dpos(oil_A2) c_u_DeviationHouseholdCap(A2)_ 1
     dpos(oil_A2) c_u_DeviationPairCap(oil_A2)_ 1
     dpos(peas_A1) c_e_DeviationIdentity(peas_A1)_ 1
     dpos(peas_A1) c_u_DeviationItemCap(peas)_ 1
     dpos(peas_A1) c_u_DeviationHouseholdCap(A1)_ 1
     dpos(peas_A1) c_u_DeviationPairCap(peas_A1)_ 1
     dpos(peas_A2) c_e_DeviationIdentity(peas_A2)_ 1
     dpos(peas_A2) c_u_DeviationItemCap(peas)_ 1
     dpos(peas_A2) c_u_DeviationHouseholdCap(A2)_ 1
     dpos(peas_A2) c_u_DeviationPairCap(peas_A2)_ 1
     dneg(maize_A1) c_e_DeviationIdentity(maize_A1)_ -1
     dneg(maize_A1) c_u_DeviationItemCap(maize)_ 1
     dneg(maize_A1) c_u_DeviationHouseholdCap(A1)_ 1
     dneg(maize_A1) c_u_DeviationPairCap(maize_A1)_ 1
     dneg(maize_A2) c_e_DeviationIdentity(maize_A2)_ -1
     dneg(maize_A2) c_u_DeviationItemCap(maize)_ 1
     dneg(maize_A2) c_u_DeviationHouseholdCap(A2)_ 1
     dneg(maize_A2) c_u_DeviationPairCap(maize_A2)_ 1
     dneg(oil_A1) c_e_DeviationIdentity(oil_A1)_ -1
     dneg(oil_A1) c_u_DeviationItemCap(oil)_ 1
     dneg(oil_A1) c_u_DeviationHouseholdCap(A1)_ 1
     dneg(oil_A1) c_u_DeviationPairCap(oil_A1)_ 1
     dneg(oil_A2) c_e_DeviationIdentity(oil_A2)_ -1
     dneg(oil_A2) c_u_DeviationItemCap(oil)_ 1
     dneg(oil_A2) c_u_DeviationHouseholdCap(A2)_ 1
     dneg(oil_A2) c_u_DeviationPairCap(oil_A2)_ 1
     dneg(peas_A1) c_e_DeviationIdentity(peas_A1)_ -1
     dneg(peas_A1) c_u_DeviationItemCap(peas)_ 1
     dneg(peas_A1) c_u_DeviationHouseholdCap(A1)_ 1
     dneg(peas_A1) c_u_DeviationPairCap(peas_A1)_ 1
     dneg(peas_A2) c_e_DeviationIdentity(peas_A2)_ -1
     dneg(peas_A2) c_u_DeviationItemCap(peas)_ 1
     dneg(peas_A2) c_u_DeviationHouseholdCap(A2)_ 1
     dneg(peas_A2) c_u_DeviationPairCap(peas_A2)_ 1
     epsilon OBJ -0.69999999999999996
     epsilon c_u_HouseholdFloor(A1)_ -1
     epsilon c_u_HouseholdFloor(A2)_ -1
     epsilon c_u_NutrientFloor(cal)_ -1
     epsilon c_u_NutrientFloor(prot)_ -1
     epsilon c_u_PairFloor(cal_A1)_ -1
     epsilon c_u_PairFloor(cal_A2)_ -1
     epsilon c_u_PairFloor(prot_A1)_ -1
     epsilon c_u_PairFloor(prot_A2)_ -1
RHS
     RHS c_u_U_link(cal_A1)_ 0
     RHS c_u_U_link(cal_A2)_ 0
     RHS c_u_U_link(prot_A1)_ 0
     RHS c_u_U_link(prot_A2)_ 0
     RHS c_u_StockBalance(maize)_ 30
     RHS c_u_StockBalance(oil)_ 15
     RHS c_u_StockBalance(peas)_ 25
     RHS c_u_PurchaseBudget_ 100
     RHS c_u_PurchaseActivation(maize)_ 0
     RHS c_u_PurchaseActivation(oil)_ 0
     RHS c_u_PurchaseActivation(peas)_ 0
     RHS c_u_PurchaseAllocationEnforcement(maize)_ 0
     RHS c_u_PurchaseAllocationEnforcement(oil)_ 0
     RHS c_u_PurchaseAllocationEnforcement(peas)_ 0
     RHS c_e_DeviationIdentity(maize_A1)_ -15
     RHS c_e_DeviationIdentity(maize_A2)_ -15
     RHS c_e_DeviationIdentity(oil_A1)_ -7.5
     RHS c_e_DeviationIdentity(oil_A2)_ -7.5
     RHS c_e_DeviationIdentity(peas_A1)_ -12.5
     RHS c_e_DeviationIdentity(peas_A2)_ -12.5
     RHS c_u_DeviationItemCap(maize)_ 12
     RHS c_u_DeviationItemCap(oil)_ 6
     RHS c_u_DeviationItemCap(peas)_ 10
     RHS c_u_DeviationHouseholdCap(A1)_ 35
     RHS c_u_DeviationHouseholdCap(A2)_ 35
     RHS c_u_DeviationPairCap(maize_A1)_ 15
     RHS c_u_DeviationPairCap(maize_A2)_ 15
     RHS c_u_DeviationPairCap(oil_A1)_ 7.5
     RHS c_u_DeviationPairCap(oil_A2)_ 7.5
     RHS c_u_DeviationPairCap(peas_A1)_ 12.5
     RHS c_u_DeviationPairCap(peas_A2)_ 12.5
     RHS c_u_HouseholdFloor(A1)_ 0
     RHS c_u_HouseholdFloor(A2)_ 0
     RHS c_u_NutrientFloor(cal)_ 0
     RHS c_u_NutrientFloor(prot)_ 0
     RHS c_u_PairFloor(cal_A1)_ 0
     RHS c_u_PairFloor(cal_A2)_ 0
     RHS c_u_PairFloor(prot_A1)_ 0
     RHS c_u_PairFloor(prot_A2)_ 0
BOUNDS
 LI BOUND x(maize_A1) 0
 UI BOUND x(maize_A1) 18
 LI BOUND x(maize_A2) 0
 UI BOUND x(maize_A2) 18
 LI BOUND x(oil_A1) 0
 UI BOUND x(oil_A1) 8
 LI BOUND x(oil_A2) 0
 UI BOUND x(oil_A2) 8
 LI BOUND x(peas_A1) 0
 UI BOUND x(peas_A1) 15
 LI BOUND x(peas_A2) 0
 UI BOUND x(peas_A2) 15
 LO BOUND u(cal_A1) 0
 UP BOUND u(cal_A1) 1
 LO BOUND u(cal_A2) 0
 UP BOUND u(cal_A2) 1
 LO BOUND u(prot_A1) 0
 UP BOUND u(prot_A1) 1
 LO BOUND u(prot_A2) 0
 UP BOUND u(prot_A2) 1
 LO BOUND y(maize) 0
 LO BOUND y(oil) 0
 LO BOUND y(peas) 0
 BV BOUND y_active(maize)
 BV BOUND y_active(oil)
 BV BOUND y_active(peas)
 LO BOUND dpos(maize_A1) 0
 LO BOUND dpos(maize_A2) 0
 LO BOUND dpos(oil_A1) 0
 LO BOUND dpos(oil_A2) 0
 LO BOUND dpos(peas_A1) 0
 LO BOUND dpos(peas_A2) 0
 LO BOUND dneg(maize_A1) 0
 LO BOUND dneg(maize_A2) 0
 LO BOUND dneg(oil_A1) 0
 LO BOUND dneg(oil_A2) 0
 LO BOUND dneg(peas_A1) 0
 LO BOUND dneg(peas_A2) 0
 LO BOUND epsilon 0
ENDATA
