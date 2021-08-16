# THIS FUNCTION COMPUTES THE TOTAL TAX
def taxfn(x):
    global taxfn
    global captax
    global dummy, earnl
    if x < 0 and parameter > 0.000001:
        dummy = 0.001 + x/(10**25)
    else:
        dummy = x
    Totinctax = 0
    for jc in range(J):
        for tyc in range(nty):
            for s in range(ns):
                for a in range(na):
                    if jc < jr:
                        earnl0 = w*eta[s]*ep[tyc,jc]*lfun[tyc,s,a,jc]
                        earnl = earnl0 - b*taup*earnl0
                    else:
                        earnl = 0
                    earncap = r*(grida[a] + TrB)
                    Totinctax = Totinctax + Nu[jc]*Phi[tyc,s,a,jc]*LabTax(dummy,ngues6,earnl,earncap)
    TAXFN = Govcons - tauc*C - Totinctax
    return TAXFN