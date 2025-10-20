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
     x(apples_H1) c_u_U_link(cal_H1)_ -0.24761904761904763
     x(apples_H1) c_u_U_link(calc_H1)_ -0.059999999999999998
     x(apples_H1) c_u_U_link(prot_H1)_ -0.040000000000000001
     x(apples_H1) c_u_StockBalance(apples)_ 1
     x(apples_H2) c_u_U_link(cal_H2)_ -0.08666666666666667
     x(apples_H2) c_u_U_link(calc_H2)_ -0.024
     x(apples_H2) c_u_U_link(prot_H2)_ -0.016666666666666666
     x(apples_H2) c_u_StockBalance(apples)_ 1
     x(apples_H3) c_u_U_link(cal_H3)_ -0.05473684210526316
     x(apples_H3) c_u_U_link(calc_H3)_ -0.014999999999999999
     x(apples_H3) c_u_U_link(prot_H3)_ -0.0090909090909090905
     x(apples_H3) c_u_StockBalance(apples)_ 1
     x(beans_H1) c_u_U_link(cal_H1)_ -1.5714285714285714
     x(beans_H1) c_u_U_link(calc_H1)_ -0.11
     x(beans_H1) c_u_U_link(prot_H1)_ -4.2000000000000002
     x(beans_H1) c_u_StockBalance(beans)_ 1
     x(beans_H2) c_u_U_link(cal_H2)_ -0.54999999999999993
     x(beans_H2) c_u_U_link(calc_H2)_ -0.044000000000000004
     x(beans_H2) c_u_U_link(prot_H2)_ -1.75
     x(beans_H2) c_u_StockBalance(beans)_ 1
     x(beans_H3) c_u_U_link(cal_H3)_ -0.3473684210526316
     x(beans_H3) c_u_U_link(calc_H3)_ -0.0275
     x(beans_H3) c_u_U_link(prot_H3)_ -0.95454545454545447
     x(beans_H3) c_u_StockBalance(beans)_ 1
     x(milk_H1) c_u_U_link(cal_H1)_ -0.30476190476190479
     x(milk_H1) c_u_U_link(calc_H1)_ -1.2
     x(milk_H1) c_u_U_link(prot_H1)_ -0.66000000000000003
     x(milk_H1) c_u_StockBalance(milk)_ 1
     x(milk_H2) c_u_U_link(cal_H2)_ -0.10666666666666666
     x(milk_H2) c_u_U_link(calc_H2)_ -0.48000000000000004
     x(milk_H2) c_u_U_link(prot_H2)_ -0.27500000000000002
     x(milk_H2) c_u_StockBalance(milk)_ 1
     x(milk_H3) c_u_U_link(cal_H3)_ -0.067368421052631577
     x(milk_H3) c_u_U_link(calc_H3)_ -0.29999999999999999
     x(milk_H3) c_u_U_link(prot_H3)_ -0.14999999999999999
     x(milk_H3) c_u_StockBalance(milk)_ 1
     x(rice_H1) c_u_U_link(cal_H1)_ -1.7142857142857142
     x(rice_H1) c_u_U_link(calc_H1)_ -0.029999999999999999
     x(rice_H1) c_u_U_link(prot_H1)_ -1.4000000000000001
     x(rice_H1) c_u_StockBalance(rice)_ 1
     x(rice_H2) c_u_U_link(cal_H2)_ -0.59999999999999998
     x(rice_H2) c_u_U_link(calc_H2)_ -0.012
     x(rice_H2) c_u_U_link(prot_H2)_ -0.58333333333333337
     x(rice_H2) c_u_StockBalance(rice)_ 1
     x(rice_H3) c_u_U_link(cal_H3)_ -0.37894736842105264
     x(rice_H3) c_u_U_link(calc_H3)_ -0.0074999999999999997
     x(rice_H3) c_u_U_link(prot_H3)_ -0.31818181818181818
     x(rice_H3) c_u_StockBalance(rice)_ 1
     u(cal_H1) OBJ 1
     u(cal_H1) c_u_U_link(cal_H1)_ 1
     u(cal_H1) c_l_PairFloor(cal_H1)_ 0.91111111111111109
     u(cal_H1) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(cal_H1) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(cal_H2) OBJ 1
     u(cal_H2) c_u_U_link(cal_H2)_ 1
     u(cal_H2) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(cal_H2)_ 0.91111111111111109
     u(cal_H2) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(cal_H2) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(cal_H3) OBJ 1
     u(cal_H3) c_u_U_link(cal_H3)_ 1
     u(cal_H3) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(cal_H3)_ 0.91111111111111109
     u(cal_H3) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(cal_H3) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(calc_H1) OBJ 1
     u(calc_H1) c_u_U_link(calc_H1)_ 1
     u(calc_H1) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(calc_H1)_ 0.91111111111111109
     u(calc_H1) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(calc_H1) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(calc_H2) OBJ 1
     u(calc_H2) c_u_U_link(calc_H2)_ 1
     u(calc_H2) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(calc_H2)_ 0.91111111111111109
     u(calc_H2) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(calc_H2) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(calc_H3) OBJ 1
     u(calc_H3) c_u_U_link(calc_H3)_ 1
     u(calc_H3) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(calc_H3)_ 0.91111111111111109
     u(calc_H3) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(calc_H3) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(prot_H1) OBJ 1
     u(prot_H1) c_u_U_link(prot_H1)_ 1
     u(prot_H1) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(prot_H1)_ 0.91111111111111109
     u(prot_H1) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(prot_H1) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(prot_H2) OBJ 1
     u(prot_H2) c_u_U_link(prot_H2)_ 1
     u(prot_H2) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(prot_H2) c_l_PairFloor(prot_H2)_ 0.91111111111111109
     u(prot_H2) c_l_PairFloor(prot_H3)_ -0.088888888888888892
     u(prot_H3) OBJ 1
     u(prot_H3) c_u_U_link(prot_H3)_ 1
     u(prot_H3) c_l_PairFloor(cal_H1)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(cal_H2)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(cal_H3)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(calc_H1)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(calc_H2)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(calc_H3)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(prot_H1)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(prot_H2)_ -0.088888888888888892
     u(prot_H3) c_l_PairFloor(prot_H3)_ 0.91111111111111109
     y(apples) c_u_StockBalance(apples)_ -1
     y(apples) c_u_PurchaseBudget_ 1.1000000000000001
     y(beans) c_u_StockBalance(beans)_ -1
     y(beans) c_u_PurchaseBudget_ 1.2
     y(milk) c_u_StockBalance(milk)_ -1
     y(milk) c_u_PurchaseBudget_ 0.90000000000000002
     y(rice) c_u_StockBalance(rice)_ -1
     y(rice) c_u_PurchaseBudget_ 1
     dpos(apples_H1) c_u_DeviationPairCap(apples_H1)_ 1
     dpos(apples_H2) c_u_DeviationPairCap(apples_H2)_ 1
     dpos(apples_H3) c_u_DeviationPairCap(apples_H3)_ 1
     dpos(beans_H1) c_u_DeviationPairCap(beans_H1)_ 1
     dpos(beans_H2) c_u_DeviationPairCap(beans_H2)_ 1
     dpos(beans_H3) c_u_DeviationPairCap(beans_H3)_ 1
     dpos(milk_H1) c_u_DeviationPairCap(milk_H1)_ 1
     dpos(milk_H2) c_u_DeviationPairCap(milk_H2)_ 1
     dpos(milk_H3) c_u_DeviationPairCap(milk_H3)_ 1
     dpos(rice_H1) c_u_DeviationPairCap(rice_H1)_ 1
     dpos(rice_H2) c_u_DeviationPairCap(rice_H2)_ 1
     dpos(rice_H3) c_u_DeviationPairCap(rice_H3)_ 1
     dneg(apples_H1) c_u_DeviationPairCap(apples_H1)_ 1
     dneg(apples_H2) c_u_DeviationPairCap(apples_H2)_ 1
     dneg(apples_H3) c_u_DeviationPairCap(apples_H3)_ 1
     dneg(beans_H1) c_u_DeviationPairCap(beans_H1)_ 1
     dneg(beans_H2) c_u_DeviationPairCap(beans_H2)_ 1
     dneg(beans_H3) c_u_DeviationPairCap(beans_H3)_ 1
     dneg(milk_H1) c_u_DeviationPairCap(milk_H1)_ 1
     dneg(milk_H2) c_u_DeviationPairCap(milk_H2)_ 1
     dneg(milk_H3) c_u_DeviationPairCap(milk_H3)_ 1
     dneg(rice_H1) c_u_DeviationPairCap(rice_H1)_ 1
     dneg(rice_H2) c_u_DeviationPairCap(rice_H2)_ 1
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
     RHS c_u_DeviationPairCap(apples_H1)_ 0
     RHS c_u_DeviationPairCap(apples_H2)_ 0
     RHS c_u_DeviationPairCap(apples_H3)_ 0
     RHS c_u_DeviationPairCap(beans_H1)_ 0
     RHS c_u_DeviationPairCap(beans_H2)_ 0
     RHS c_u_DeviationPairCap(beans_H3)_ 0
     RHS c_u_DeviationPairCap(milk_H1)_ 0
     RHS c_u_DeviationPairCap(milk_H2)_ 0
     RHS c_u_DeviationPairCap(milk_H3)_ 0
     RHS c_u_DeviationPairCap(rice_H1)_ 0
     RHS c_u_DeviationPairCap(rice_H2)_ 0
     RHS c_u_DeviationPairCap(rice_H3)_ 0
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
