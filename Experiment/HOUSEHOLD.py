# THIS SUBROUTINE SOLVES HOUSEHOLDS' PROBLEM
errel = 0.0000001
errabs = 0.00000001

Vfun[:,:,:,:] = 0
lfun[:,:,:,:] = 0
cfun[:,:,:,:] = 0
afun[:,:,:,:] = 0
vpfun[:,:,:,:] = 0

# VALUE FUNCTION OF LAST GENERATION
for a in range(na):
    earnl = 0
    earncap = r*(grida[a]+TrB)
    taxes = LabTax(parameter,thresold,earnl,earncap)
    lab = 0
    con = (SS + (1 + r)*(grida[a] + TrB) - taxes)/(1 + tauc)
    Vfun[:,:,a,J-1] = U(con,lab)
    lfun[:,:,a,J-1] = lab
    cfun[:,:,a,J-1] = con
    afun[:,:,a,J-1] = 0
    vpfun[:,:,a,J-1] = (1 + r*(1 - tauk))*marginal_utility(con,lab)

# COMPUTE OPTIMAL POLICIES FOR HOUSEHOLDS
for q in range(J-1):
    jc = J - q - 2
    for tyc in range(nty):
        for s in range(ns):
            for a in range(na):
                if jc >= jr:
                    lfun[tyc,s,a,jc] = 0
                    lbound = blimit
                    ubound = grida[na-1]
                    earnl = 0
                    earncap = r*(grida[a] + TrB)
                    taxes = LabTax(parameter,thresold,earnl,earncap)
                    lab = 0
                    conl = (SS + (1 + r)*(grida[a] + TrB) - taxes - lbound)/(1 + tauc)
                    conh = (SS + (1 + r)*(grida[a] + TrB) - taxes - ubound)/(1 + tauc)
                    basefun(grida,na,lbound)
                    vpml = 0
                    for sc in range(ns):
                        vpml = vpml + bbeta*SurvProb[jc]*pi[s,sc]*(vals[0]*vpfun[tyc,sc,inds[0],jc+1] + vals[1]*vpfun[tyc,sc,inds[1],jc+1])
                    basefun(grida,na,ubound)
                    vpmu = 0
                    for sc in range(ns):
                        vpmu = vpmu + bbeta*SurvProb[jc]*pi[s,sc]*(vals[0]*vpfun[tyc,sc,inds[0],jc+1] + vals[1]*vpfun[tyc,sc,inds[1],jc+1])
                    if marginal_utility(conl,lab) > vpml:
                        amax = lbound
                    elif marginal_utility(conh,lab) < vpmu:
                        amax = ubound
                    else:
                        maxfun = 1000
                        amax = scipy.optimize.brenth(euler_eqn, lbound, ubound, maxiter=maxfun)
                    afun[tyc,s,a,jc] = amax
                    earnl = 0
                    earncap = r*(grida[a] + TrB)
                    taxes = LabTax(parameter,thresold,earnl,earncap)
                    cfun[tyc,s,a,jc] = (SS + (1 + r)*(grida[a] + TrB) - taxes - amax)/(1 + tauc)
                    # UPDATE VALUE FUNCTION
                    basefun(grida,na,amax)
                    VM = np.empty((ns))
                    for j in range(ns):
                        VM[j] = vals[0]*Vfun[tyc,j,inds[0],jc+1] + vals[1]*Vfun[tyc,j,inds[1],jc+1]
                    Vfun[tyc,s,a,jc] = U(cfun[tyc,s,a,jc],lfun[tyc,s,a,jc]) + bbeta*SurvProb[jc]*sum(VM[:]*pi[s,:])
                    vpfun[tyc,s,a,jc] = (1 + r*(1 - tauk))*marginal_utility(cfun[tyc,s,a,jc],lfun[tyc,s,a,jc])
                else:
                    vhelp[:] = umin
                    for l in range(nl):
                        lbound = grida[0]
                        ubound = grida[na-1]
                        earnl0 = w*eta[s]*ep[tyc,jc]*gridl[l]   # LABOUR INCOME BEFORE SS TAX
                        earnl = earnl0 - b*taup*min(maxSS,earnl0) # LABOUR INCOME AFTER SS TAX PAID BY EMPLOYER
                        earncap = r*(grida[a] + TrB)
                        taxes = LabTax(parameter,thresold,earnl,earncap)
                        lab = gridl[l]
                        conl = (earnl0 - taup*min(maxSS,earnl0) + (1 + r)*(grida[a] + TrB) - taxes - lbound)/(1 + tauc)
                        conh = (earnl0 - taup*min(maxSS,earnl0) + (1 + r)*(grida[a] + TrB) - taxes - ubound)/(1 + tauc)
                        basefun(grida,na,lbound)
                        vpml = 0
                        for sc in range(ns):
                            vpml = vpml + bbeta*SurvProb[jc]*pi[s,sc]*(vals[0]*vpfun[tyc,sc,inds[0],jc + 1] + vals[1]*vpfun[tyc,sc,inds[1],jc+1])
                        basefun(grida,na,ubound)
                        vpmu = 0
                        for sc in range(ns):
                            vpmu = vpmu + bbeta*SurvProb[jc]*pi[s,sc]*(vals[0]*vpfun[tyc,sc,inds[0],jc + 1] + vals[1]*vpfun[tyc,sc,inds[1],jc+1])
                        if marginal_utility(conl,lab) > vpml:
                            amax = lbound
                        elif marginal_utility(conh,lab) < vpmu:
                            amax = ubound
                        else:
                            maxfun = 1000
                            amax = scipy.optimize.brenth(euler_eqn, lbound, ubound, maxiter=maxfun)
                        # SOLVE FOR OPTIMAL ASSET POLICY
                        ahelp[l] = amax
                        lhelp[l] = gridl[l]
                        earnl0 = w * eta[s] * ep[tyc, jc] * gridl[l]
                        earnl = earnl0 - b*taup*min(maxSS,earnl0)
                        earncap = r*(grida[a] + TrB)
                        taxes = LabTax(parameter,thresold,earnl,earncap)
                        chelp[l] = (earnl0 - taup*min(maxSS,earnl0) + (1 + r)*(grida[a] + TrB) - taxes - ahelp[l])/(1 + tauc)
                        basefun(grida,na,ahelp[l])
                        for j in range(ns):
                            VM[j] = vals[0] * Vfun[tyc, j, inds[0], jc + 1] + vals[1] * Vfun[tyc, j, inds[1], jc + 1]
                        vhelp[l] = U(chelp[l],lhelp[l]) + bbeta*SurvProb[jc]*sum(VM[:]*pi[s,:])
                        vphelp[l] = (1 + r*(1 - tauk))*marginal_utility(chelp[l],lhelp[l])
                    # CHECK WHICH l IS BEST
                    Vfun[tyc,s,a,jc] = max(vhelp)
                    pos = np.argmax(vhelp)
                    afun[tyc,s,a,jc] = ahelp[pos]
                    lfun[tyc,s,a,jc] = lhelp[pos]
                    cfun[tyc,s,a,jc] = chelp[pos]
                    vpfun[tyc,s,a,jc] = vphelp[pos]