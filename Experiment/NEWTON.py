# This subroutine computes the steady state interest rate and labor supply and intercept for tax system using the
# classical newton method; inputs are the guesses for r, N and Tint and the subroutine calls resid that delivers the
# residual from markets clearing in the asset market, labor market and the gvernment budget constraint
def Newton(fun, gues1, gues2, gues3, gues4, gues5):
    global tol, adj
    global ngues1, ngues2, ngues3, ngues4, ngues5
    global epss, etas, high, low, nroot, xguess, itmax, errel, errabs
    global r, N, parameter, TrB, SS
    tol = 0.0025
    adj = 0.2
    epss = 0.1
    etas = 1
    nroot = 1
    itmax = 1000
    xguess = gues3
    low = 0.00000001
    high = 1000000
    for i in range(itmax):
        print('____________________________________________________________________')
        print("Newton iteration ", i + 1)
        fun(gues1, gues2, gues3, gues4, gues5)
        ngues1 = TFP * alpha * (As / (LabS * (1 + nn))) ** (alpha - 1) - delta
        ngues2 = LabS
        ngues4 = TrBn
        ngues5 = SSn
        # WITH GOUVEIA - STRAUSS: UPÏDATING A2
        if taxfn(high) * taxfn(low) < 0:
            ngues3 = scipy.optimize.brenth(taxfn, low, high, maxiter=itmax)
        else:
            ngues3 = 0
        if abs(fval1) / Y < tol and abs(fval2) / ngues2 < tol and abs(fval3) / Y < tol and abs(fval4) < tol and abs(
                fval5) < tol:
            print("Convergence Achieved")
            break
        if ngues3 == 0 and gues3==0 and i > 10:
            print("Convergence Failed, Marginal rate too low to finance government expenditure")
            break
        print(' ')
        print("      <variable>       <old guess>         <new guess>        <error>")
        print("  (1) interest rate ", gues1, ngues1, fval1 / Y)
        print("  (2) labor supply  ", gues2, ngues2, fval2 / ngues2)
        print("  (3) parameter     ", gues3, ngues3, fval3 / Y)
        print("  (4) bequest TrB   ", gues4, ngues4, fval4)
        print("  (5) SS benefit SS ", gues5, ngues5, fval5)
        print(" ")
        print('Tax System:  <parameter>  ', ngues3)
        print('Excess Dem. Goods Market ', exdem / Y)
        print('Total Shares in GDP      ', (C + Govcons + As * (delta + nn) / (1.0 + nn)) / Y)
        print("  K/Y=", As / ((1.0 + nn) * Y), "  I/Y=", (delta + nn) * As / ((1.0 + nn) * Y))
        print("  G/Y=", Govcons / Y, "  C/Y=", C / Y)
        print("  Avg hrs wrkd= ", hours)
        print("  Avg tax rate= ", Totinctax / (Y - delta * As / (1.0 + nn)))
        gues1 = (1 - adj) * gues1 + adj * ngues1
        gues2 = (1 - adj) * gues2 + adj * ngues2
        gues3 = (1 - adj) * gues3 + adj * ngues3
        gues4 = (1 - adj) * gues4 + adj * ngues4
        gues5 = (1 - adj) * gues5 + adj * ngues5
    r = ngues1
    N = ngues2
    parameter = ngues3
    TrB = ngues4
    SS = ngues5
    print(' ')
    print("Convergence achieved in ", i + 1, " Iterations")
    print("    <variable>       <old guess>       <new guess>         <error>")
    print("  (1) interest rate ", gues1, ngues1, fval1 / Y)
    print("  (2) labor supply  ", gues2, ngues2, fval2 / Y)
    print("  (3) parameter     ", gues3, ngues3, fval3 / Y)
    print("  (4) bequest TrB   ", gues4, ngues4, fval4)
    print("  (5) SS benefit SS ", gues5, ngues5, fval5)
    print('Excess Dem. Goods Mark.', exdem / Y, ' ')
    print('STATIONARY EQUILIBRIUM')
    print('''

    ###########################################################################

    ''')
    print("with Non-Separable utility")
    print("(betaNS,deltaNS,gamma)=", beta_NS, delta_NS, gamma)
    print("  K/Y=", As / ((1.0 + nn) * Y))
    print("  I/Y=", (delta + nn) * As / ((1.0 + nn) * Y))
    print("  G/Y=", Govcons / Y)
    print("  C/Y=", C / Y)
    print("  Avg hrs wrkd= ", hours)
    print("  Avg tax rate= ", Totinctax / (Y - delta * As / (1.0 + nn)))
    print("  Total bequest=", Tr, Y, Tr / Y)
    print('''

    ###########################################################################

    ''')


execfile("RESIDUALS.py")
execfile("EULER_EQN.py")
execfile("TAXFN.py")