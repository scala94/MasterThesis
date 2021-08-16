def euler_eqn(x):
    global con,lab
    global vpm
    vpm = np.zeros((ns))
    if jc < jr:
        earnl0 = w*eta[s]*ep[tyc,jc]*gridl[l]
        earnl = earnl0 - b*taup*min(maxSS,earnl0)
        earncap = r*(grida[a] + TrB)
        taxes = LabTax(parameter,thresold,earnl,earncap)
        lab = gridl[l]
        con = (earnl0 - taup*min(maxSS,earnl0) + (1 + r)*(grida[a] + TrB) - taxes - x)/(1 + tauc)
    else:
        earnl = 0
        earncap = r*(grida[a] + TrB)
        taxes = LabTax(parameter,thresold,earnl,earncap)
        lab = 0
        con = (SS + (1 + r)*(grida[a] + TrB) - taxes - x)/(1 + tauc)
    basefun(grida,na,x)
    for i in range(ns):
        vpm[i] = vals[0]*vpfun[tyc,i,inds[0],jc + 1] + vals[1]*vpfun[tyc,i,inds[1],jc + 1]
    EULER_EQN = -marginal_utility(con,lab)+bbeta*SurvProb[jc]*sum(vpm[:]*pi[s,:])
    return EULER_EQN
