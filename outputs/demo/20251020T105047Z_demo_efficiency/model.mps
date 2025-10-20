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
 L  c_u_U_link(cal_H3)_
 L  c_u_U_link(calc_H1)_
 L  c_u_U_link(calc_H2)_
 L  c_u_U_link(calc_H3)_
 L  c_u_U_link(prot_H1)_
 L  c_u_U_link(prot_H2)_
 L  c_u_U_link(prot_H3)_
 L  c_u_StockBalance(apples)_
 L  c_u_StockBalance(beans)_
 L  c_u_StockBalance(milk)_
 L  c_u_StockBalance(rice)_
 L  c_u_PurchaseBudget_
 E  c_e_DeviationIdentity(apples_H1)_
 E  c_e_DeviationIdentity(apples_H2)_
 E  c_e_DeviationIdentity(apples_H3)_
 E  c_e_DeviationIdentity(beans_H1)_
 E  c_e_DeviationIdentity(beans_H2)_
 E  c_e_DeviationIdentity(beans_H3)_
 E  c_e_DeviationIdentity(milk_H1)_
 E  c_e_DeviationIdentity(milk_H2)_
 E  c_e_DeviationIdentity(milk_H3)_
 E  c_e_DeviationIdentity(rice_H1)_
 E  c_e_DeviationIdentity(rice_H2)_
 E  c_e_DeviationIdentity(rice_H3)_
 L  c_u_DeviationItemCap(apples)_
 L  c_u_DeviationItemCap(beans)_
 L  c_u_DeviationItemCap(milk)_
 L  c_u_DeviationItemCap(rice)_
 L  c_u_DeviationHouseholdCap(H1)_
 L  c_u_DeviationHouseholdCap(H2)_
 L  c_u_DeviationHouseholdCap(H3)_
 L  c_u_DeviationPairCap(apples_H1)_
 L  c_u_DeviationPairCap(apples_H2)_
 L  c_u_DeviationPairCap(apples_H3)_
 L  c_u_DeviationPairCap(beans_H1)_
 L  c_u_DeviationPairCap(beans_H2)_
 L  c_u_DeviationPairCap(beans_H3)_
 L  c_u_DeviationPairCap(milk_H1)_
 L  c_u_DeviationPairCap(milk_H2)_
 L  c_u_DeviationPairCap(milk_H3)_
 L  c_u_DeviationPairCap(rice_H1)_
 L  c_u_DeviationPairCap(rice_H2)_
 L  c_u_DeviationPairCap(rice_H3)_
 G  c_l_HouseholdFloor(H1)_
 G  c_l_HouseholdFloor(H2)_
 G  c_l_HouseholdFloor(H3)_
 G  c_l_NutrientFloor(cal)_
 G  c_l_NutrientFloor(calc)_
 G  c_l_NutrientFloor(prot)_
 G  c_l_PairFloor(cal_H1)_
 G  c_l_PairFloor(cal_H2)_
 G  c_l_PairFloor(cal_H3)_
 G  c_l_PairFloor(calc_H1)_
 G  c_l_PairFloor(calc_H2)_
 G  c_l_PairFloor(calc_H3)_
 G  c_l_PairFloor(prot_H1)_
 G  c_l_PairFloor(prot_H2)_
 G  c_l_PairFloor(prot_H3)_
COLUMNS
     x(apples_H1) c_u_U_link(cal_H1)_ -0.024761904761904763
     x(apples_H1) c_u_U_link(calc_H1)_ -0.0060000000000000001
     x(apples_H1) c_u_U_link(prot_H1)_ -0.0040000000000000001
     x(apples_H1) c_u_StockBalance(apples)_ 1
     x(apples_H1) c_e_DeviationIdentity(apples_H1)_ -1
     x(apples_H2) c_u_U_link(cal_H2)_ -0.0086666666666666663
     x(apples_H2) c_u_U_link(calc_H2)_ -0.0024000000000000002
     x(apples_H2) c_u_U_link(prot_H2)_ -0.0016666666666666668
     x(apples_H2) c_u_StockBalance(apples)_ 1
     x(apples_H2) c_e_DeviationIdentity(apples_H2)_ -1
     x(apples_H3) c_u_U_link(cal_H3)_ -0.0054736842105263155
     x(apples_H3) c_u_U_link(calc_H3)_ -0.0015
     x(apples_H3) c_u_U_link(prot_H3)_ -0.00090909090909090909
     x(apples_H3) c_u_StockBalance(apples)_ 1
     x(apples_H3) c_e_DeviationIdentity(apples_H3)_ -1
     x(beans_H1) c_u_U_link(cal_H1)_ -0.15714285714285714
     x(beans_H1) c_u_U_link(calc_H1)_ -0.011000000000000001
     x(beans_H1) c_u_U_link(prot_H1)_ -0.41999999999999998
     x(beans_H1) c_u_StockBalance(beans)_ 1
     x(beans_H1) c_e_DeviationIdentity(beans_H1)_ -1
     x(beans_H2) c_u_U_link(cal_H2)_ -0.055
     x(beans_H2) c_u_U_link(calc_H2)_ -0.0044000000000000003
     x(beans_H2) c_u_U_link(prot_H2)_ -0.17500000000000002
     x(beans_H2) c_u_StockBalance(beans)_ 1
     x(beans_H2) c_e_DeviationIdentity(beans_H2)_ -1
     x(beans_H3) c_u_U_link(cal_H3)_ -0.034736842105263156
     x(beans_H3) c_u_U_link(calc_H3)_ -0.0027500000000000003
     x(beans_H3) c_u_U_link(prot_H3)_ -0.095454545454545459
     x(beans_H3) c_u_StockBalance(beans)_ 1
     x(beans_H3) c_e_DeviationIdentity(beans_H3)_ -1
     x(milk_H1) c_u_U_link(cal_H1)_ -0.030476190476190476
     x(milk_H1) c_u_U_link(calc_H1)_ -0.12000000000000001
     x(milk_H1) c_u_U_link(prot_H1)_ -0.066000000000000003
     x(milk_H1) c_u_StockBalance(milk)_ 1
     x(milk_H1) c_e_DeviationIdentity(milk_H1)_ -1
     x(milk_H2) c_u_U_link(cal_H2)_ -0.010666666666666668
     x(milk_H2) c_u_U_link(calc_H2)_ -0.048000000000000001
     x(milk_H2) c_u_U_link(prot_H2)_ -0.0275
     x(milk_H2) c_u_StockBalance(milk)_ 1
     x(milk_H2) c_e_DeviationIdentity(milk_H2)_ -1
     x(milk_H3) c_u_U_link(cal_H3)_ -0.0067368421052631583
     x(milk_H3) c_u_U_link(calc_H3)_ -0.030000000000000002
     x(milk_H3) c_u_U_link(prot_H3)_ -0.014999999999999999
     x(milk_H3) c_u_StockBalance(milk)_ 1
     x(milk_H3) c_e_DeviationIdentity(milk_H3)_ -1
     x(rice_H1) c_u_U_link(cal_H1)_ -0.17142857142857143
     x(rice_H1) c_u_U_link(calc_H1)_ -0.0030000000000000001
     x(rice_H1) c_u_U_link(prot_H1)_ -0.14000000000000001
     x(rice_H1) c_u_StockBalance(rice)_ 1
     x(rice_H1) c_e_DeviationIdentity(rice_H1)_ -1
     x(rice_H2) c_u_U_link(cal_H2)_ -0.060000000000000005
     x(rice_H2) c_u_U_link(calc_H2)_ -0.0012000000000000001
     x(rice_H2) c_u_U_link(prot_H2)_ -0.058333333333333334
     x(rice_H2) c_u_StockBalance(rice)_ 1
     x(rice_H2) c_e_DeviationIdentity(rice_H2)_ -1
     x(rice_H3) c_u_U_link(cal_H3)_ -0.037894736842105266
     x(rice_H3) c_u_U_link(calc_H3)_ -0.00075000000000000002
     x(rice_H3) c_u_U_link(prot_H3)_ -0.031818181818181815
     x(rice_H3) c_u_StockBalance(rice)_ 1
     x(rice_H3) c_e_DeviationIdentity(rice_H3)_ -1
     u(cal_H1) OBJ 1
     u(cal_H1) c_u_U_link(cal_H1)_ 1
     u(cal_H1) c_l_HouseholdFloor(H1)_ 0.32222222222222219
     u(cal_H1) c_l_HouseholdFloor(H2)_ -0.011111111111111112
     u(cal_H1) c_l_HouseholdFloor(H3)_ -0.011111111111111112
     u(cal_H1) c_l_NutrientFloor(cal)_ 0.32222222222222219
     u(cal_H1) c_l_NutrientFloor(calc)_ -0.011111111111111112
     u(cal_H1) c_l_NutrientFloor(prot)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(cal_H1)_ 0.98888888888888893
     u(cal_H1) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(cal_H1) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(cal_H2) OBJ 1
     u(cal_H2) c_u_U_link(cal_H2)_ 1
     u(cal_H2) c_l_HouseholdFloor(H1)_ -0.011111111111111112
     u(cal_H2) c_l_HouseholdFloor(H2)_ 0.32222222222222219
     u(cal_H2) c_l_HouseholdFloor(H3)_ -0.011111111111111112
     u(cal_H2) c_l_NutrientFloor(cal)_ 0.32222222222222219
     u(cal_H2) c_l_NutrientFloor(calc)_ -0.011111111111111112
     u(cal_H2) c_l_NutrientFloor(prot)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(cal_H2)_ 0.98888888888888893
     u(cal_H2) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(cal_H2) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(cal_H3) OBJ 1
     u(cal_H3) c_u_U_link(cal_H3)_ 1
     u(cal_H3) c_l_HouseholdFloor(H1)_ -0.011111111111111112
     u(cal_H3) c_l_HouseholdFloor(H2)_ -0.011111111111111112
     u(cal_H3) c_l_HouseholdFloor(H3)_ 0.32222222222222219
     u(cal_H3) c_l_NutrientFloor(cal)_ 0.32222222222222219
     u(cal_H3) c_l_NutrientFloor(calc)_ -0.011111111111111112
     u(cal_H3) c_l_NutrientFloor(prot)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(cal_H3)_ 0.98888888888888893
     u(cal_H3) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(cal_H3) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(calc_H1) OBJ 1
     u(calc_H1) c_u_U_link(calc_H1)_ 1
     u(calc_H1) c_l_HouseholdFloor(H1)_ 0.32222222222222219
     u(calc_H1) c_l_HouseholdFloor(H2)_ -0.011111111111111112
     u(calc_H1) c_l_HouseholdFloor(H3)_ -0.011111111111111112
     u(calc_H1) c_l_NutrientFloor(cal)_ -0.011111111111111112
     u(calc_H1) c_l_NutrientFloor(calc)_ 0.32222222222222219
     u(calc_H1) c_l_NutrientFloor(prot)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(calc_H1)_ 0.98888888888888893
     u(calc_H1) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(calc_H1) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(calc_H2) OBJ 1
     u(calc_H2) c_u_U_link(calc_H2)_ 1
     u(calc_H2) c_l_HouseholdFloor(H1)_ -0.011111111111111112
     u(calc_H2) c_l_HouseholdFloor(H2)_ 0.32222222222222219
     u(calc_H2) c_l_HouseholdFloor(H3)_ -0.011111111111111112
     u(calc_H2) c_l_NutrientFloor(cal)_ -0.011111111111111112
     u(calc_H2) c_l_NutrientFloor(calc)_ 0.32222222222222219
     u(calc_H2) c_l_NutrientFloor(prot)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(calc_H2)_ 0.98888888888888893
     u(calc_H2) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(calc_H2) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(calc_H3) OBJ 1
     u(calc_H3) c_u_U_link(calc_H3)_ 1
     u(calc_H3) c_l_HouseholdFloor(H1)_ -0.011111111111111112
     u(calc_H3) c_l_HouseholdFloor(H2)_ -0.011111111111111112
     u(calc_H3) c_l_HouseholdFloor(H3)_ 0.32222222222222219
     u(calc_H3) c_l_NutrientFloor(cal)_ -0.011111111111111112
     u(calc_H3) c_l_NutrientFloor(calc)_ 0.32222222222222219
     u(calc_H3) c_l_NutrientFloor(prot)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(calc_H3)_ 0.98888888888888893
     u(calc_H3) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(calc_H3) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(prot_H1) OBJ 1
     u(prot_H1) c_u_U_link(prot_H1)_ 1
     u(prot_H1) c_l_HouseholdFloor(H1)_ 0.32222222222222219
     u(prot_H1) c_l_HouseholdFloor(H2)_ -0.011111111111111112
     u(prot_H1) c_l_HouseholdFloor(H3)_ -0.011111111111111112
     u(prot_H1) c_l_NutrientFloor(cal)_ -0.011111111111111112
     u(prot_H1) c_l_NutrientFloor(calc)_ -0.011111111111111112
     u(prot_H1) c_l_NutrientFloor(prot)_ 0.32222222222222219
     u(prot_H1) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(prot_H1)_ 0.98888888888888893
     u(prot_H1) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(prot_H1) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(prot_H2) OBJ 1
     u(prot_H2) c_u_U_link(prot_H2)_ 1
     u(prot_H2) c_l_HouseholdFloor(H1)_ -0.011111111111111112
     u(prot_H2) c_l_HouseholdFloor(H2)_ 0.32222222222222219
     u(prot_H2) c_l_HouseholdFloor(H3)_ -0.011111111111111112
     u(prot_H2) c_l_NutrientFloor(cal)_ -0.011111111111111112
     u(prot_H2) c_l_NutrientFloor(calc)_ -0.011111111111111112
     u(prot_H2) c_l_NutrientFloor(prot)_ 0.32222222222222219
     u(prot_H2) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(prot_H2) c_l_PairFloor(prot_H2)_ 0.98888888888888893
     u(prot_H2) c_l_PairFloor(prot_H3)_ -0.011111111111111112
     u(prot_H3) OBJ 1
     u(prot_H3) c_u_U_link(prot_H3)_ 1
     u(prot_H3) c_l_HouseholdFloor(H1)_ -0.011111111111111112
     u(prot_H3) c_l_HouseholdFloor(H2)_ -0.011111111111111112
     u(prot_H3) c_l_HouseholdFloor(H3)_ 0.32222222222222219
     u(prot_H3) c_l_NutrientFloor(cal)_ -0.011111111111111112
     u(prot_H3) c_l_NutrientFloor(calc)_ -0.011111111111111112
     u(prot_H3) c_l_NutrientFloor(prot)_ 0.32222222222222219
     u(prot_H3) c_l_PairFloor(cal_H1)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(cal_H2)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(cal_H3)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(calc_H1)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(calc_H2)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(calc_H3)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(prot_H1)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(prot_H2)_ -0.011111111111111112
     u(prot_H3) c_l_PairFloor(prot_H3)_ 0.98888888888888893
     y(apples) c_u_StockBalance(apples)_ -1
     y(apples) c_u_PurchaseBudget_ 1.1000000000000001
     y(apples) c_e_DeviationIdentity(apples_H1)_ 0.111111111
     y(apples) c_e_DeviationIdentity(apples_H2)_ 0.33333333300000001
     y(apples) c_e_DeviationIdentity(apples_H3)_ 0.55555555599999995
     y(apples) c_u_DeviationItemCap(apples)_ -0.90000000000000002
     y(apples) c_u_DeviationHouseholdCap(H1)_ -0.90000000000000002
     y(apples) c_u_DeviationHouseholdCap(H2)_ -0.90000000000000002
     y(apples) c_u_DeviationHouseholdCap(H3)_ -0.90000000000000002
     y(apples) c_u_DeviationPairCap(apples_H1)_ -0.90000000000000002
     y(apples) c_u_DeviationPairCap(apples_H2)_ -0.90000000000000002
     y(apples) c_u_DeviationPairCap(apples_H3)_ -0.90000000000000002
     y(beans) c_u_StockBalance(beans)_ -1
     y(beans) c_u_PurchaseBudget_ 1.2
     y(beans) c_e_DeviationIdentity(beans_H1)_ 0.111111111
     y(beans) c_e_DeviationIdentity(beans_H2)_ 0.33333333300000001
     y(beans) c_e_DeviationIdentity(beans_H3)_ 0.55555555599999995
     y(beans) c_u_DeviationItemCap(beans)_ -0.90000000000000002
     y(beans) c_u_DeviationHouseholdCap(H1)_ -0.90000000000000002
     y(beans) c_u_DeviationHouseholdCap(H2)_ -0.90000000000000002
     y(beans) c_u_DeviationHouseholdCap(H3)_ -0.90000000000000002
     y(beans) c_u_DeviationPairCap(beans_H1)_ -0.90000000000000002
     y(beans) c_u_DeviationPairCap(beans_H2)_ -0.90000000000000002
     y(beans) c_u_DeviationPairCap(beans_H3)_ -0.90000000000000002
     y(milk) c_u_StockBalance(milk)_ -1
     y(milk) c_u_PurchaseBudget_ 0.90000000000000002
     y(milk) c_e_DeviationIdentity(milk_H1)_ 0.111111111
     y(milk) c_e_DeviationIdentity(milk_H2)_ 0.33333333300000001
     y(milk) c_e_DeviationIdentity(milk_H3)_ 0.55555555599999995
     y(milk) c_u_DeviationItemCap(milk)_ -0.90000000000000002
     y(milk) c_u_DeviationHouseholdCap(H1)_ -0.90000000000000002
     y(milk) c_u_DeviationHouseholdCap(H2)_ -0.90000000000000002
     y(milk) c_u_DeviationHouseholdCap(H3)_ -0.90000000000000002
     y(milk) c_u_DeviationPairCap(milk_H1)_ -0.90000000000000002
     y(milk) c_u_DeviationPairCap(milk_H2)_ -0.90000000000000002
     y(milk) c_u_DeviationPairCap(milk_H3)_ -0.90000000000000002
     y(rice) c_u_StockBalance(rice)_ -1
     y(rice) c_u_PurchaseBudget_ 1
     y(rice) c_e_DeviationIdentity(rice_H1)_ 0.111111111
     y(rice) c_e_DeviationIdentity(rice_H2)_ 0.33333333300000001
     y(rice) c_e_DeviationIdentity(rice_H3)_ 0.55555555599999995
     y(rice) c_u_DeviationItemCap(rice)_ -0.90000000000000002
     y(rice) c_u_DeviationHouseholdCap(H1)_ -0.90000000000000002
     y(rice) c_u_DeviationHouseholdCap(H2)_ -0.90000000000000002
     y(rice) c_u_DeviationHouseholdCap(H3)_ -0.90000000000000002
     y(rice) c_u_DeviationPairCap(rice_H1)_ -0.90000000000000002
     y(rice) c_u_DeviationPairCap(rice_H2)_ -0.90000000000000002
     y(rice) c_u_DeviationPairCap(rice_H3)_ -0.90000000000000002
     dpos(apples_H1) c_e_DeviationIdentity(apples_H1)_ 1
     dpos(apples_H1) c_u_DeviationItemCap(apples)_ 1
     dpos(apples_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(apples_H1) c_u_DeviationPairCap(apples_H1)_ 1
     dpos(apples_H2) c_e_DeviationIdentity(apples_H2)_ 1
     dpos(apples_H2) c_u_DeviationItemCap(apples)_ 1
     dpos(apples_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(apples_H2) c_u_DeviationPairCap(apples_H2)_ 1
     dpos(apples_H3) c_e_DeviationIdentity(apples_H3)_ 1
     dpos(apples_H3) c_u_DeviationItemCap(apples)_ 1
     dpos(apples_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dpos(apples_H3) c_u_DeviationPairCap(apples_H3)_ 1
     dpos(beans_H1) c_e_DeviationIdentity(beans_H1)_ 1
     dpos(beans_H1) c_u_DeviationItemCap(beans)_ 1
     dpos(beans_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(beans_H1) c_u_DeviationPairCap(beans_H1)_ 1
     dpos(beans_H2) c_e_DeviationIdentity(beans_H2)_ 1
     dpos(beans_H2) c_u_DeviationItemCap(beans)_ 1
     dpos(beans_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(beans_H2) c_u_DeviationPairCap(beans_H2)_ 1
     dpos(beans_H3) c_e_DeviationIdentity(beans_H3)_ 1
     dpos(beans_H3) c_u_DeviationItemCap(beans)_ 1
     dpos(beans_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dpos(beans_H3) c_u_DeviationPairCap(beans_H3)_ 1
     dpos(milk_H1) c_e_DeviationIdentity(milk_H1)_ 1
     dpos(milk_H1) c_u_DeviationItemCap(milk)_ 1
     dpos(milk_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(milk_H1) c_u_DeviationPairCap(milk_H1)_ 1
     dpos(milk_H2) c_e_DeviationIdentity(milk_H2)_ 1
     dpos(milk_H2) c_u_DeviationItemCap(milk)_ 1
     dpos(milk_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(milk_H2) c_u_DeviationPairCap(milk_H2)_ 1
     dpos(milk_H3) c_e_DeviationIdentity(milk_H3)_ 1
     dpos(milk_H3) c_u_DeviationItemCap(milk)_ 1
     dpos(milk_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dpos(milk_H3) c_u_DeviationPairCap(milk_H3)_ 1
     dpos(rice_H1) c_e_DeviationIdentity(rice_H1)_ 1
     dpos(rice_H1) c_u_DeviationItemCap(rice)_ 1
     dpos(rice_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dpos(rice_H1) c_u_DeviationPairCap(rice_H1)_ 1
     dpos(rice_H2) c_e_DeviationIdentity(rice_H2)_ 1
     dpos(rice_H2) c_u_DeviationItemCap(rice)_ 1
     dpos(rice_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dpos(rice_H2) c_u_DeviationPairCap(rice_H2)_ 1
     dpos(rice_H3) c_e_DeviationIdentity(rice_H3)_ 1
     dpos(rice_H3) c_u_DeviationItemCap(rice)_ 1
     dpos(rice_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dpos(rice_H3) c_u_DeviationPairCap(rice_H3)_ 1
     dneg(apples_H1) c_e_DeviationIdentity(apples_H1)_ -1
     dneg(apples_H1) c_u_DeviationItemCap(apples)_ 1
     dneg(apples_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(apples_H1) c_u_DeviationPairCap(apples_H1)_ 1
     dneg(apples_H2) c_e_DeviationIdentity(apples_H2)_ -1
     dneg(apples_H2) c_u_DeviationItemCap(apples)_ 1
     dneg(apples_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(apples_H2) c_u_DeviationPairCap(apples_H2)_ 1
     dneg(apples_H3) c_e_DeviationIdentity(apples_H3)_ -1
     dneg(apples_H3) c_u_DeviationItemCap(apples)_ 1
     dneg(apples_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dneg(apples_H3) c_u_DeviationPairCap(apples_H3)_ 1
     dneg(beans_H1) c_e_DeviationIdentity(beans_H1)_ -1
     dneg(beans_H1) c_u_DeviationItemCap(beans)_ 1
     dneg(beans_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(beans_H1) c_u_DeviationPairCap(beans_H1)_ 1
     dneg(beans_H2) c_e_DeviationIdentity(beans_H2)_ -1
     dneg(beans_H2) c_u_DeviationItemCap(beans)_ 1
     dneg(beans_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(beans_H2) c_u_DeviationPairCap(beans_H2)_ 1
     dneg(beans_H3) c_e_DeviationIdentity(beans_H3)_ -1
     dneg(beans_H3) c_u_DeviationItemCap(beans)_ 1
     dneg(beans_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dneg(beans_H3) c_u_DeviationPairCap(beans_H3)_ 1
     dneg(milk_H1) c_e_DeviationIdentity(milk_H1)_ -1
     dneg(milk_H1) c_u_DeviationItemCap(milk)_ 1
     dneg(milk_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(milk_H1) c_u_DeviationPairCap(milk_H1)_ 1
     dneg(milk_H2) c_e_DeviationIdentity(milk_H2)_ -1
     dneg(milk_H2) c_u_DeviationItemCap(milk)_ 1
     dneg(milk_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(milk_H2) c_u_DeviationPairCap(milk_H2)_ 1
     dneg(milk_H3) c_e_DeviationIdentity(milk_H3)_ -1
     dneg(milk_H3) c_u_DeviationItemCap(milk)_ 1
     dneg(milk_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dneg(milk_H3) c_u_DeviationPairCap(milk_H3)_ 1
     dneg(rice_H1) c_e_DeviationIdentity(rice_H1)_ -1
     dneg(rice_H1) c_u_DeviationItemCap(rice)_ 1
     dneg(rice_H1) c_u_DeviationHouseholdCap(H1)_ 1
     dneg(rice_H1) c_u_DeviationPairCap(rice_H1)_ 1
     dneg(rice_H2) c_e_DeviationIdentity(rice_H2)_ -1
     dneg(rice_H2) c_u_DeviationItemCap(rice)_ 1
     dneg(rice_H2) c_u_DeviationHouseholdCap(H2)_ 1
     dneg(rice_H2) c_u_DeviationPairCap(rice_H2)_ 1
     dneg(rice_H3) c_e_DeviationIdentity(rice_H3)_ -1
     dneg(rice_H3) c_u_DeviationItemCap(rice)_ 1
     dneg(rice_H3) c_u_DeviationHouseholdCap(H3)_ 1
     dneg(rice_H3) c_u_DeviationPairCap(rice_H3)_ 1
RHS
     RHS c_u_U_link(cal_H1)_ 0
     RHS c_u_U_link(cal_H2)_ 0
     RHS c_u_U_link(cal_H3)_ 0
     RHS c_u_U_link(calc_H1)_ 0
     RHS c_u_U_link(calc_H2)_ 0
     RHS c_u_U_link(calc_H3)_ 0
     RHS c_u_U_link(prot_H1)_ 0
     RHS c_u_U_link(prot_H2)_ 0
     RHS c_u_U_link(prot_H3)_ 0
     RHS c_u_StockBalance(apples)_ 8
     RHS c_u_StockBalance(beans)_ 12
     RHS c_u_StockBalance(milk)_ 10
     RHS c_u_StockBalance(rice)_ 20
     RHS c_u_PurchaseBudget_ 10
     RHS c_e_DeviationIdentity(apples_H1)_ -0.88888888799999999
     RHS c_e_DeviationIdentity(apples_H2)_ -2.6666666640000001
     RHS c_e_DeviationIdentity(apples_H3)_ -4.4444444479999996
     RHS c_e_DeviationIdentity(beans_H1)_ -1.333333332
     RHS c_e_DeviationIdentity(beans_H2)_ -3.9999999960000001
     RHS c_e_DeviationIdentity(beans_H3)_ -6.6666666719999998
     RHS c_e_DeviationIdentity(milk_H1)_ -1.11111111
     RHS c_e_DeviationIdentity(milk_H2)_ -3.3333333300000003
     RHS c_e_DeviationIdentity(milk_H3)_ -5.5555555599999993
     RHS c_e_DeviationIdentity(rice_H1)_ -2.2222222199999999
     RHS c_e_DeviationIdentity(rice_H2)_ -6.6666666600000006
     RHS c_e_DeviationIdentity(rice_H3)_ -11.111111119999999
     RHS c_u_DeviationItemCap(apples)_ 7.2000000000000002
     RHS c_u_DeviationItemCap(beans)_ 10.800000000000001
     RHS c_u_DeviationItemCap(milk)_ 9
     RHS c_u_DeviationItemCap(rice)_ 18
     RHS c_u_DeviationHouseholdCap(H1)_ 45
     RHS c_u_DeviationHouseholdCap(H2)_ 45
     RHS c_u_DeviationHouseholdCap(H3)_ 45
     RHS c_u_DeviationPairCap(apples_H1)_ 7.2000000000000002
     RHS c_u_DeviationPairCap(apples_H2)_ 7.2000000000000002
     RHS c_u_DeviationPairCap(apples_H3)_ 7.2000000000000002
     RHS c_u_DeviationPairCap(beans_H1)_ 10.800000000000001
     RHS c_u_DeviationPairCap(beans_H2)_ 10.800000000000001
     RHS c_u_DeviationPairCap(beans_H3)_ 10.800000000000001
     RHS c_u_DeviationPairCap(milk_H1)_ 9
     RHS c_u_DeviationPairCap(milk_H2)_ 9
     RHS c_u_DeviationPairCap(milk_H3)_ 9
     RHS c_u_DeviationPairCap(rice_H1)_ 18
     RHS c_u_DeviationPairCap(rice_H2)_ 18
     RHS c_u_DeviationPairCap(rice_H3)_ 18
     RHS c_l_HouseholdFloor(H1)_ 0
     RHS c_l_HouseholdFloor(H2)_ 0
     RHS c_l_HouseholdFloor(H3)_ 0
     RHS c_l_NutrientFloor(cal)_ 0
     RHS c_l_NutrientFloor(calc)_ 0
     RHS c_l_NutrientFloor(prot)_ 0
     RHS c_l_PairFloor(cal_H1)_ 0
     RHS c_l_PairFloor(cal_H2)_ 0
     RHS c_l_PairFloor(cal_H3)_ 0
     RHS c_l_PairFloor(calc_H1)_ 0
     RHS c_l_PairFloor(calc_H2)_ 0
     RHS c_l_PairFloor(calc_H3)_ 0
     RHS c_l_PairFloor(prot_H1)_ 0
     RHS c_l_PairFloor(prot_H2)_ 0
     RHS c_l_PairFloor(prot_H3)_ 0
BOUNDS
 LI BOUND x(apples_H1) 0
 UI BOUND x(apples_H1) 3
 LI BOUND x(apples_H2) 0
 UI BOUND x(apples_H2) 9
 LI BOUND x(apples_H3) 0
 UI BOUND x(apples_H3) 15
 LI BOUND x(beans_H1) 0
 UI BOUND x(beans_H1) 3
 LI BOUND x(beans_H2) 0
 UI BOUND x(beans_H2) 9
 LI BOUND x(beans_H3) 0
 UI BOUND x(beans_H3) 15
 LI BOUND x(milk_H1) 0
 UI BOUND x(milk_H1) 3
 LI BOUND x(milk_H2) 0
 UI BOUND x(milk_H2) 9
 LI BOUND x(milk_H3) 0
 UI BOUND x(milk_H3) 15
 LI BOUND x(rice_H1) 0
 UI BOUND x(rice_H1) 3
 LI BOUND x(rice_H2) 0
 UI BOUND x(rice_H2) 9
 LI BOUND x(rice_H3) 0
 UI BOUND x(rice_H3) 15
 LO BOUND u(cal_H1) 0
 UP BOUND u(cal_H1) 1
 LO BOUND u(cal_H2) 0
 UP BOUND u(cal_H2) 1
 LO BOUND u(cal_H3) 0
 UP BOUND u(cal_H3) 1
 LO BOUND u(calc_H1) 0
 UP BOUND u(calc_H1) 1
 LO BOUND u(calc_H2) 0
 UP BOUND u(calc_H2) 1
 LO BOUND u(calc_H3) 0
 UP BOUND u(calc_H3) 1
 LO BOUND u(prot_H1) 0
 UP BOUND u(prot_H1) 1
 LO BOUND u(prot_H2) 0
 UP BOUND u(prot_H2) 1
 LO BOUND u(prot_H3) 0
 UP BOUND u(prot_H3) 1
 LO BOUND y(apples) 0
 LO BOUND y(beans) 0
 LO BOUND y(milk) 0
 LO BOUND y(rice) 0
 LO BOUND dpos(apples_H1) 0
 LO BOUND dpos(apples_H2) 0
 LO BOUND dpos(apples_H3) 0
 LO BOUND dpos(beans_H1) 0
 LO BOUND dpos(beans_H2) 0
 LO BOUND dpos(beans_H3) 0
 LO BOUND dpos(milk_H1) 0
 LO BOUND dpos(milk_H2) 0
 LO BOUND dpos(milk_H3) 0
 LO BOUND dpos(rice_H1) 0
 LO BOUND dpos(rice_H2) 0
 LO BOUND dpos(rice_H3) 0
 LO BOUND dneg(apples_H1) 0
 LO BOUND dneg(apples_H2) 0
 LO BOUND dneg(apples_H3) 0
 LO BOUND dneg(beans_H1) 0
 LO BOUND dneg(beans_H2) 0
 LO BOUND dneg(beans_H3) 0
 LO BOUND dneg(milk_H1) 0
 LO BOUND dneg(milk_H2) 0
 LO BOUND dneg(milk_H3) 0
 LO BOUND dneg(rice_H1) 0
 LO BOUND dneg(rice_H2) 0
 LO BOUND dneg(rice_H3) 0
ENDATA
