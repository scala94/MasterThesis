# THIS SUBROUTINE COMPUTES THE ERRORS FROM ITERATIONS
# resid(x1,x2,x3,x4,x5) -> it gives back fv1,fv2,fv3,fv4,fv5
def resid(x1,x2,x3,x4,x5):
    global r,N,parameter,TrB,SS
    global K,Y,w,exdem
    global maxSS
    global fval1,fval2,fval3,fval4,fval5

    r = x1
    N = x2
    parameter = x3
    TrB = x4
    SS = x5

    K = N*((alpha*TFP)/(r + delta))**(1/(1 - alpha)) # CAPITAL STOCK
    Y = TFP*(K**alpha)*(N**(1-alpha))                # AGGREGATE OUTPUT
    w = (1-alpha)*Y/N                                # WAGES
    w = w/(1 + 1/3*taup)

    maxSS = maxSSrat*Y/sum(Nu)

    # SOLVE HOUSEHOLD PROBLEM: call household
    execfile("HOUSEHOLD.py")

    # FIND STATIONARY DISTRIBUTION: call distribution
    execfile("DISTRIBUTION.py")

    # COMPUTE RESIDUALS OF FUNCTIONS WE WANT TO SET TO ZERO
    fval1 = As - K*(1+nn)
    fval2 = LabS-N
    fval3 = Govcons - tauc*C - Totinctax
    fval4 = TrB - TrBn
    fval5 = SS - SSn
    # GOODS MARKET CLEARING
    Y = TFP*(K**alpha)*(LabS**(1-alpha))
    exdem = C+As-(1-delta)*K + Govcons - Y