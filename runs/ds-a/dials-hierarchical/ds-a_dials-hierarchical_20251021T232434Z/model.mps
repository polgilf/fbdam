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
 L  c_u_PurchaseActivation(apples)_
 L  c_u_PurchaseActivation(beans)_
 L  c_u_PurchaseActivation(milk)_
 L  c_u_PurchaseActivation(rice)_
 L  c_u_PurchaseNoWaste(apples)_
 L  c_u_PurchaseNoWaste(beans)_
 L  c_u_PurchaseNoWaste(milk)_
 L  c_u_PurchaseNoWaste(rice)_
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
     x(apples_H1) c_u_PurchaseNoWaste(apples)_ -1
     x(apples_H1) c_e_DeviationIdentity(apples_H1)_ -1
     x(apples_H2) c_u_U_link(cal_H2)_ -0.0086666666666666663
     x(apples_H2) c_u_U_link(calc_H2)_ -0.0024000000000000002
     x(apples_H2) c_u_U_link(prot_H2)_ -0.0016666666666666668
     x(apples_H2) c_u_StockBalance(apples)_ 1
     x(apples_H2) c_u_PurchaseNoWaste(apples)_ -1
     x(apples_H2) c_e_DeviationIdentity(apples_H2)_ -1
     x(apples_H3) c_u_U_link(cal_H3)_ -0.0054736842105263155
     x(apples_H3) c_u_U_link(calc_H3)_ -0.0015
     x(apples_H3) c_u_U_link(prot_H3)_ -0.00090909090909090909
     x(apples_H3) c_u_StockBalance(apples)_ 1
     x(apples_H3) c_u_PurchaseNoWaste(apples)_ -1
     x(apples_H3) c_e_DeviationIdentity(apples_H3)_ -1
     x(beans_H1) c_u_U_link(cal_H1)_ -0.15714285714285714
     x(beans_H1) c_u_U_link(calc_H1)_ -0.011000000000000001
     x(beans_H1) c_u_U_link(prot_H1)_ -0.41999999999999998
     x(beans_H1) c_u_StockBalance(beans)_ 1
     x(beans_H1) c_u_PurchaseNoWaste(beans)_ -1
     x(beans_H1) c_e_DeviationIdentity(beans_H1)_ -1
     x(beans_H2) c_u_U_link(cal_H2)_ -0.055
     x(beans_H2) c_u_U_link(calc_H2)_ -0.0044000000000000003
     x(beans_H2) c_u_U_link(prot_H2)_ -0.17500000000000002
     x(beans_H2) c_u_StockBalance(beans)_ 1
     x(beans_H2) c_u_PurchaseNoWaste(beans)_ -1
     x(beans_H2) c_e_DeviationIdentity(beans_H2)_ -1
     x(beans_H3) c_u_U_link(cal_H3)_ -0.034736842105263156
     x(beans_H3) c_u_U_link(calc_H3)_ -0.0027500000000000003
     x(beans_H3) c_u_U_link(prot_H3)_ -0.095454545454545459
     x(beans_H3) c_u_StockBalance(beans)_ 1
     x(beans_H3) c_u_PurchaseNoWaste(beans)_ -1
     x(beans_H3) c_e_DeviationIdentity(beans_H3)_ -1
     x(milk_H1) c_u_U_link(cal_H1)_ -0.030476190476190476
     x(milk_H1) c_u_U_link(calc_H1)_ -0.12000000000000001
     x(milk_H1) c_u_U_link(prot_H1)_ -0.066000000000000003
     x(milk_H1) c_u_StockBalance(milk)_ 1
     x(milk_H1) c_u_PurchaseNoWaste(milk)_ -1
     x(milk_H1) c_e_DeviationIdentity(milk_H1)_ -1
     x(milk_H2) c_u_U_link(cal_H2)_ -0.010666666666666668
     x(milk_H2) c_u_U_link(calc_H2)_ -0.048000000000000001
     x(milk_H2) c_u_U_link(prot_H2)_ -0.0275
     x(milk_H2) c_u_StockBalance(milk)_ 1
     x(milk_H2) c_u_PurchaseNoWaste(milk)_ -1
     x(milk_H2) c_e_DeviationIdentity(milk_H2)_ -1
     x(milk_H3) c_u_U_link(cal_H3)_ -0.0067368421052631583
     x(milk_H3) c_u_U_link(calc_H3)_ -0.030000000000000002
     x(milk_H3) c_u_U_link(prot_H3)_ -0.014999999999999999
     x(milk_H3) c_u_StockBalance(milk)_ 1
     x(milk_H3) c_u_PurchaseNoWaste(milk)_ -1
     x(milk_H3) c_e_DeviationIdentity(milk_H3)_ -1
     x(rice_H1) c_u_U_link(cal_H1)_ -0.17142857142857143
     x(rice_H1) c_u_U_link(calc_H1)_ -0.0030000000000000001
     x(rice_H1) c_u_U_link(prot_H1)_ -0.14000000000000001
     x(rice_H1) c_u_StockBalance(rice)_ 1
     x(rice_H1) c_u_PurchaseNoWaste(rice)_ -1
     x(rice_H1) c_e_DeviationIdentity(rice_H1)_ -1
     x(rice_H2) c_u_U_link(cal_H2)_ -0.060000000000000005
     x(rice_H2) c_u_U_link(calc_H2)_ -0.0012000000000000001
     x(rice_H2) c_u_U_link(prot_H2)_ -0.058333333333333334
     x(rice_H2) c_u_StockBalance(rice)_ 1
     x(rice_H2) c_u_PurchaseNoWaste(rice)_ -1
     x(rice_H2) c_e_DeviationIdentity(rice_H2)_ -1
     x(rice_H3) c_u_U_link(cal_H3)_ -0.037894736842105266
     x(rice_H3) c_u_U_link(calc_H3)_ -0.00075000000000000002
     x(rice_H3) c_u_U_link(prot_H3)_ -0.031818181818181815
     x(rice_H3) c_u_StockBalance(rice)_ 1
     x(rice_H3) c_u_PurchaseNoWaste(rice)_ -1
     x(rice_H3) c_e_DeviationIdentity(rice_H3)_ -1
     u(cal_H1) OBJ 1
     u(cal_H1) c_u_U_link(cal_H1)_ 1
     u(cal_H1) c_l_HouseholdFloor(H1)_ 0.24444444444444441
     u(cal_H1) c_l_HouseholdFloor(H2)_ -0.088888888888888892
     u(cal_H1) c_l_HouseholdFloor(H3)_ -0.088888888888888892
     u(cal_H1) c_l_NutrientFloor(cal)_ 0.27777777777777779
     u(cal_H1) c_l_NutrientFloor(calc)_ -0.055555555555555552
     u(cal_H1) c_l_NutrientFloor(prot)_ -0.055555555555555552
     u(cal_H1) c_l_PairFloor(cal_H1)_ 0.96666666666666667
     u(cal_H1) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(cal_H1) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(cal_H2) OBJ 1
     u(cal_H2) c_u_U_link(cal_H2)_ 1
     u(cal_H2) c_l_HouseholdFloor(H1)_ -0.088888888888888892
     u(cal_H2) c_l_HouseholdFloor(H2)_ 0.24444444444444441
     u(cal_H2) c_l_HouseholdFloor(H3)_ -0.088888888888888892
     u(cal_H2) c_l_NutrientFloor(cal)_ 0.27777777777777779
     u(cal_H2) c_l_NutrientFloor(calc)_ -0.055555555555555552
     u(cal_H2) c_l_NutrientFloor(prot)_ -0.055555555555555552
     u(cal_H2) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(cal_H2)_ 0.96666666666666667
     u(cal_H2) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(cal_H2) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(cal_H3) OBJ 1
     u(cal_H3) c_u_U_link(cal_H3)_ 1
     u(cal_H3) c_l_HouseholdFloor(H1)_ -0.088888888888888892
     u(cal_H3) c_l_HouseholdFloor(H2)_ -0.088888888888888892
     u(cal_H3) c_l_HouseholdFloor(H3)_ 0.24444444444444441
     u(cal_H3) c_l_NutrientFloor(cal)_ 0.27777777777777779
     u(cal_H3) c_l_NutrientFloor(calc)_ -0.055555555555555552
     u(cal_H3) c_l_NutrientFloor(prot)_ -0.055555555555555552
     u(cal_H3) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(cal_H3)_ 0.96666666666666667
     u(cal_H3) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(cal_H3) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(calc_H1) OBJ 1
     u(calc_H1) c_u_U_link(calc_H1)_ 1
     u(calc_H1) c_l_HouseholdFloor(H1)_ 0.24444444444444441
     u(calc_H1) c_l_HouseholdFloor(H2)_ -0.088888888888888892
     u(calc_H1) c_l_HouseholdFloor(H3)_ -0.088888888888888892
     u(calc_H1) c_l_NutrientFloor(cal)_ -0.055555555555555552
     u(calc_H1) c_l_NutrientFloor(calc)_ 0.27777777777777779
     u(calc_H1) c_l_NutrientFloor(prot)_ -0.055555555555555552
     u(calc_H1) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(calc_H1)_ 0.96666666666666667
     u(calc_H1) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(calc_H1) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(calc_H2) OBJ 1
     u(calc_H2) c_u_U_link(calc_H2)_ 1
     u(calc_H2) c_l_HouseholdFloor(H1)_ -0.088888888888888892
     u(calc_H2) c_l_HouseholdFloor(H2)_ 0.24444444444444441
     u(calc_H2) c_l_HouseholdFloor(H3)_ -0.088888888888888892
     u(calc_H2) c_l_NutrientFloor(cal)_ -0.055555555555555552
     u(calc_H2) c_l_NutrientFloor(calc)_ 0.27777777777777779
     u(calc_H2) c_l_NutrientFloor(prot)_ -0.055555555555555552
     u(calc_H2) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(calc_H2)_ 0.96666666666666667
     u(calc_H2) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(calc_H2) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(calc_H3) OBJ 1
     u(calc_H3) c_u_U_link(calc_H3)_ 1
     u(calc_H3) c_l_HouseholdFloor(H1)_ -0.088888888888888892
     u(calc_H3) c_l_HouseholdFloor(H2)_ -0.088888888888888892
     u(calc_H3) c_l_HouseholdFloor(H3)_ 0.24444444444444441
     u(calc_H3) c_l_NutrientFloor(cal)_ -0.055555555555555552
     u(calc_H3) c_l_NutrientFloor(calc)_ 0.27777777777777779
     u(calc_H3) c_l_NutrientFloor(prot)_ -0.055555555555555552
     u(calc_H3) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(calc_H3)_ 0.96666666666666667
     u(calc_H3) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(calc_H3) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(prot_H1) OBJ 1
     u(prot_H1) c_u_U_link(prot_H1)_ 1
     u(prot_H1) c_l_HouseholdFloor(H1)_ 0.24444444444444441
     u(prot_H1) c_l_HouseholdFloor(H2)_ -0.088888888888888892
     u(prot_H1) c_l_HouseholdFloor(H3)_ -0.088888888888888892
     u(prot_H1) c_l_NutrientFloor(cal)_ -0.055555555555555552
     u(prot_H1) c_l_NutrientFloor(calc)_ -0.055555555555555552
     u(prot_H1) c_l_NutrientFloor(prot)_ 0.27777777777777779
     u(prot_H1) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(prot_H1)_ 0.96666666666666667
     u(prot_H1) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(prot_H1) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(prot_H2) OBJ 1
     u(prot_H2) c_u_U_link(prot_H2)_ 1
     u(prot_H2) c_l_HouseholdFloor(H1)_ -0.088888888888888892
     u(prot_H2) c_l_HouseholdFloor(H2)_ 0.24444444444444441
     u(prot_H2) c_l_HouseholdFloor(H3)_ -0.088888888888888892
     u(prot_H2) c_l_NutrientFloor(cal)_ -0.055555555555555552
     u(prot_H2) c_l_NutrientFloor(calc)_ -0.055555555555555552
     u(prot_H2) c_l_NutrientFloor(prot)_ 0.27777777777777779
     u(prot_H2) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(prot_H2) c_l_PairFloor(prot_H2)_ 0.96666666666666667
     u(prot_H2) c_l_PairFloor(prot_H3)_ -0.033333333333333333
     u(prot_H3) OBJ 1
     u(prot_H3) c_u_U_link(prot_H3)_ 1
     u(prot_H3) c_l_HouseholdFloor(H1)_ -0.088888888888888892
     u(prot_H3) c_l_HouseholdFloor(H2)_ -0.088888888888888892
     u(prot_H3) c_l_HouseholdFloor(H3)_ 0.24444444444444441
     u(prot_H3) c_l_NutrientFloor(cal)_ -0.055555555555555552
     u(prot_H3) c_l_NutrientFloor(calc)_ -0.055555555555555552
     u(prot_H3) c_l_NutrientFloor(prot)_ 0.27777777777777779
     u(prot_H3) c_l_PairFloor(cal_H1)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(cal_H2)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(cal_H3)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(calc_H1)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(calc_H2)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(calc_H3)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(prot_H1)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(prot_H2)_ -0.033333333333333333
     u(prot_H3) c_l_PairFloor(prot_H3)_ 0.96666666666666667
     y(apples) c_u_StockBalance(apples)_ -1
     y(apples) c_u_PurchaseBudget_ 1.1000000000000001
     y(apples) c_u_PurchaseActivation(apples)_ 1
     y(apples) c_u_PurchaseNoWaste(apples)_ 1
     y(apples) c_e_DeviationIdentity(apples_H1)_ 0.1111111111111111
     y(apples) c_e_DeviationIdentity(apples_H2)_ 0.33333333333333331
     y(apples) c_e_DeviationIdentity(apples_H3)_ 0.55555555555555558
     y(apples) c_u_DeviationItemCap(apples)_ -0.40000000000000002
     y(apples) c_u_DeviationHouseholdCap(H1)_ -0.022222222222222223
     y(apples) c_u_DeviationHouseholdCap(H2)_ -0.066666666666666666
     y(apples) c_u_DeviationHouseholdCap(H3)_ -0.11111111111111112
     y(apples) c_u_DeviationPairCap(apples_H1)_ -0.066666666666666666
     y(apples) c_u_DeviationPairCap(apples_H2)_ -0.19999999999999998
     y(apples) c_u_DeviationPairCap(apples_H3)_ -0.33333333333333331
     y(beans) c_u_StockBalance(beans)_ -1
     y(beans) c_u_PurchaseBudget_ 1.2
     y(beans) c_u_PurchaseActivation(beans)_ 1
     y(beans) c_u_PurchaseNoWaste(beans)_ 1
     y(beans) c_e_DeviationIdentity(beans_H1)_ 0.1111111111111111
     y(beans) c_e_DeviationIdentity(beans_H2)_ 0.33333333333333331
     y(beans) c_e_DeviationIdentity(beans_H3)_ 0.55555555555555558
     y(beans) c_u_DeviationItemCap(beans)_ -0.40000000000000002
     y(beans) c_u_DeviationHouseholdCap(H1)_ -0.022222222222222223
     y(beans) c_u_DeviationHouseholdCap(H2)_ -0.066666666666666666
     y(beans) c_u_DeviationHouseholdCap(H3)_ -0.11111111111111112
     y(beans) c_u_DeviationPairCap(beans_H1)_ -0.066666666666666666
     y(beans) c_u_DeviationPairCap(beans_H2)_ -0.19999999999999998
     y(beans) c_u_DeviationPairCap(beans_H3)_ -0.33333333333333331
     y(milk) c_u_StockBalance(milk)_ -1
     y(milk) c_u_PurchaseBudget_ 0.90000000000000002
     y(milk) c_u_PurchaseActivation(milk)_ 1
     y(milk) c_u_PurchaseNoWaste(milk)_ 1
     y(milk) c_e_DeviationIdentity(milk_H1)_ 0.1111111111111111
     y(milk) c_e_DeviationIdentity(milk_H2)_ 0.33333333333333331
     y(milk) c_e_DeviationIdentity(milk_H3)_ 0.55555555555555558
     y(milk) c_u_DeviationItemCap(milk)_ -0.40000000000000002
     y(milk) c_u_DeviationHouseholdCap(H1)_ -0.022222222222222223
     y(milk) c_u_DeviationHouseholdCap(H2)_ -0.066666666666666666
     y(milk) c_u_DeviationHouseholdCap(H3)_ -0.11111111111111112
     y(milk) c_u_DeviationPairCap(milk_H1)_ -0.066666666666666666
     y(milk) c_u_DeviationPairCap(milk_H2)_ -0.19999999999999998
     y(milk) c_u_DeviationPairCap(milk_H3)_ -0.33333333333333331
     y(rice) c_u_StockBalance(rice)_ -1
     y(rice) c_u_PurchaseBudget_ 1
     y(rice) c_u_PurchaseActivation(rice)_ 1
     y(rice) c_u_PurchaseNoWaste(rice)_ 1
     y(rice) c_e_DeviationIdentity(rice_H1)_ 0.1111111111111111
     y(rice) c_e_DeviationIdentity(rice_H2)_ 0.33333333333333331
     y(rice) c_e_DeviationIdentity(rice_H3)_ 0.55555555555555558
     y(rice) c_u_DeviationItemCap(rice)_ -0.40000000000000002
     y(rice) c_u_DeviationHouseholdCap(H1)_ -0.022222222222222223
     y(rice) c_u_DeviationHouseholdCap(H2)_ -0.066666666666666666
     y(rice) c_u_DeviationHouseholdCap(H3)_ -0.11111111111111112
     y(rice) c_u_DeviationPairCap(rice_H1)_ -0.066666666666666666
     y(rice) c_u_DeviationPairCap(rice_H2)_ -0.19999999999999998
     y(rice) c_u_DeviationPairCap(rice_H3)_ -0.33333333333333331
     y_active(apples) c_u_PurchaseActivation(apples)_ -9.0909090909090899
     y_active(apples) c_u_PurchaseNoWaste(apples)_ 8
     y_active(beans) c_u_PurchaseActivation(beans)_ -8.3333333333333339
     y_active(beans) c_u_PurchaseNoWaste(beans)_ 12
     y_active(milk) c_u_PurchaseActivation(milk)_ -11.111111111111111
     y_active(milk) c_u_PurchaseNoWaste(milk)_ 10
     y_active(rice) c_u_PurchaseActivation(rice)_ -10
     y_active(rice) c_u_PurchaseNoWaste(rice)_ 20
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
     RHS c_u_PurchaseActivation(apples)_ 0
     RHS c_u_PurchaseActivation(beans)_ 0
     RHS c_u_PurchaseActivation(milk)_ 0
     RHS c_u_PurchaseActivation(rice)_ 0
     RHS c_u_PurchaseNoWaste(apples)_ 0
     RHS c_u_PurchaseNoWaste(beans)_ 0
     RHS c_u_PurchaseNoWaste(milk)_ 0
     RHS c_u_PurchaseNoWaste(rice)_ 0
     RHS c_e_DeviationIdentity(apples_H1)_ -0.88888888888888884
     RHS c_e_DeviationIdentity(apples_H2)_ -2.6666666666666665
     RHS c_e_DeviationIdentity(apples_H3)_ -4.4444444444444446
     RHS c_e_DeviationIdentity(beans_H1)_ -1.3333333333333333
     RHS c_e_DeviationIdentity(beans_H2)_ -4
     RHS c_e_DeviationIdentity(beans_H3)_ -6.666666666666667
     RHS c_e_DeviationIdentity(milk_H1)_ -1.1111111111111112
     RHS c_e_DeviationIdentity(milk_H2)_ -3.333333333333333
     RHS c_e_DeviationIdentity(milk_H3)_ -5.5555555555555554
     RHS c_e_DeviationIdentity(rice_H1)_ -2.2222222222222223
     RHS c_e_DeviationIdentity(rice_H2)_ -6.6666666666666661
     RHS c_e_DeviationIdentity(rice_H3)_ -11.111111111111111
     RHS c_u_DeviationItemCap(apples)_ 3.2000000000000002
     RHS c_u_DeviationItemCap(beans)_ 4.8000000000000007
     RHS c_u_DeviationItemCap(milk)_ 4
     RHS c_u_DeviationItemCap(rice)_ 8
     RHS c_u_DeviationHouseholdCap(H1)_ 1.1111111111111112
     RHS c_u_DeviationHouseholdCap(H2)_ 3.333333333333333
     RHS c_u_DeviationHouseholdCap(H3)_ 5.5555555555555554
     RHS c_u_DeviationPairCap(apples_H1)_ 0.53333333333333333
     RHS c_u_DeviationPairCap(apples_H2)_ 1.5999999999999999
     RHS c_u_DeviationPairCap(apples_H3)_ 2.6666666666666665
     RHS c_u_DeviationPairCap(beans_H1)_ 0.80000000000000004
     RHS c_u_DeviationPairCap(beans_H2)_ 2.3999999999999999
     RHS c_u_DeviationPairCap(beans_H3)_ 4
     RHS c_u_DeviationPairCap(milk_H1)_ 0.66666666666666663
     RHS c_u_DeviationPairCap(milk_H2)_ 1.9999999999999998
     RHS c_u_DeviationPairCap(milk_H3)_ 3.333333333333333
     RHS c_u_DeviationPairCap(rice_H1)_ 1.3333333333333333
     RHS c_u_DeviationPairCap(rice_H2)_ 3.9999999999999996
     RHS c_u_DeviationPairCap(rice_H3)_ 6.6666666666666661
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
 UI BOUND x(apples_H1) 5
 LI BOUND x(apples_H2) 0
 UI BOUND x(apples_H2) 9
 LI BOUND x(apples_H3) 0
 UI BOUND x(apples_H3) 15
 LI BOUND x(beans_H1) 0
 UI BOUND x(beans_H1) 5
 LI BOUND x(beans_H2) 0
 UI BOUND x(beans_H2) 9
 LI BOUND x(beans_H3) 0
 UI BOUND x(beans_H3) 15
 LI BOUND x(milk_H1) 0
 UI BOUND x(milk_H1) 5
 LI BOUND x(milk_H2) 0
 UI BOUND x(milk_H2) 9
 LI BOUND x(milk_H3) 0
 UI BOUND x(milk_H3) 15
 LI BOUND x(rice_H1) 0
 UI BOUND x(rice_H1) 5
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
 BV BOUND y_active(apples)
 BV BOUND y_active(beans)
 BV BOUND y_active(milk)
 BV BOUND y_active(rice)
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
