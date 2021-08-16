# THIS SUBROUTINE COMPUTES STEADY STATE DISTRIBUTION OF ASSETS

TT = np.zeros((nty, ns, na, ns, na))
Phi = np.zeros((nty,ns,na,J))
help = np.zeros((J))
ADis = np.zeros((na))
probb = np.zeros((J))
Trn = np.zeros((ns,J))
# real(prec), dimension(2)::vals,
# real(prec)::Trn(ns, J), Transagg1, Tr1, Transagg2, earnl, earnl0, earncap,

earnings = np.zeros((nty, ns, na, J))
logearnings = np.zeros((nty, ns, na, J))

# Initialize Distribution by Computing Distribution for first Generation

for tyc in range(nty):
    for s in range(ns):
        Phi[tyc,s,0,0] = measty[tyc]*pini[s]

# Loop to find distributions for generations 2 to J
for jc in range(1,J):
    TT[:, :, :, :, :] = 0
    for tyc in range(nty):
        for s in range(ns):
            for a in range(na):
                for sc in range(ns):
                    basefun(grida,na,afun[tyc,s,a,jc-1])
                    TT[tyc,sc,inds[0],s,a] = vals[0] * pi[s,sc]
                    TT[tyc,sc,inds[1],s,a] = vals[1] * pi[s,sc]
    for tyc in range(nty):
        for sc in range(ns):
            for ac in range(na):
                for s in range(ns):
                    for a in range(na):
                        Phi[tyc,sc,ac,jc] = Phi[tyc,sc,ac,jc] + Phi[tyc,s,a,jc-1] * TT[tyc,sc,ac,s,a]

# Find Stationary Distribution over Asset Holdings

for a in range(na):
    for jc in range(J):
        help[jc] = sum(sum(Phi[:,:,a,jc]))
    ADis[a] = sum(help*mu)

if ADis[na-1] > 0:
    print("Enlarge Grid", ADis[na-1])

if sum(ADis[:]) > 1.01 or sum(ADis[:]) < 0.99:
    print("Should equal 1", sum(ADis[:]))
    print('ADis in DISTRIB.f90.')


for jc in range(J):
    if sum(sum(sum(Phi[:,:,:,jc]))) > 1.001 or sum(sum(sum(Phi[:,:,:,jc]))) < 0.999:
        print("Should equal 1", sum(sum(sum(Phi[:,:,:,jc]))))
        print("Phi in DISTRIB.f90")

# Find Aggregate Asset Holdings(end of Period)
for jc in range(J):
    abar[jc] = 0
    astartbar[jc] = 0
    for tyc in range(nty):
        abartype[jc,tyc] = 0
        astartbartype[jc,tyc] = 0
        for s in range(ns):
            abar[jc] = abar[jc] + sum(Phi[tyc,s,:,jc]*afun[tyc,s,:,jc])
            astartbar[jc] = astartbar[jc] + sum(Phi[tyc,s,:,jc]*grida[:])
            abartype[jc,tyc] = abartype[jc,tyc] + sum(Phi[tyc,s,:,jc]*afun[tyc,s,:,jc])/measty[tyc]
            astartbartype[jc,tyc] = astartbartype[jc,tyc] + sum(Phi[tyc,s,:,jc]*grida[:])/measty[tyc]

# Computing aggregate labor supply
for jc in range(J):
    lbar[jc] = 0
    for tyc in range(nty):
        lbartype[jc,tyc] = 0
        for s in range(ns):
            lbar[jc] = lbar[jc] + sum(eta[s]*ep[tyc,jc]*Phi[tyc,s,:,jc]*lfun[tyc,s,:,jc])
            lbartype[jc,tyc] = lbartype[jc,tyc] + sum(eta[s]*ep[tyc,jc]*Phi[tyc,s,:,jc]*lfun[tyc,s,:,jc])/measty[tyc]

for jc in range(J):
    labar[jc] = 0
    for tyc in range(nty):
        labartype[jc,tyc] = 0
        for s in range(ns):
            labar[jc] = labar[jc] + sum(Phi[tyc,s,:,jc]*lfun[tyc,s,:,jc])
            labartype[jc,tyc] = labartype[jc,tyc] + sum(Phi[tyc,s,:,jc]*lfun[tyc,s,:,jc])/measty[tyc]

# Compute average hours worked

hours = sum(Nu[0:jr-1]*labar[0: jr-1])/sum(Nu[0: jr-1])

# Compute Income Statistics over the life cycle

for jc in range(jr-1):
    probb[jc] = 0
    meanearn[jc] = 0
    logmean[jc] = 0
    varlogearn[jc] = 0
    for tyc in range(nty):
        meanearntype[jc,tyc] = 0
        logmeantype[jc,tyc] = 0
        for s in range(ns):
            for a in range(na): # Labor Income before taxes (this is where we should estimate the stochastic process parameters on)
                earnings[tyc,s,a,jc] = eta[s]*ep[tyc,jc]*lfun[tyc,s,a,jc]*w
                meanearn[jc] = meanearn[jc] + earnings[tyc,s,a,jc] * Phi[tyc,s,a,jc]
                meanearntype[jc,tyc] = meanearntype[jc,tyc] + earnings[tyc,s,a,jc]*Phi[tyc,s,a,jc]/measty[tyc]
                if earnings[tyc,s,a,jc] > 0.00001:
                    logearnings[tyc,s,a,jc] = np.log(earnings[tyc,s,a,jc])
                    logmean[jc] = logmean[jc] + logearnings[tyc,s,a,jc]*Phi[tyc,s,a,jc]
                    logmeantype[jc,tyc] = logmeantype[jc,tyc] + logearnings[tyc,s,a,jc]*Phi[tyc,s,a,jc]/measty[tyc]
                    probb[jc] = probb[jc] + Phi[tyc,s,a,jc]
    logmean[jc] = logmean[jc]/probb[jc]
    # Variance of Log-Earnings
    for tyc in range(nty):
        varlogearntype[jc,tyc] = 0
        for s in range(ns):
            for a in range(na):
                if earnings[tyc,s,a,jc] > 0.00001 and Phi[tyc,s,a,jc] > 0:
                    varlogearn[jc] = varlogearn[jc] + Phi[tyc,s,a,jc]*(logearnings[tyc,s,a,jc] - logmean[jc])**2
                    varlogearntype[jc,tyc] = varlogearntype[jc,tyc] + (Phi[tyc,s,a,jc]/measty[tyc])*(logearnings[tyc,s,a,jc] - logmeantype[jc,tyc])**2
    varlogearn[jc] = varlogearn[jc]/probb[jc]



# Computing aggregate Consumption

for jc in range(J):
    cbar[jc] = 0
    for tyc in range(nty):
        cbartype[jc,tyc] = 0
        for s in range(ns):
            cbar[jc] = cbar[jc] + sum(Phi[tyc,s,:,jc]*cfun[tyc,s,:,jc])
            cbartype[jc,tyc] = cbartype[jc,tyc] + sum(Phi[tyc,s,:,jc]*cfun[tyc,s,:,jc])/measty[tyc]

# Computing total taxes paid

Totinctax = 0
TotSStax = 0

for jc in range(J):
    for tyc in range(nty):
        for s in range(ns):
            for a in range(na):
                if jc < jr:
                    earnl0 = w*eta[s]*ep[tyc,jc]*lfun[tyc,s,a,jc]
                    earnl = earnl0 - b*taup*min(maxSS,earnl0)
                else:
                    earnl0 = 0
                    earnl = 0
                earncap = r*(grida[a] + TrB)
                Totinctax = Totinctax + Nu[jc]*Phi[tyc,s,a,jc]*LabTax(parameter,thresold,earnl,earncap)
                TotSStax = TotSStax + Nu[jc]*Phi[tyc,s,a,jc]*taup*min(maxSS,earnl0)

LabS = sum(Nu[:]*lbar[:])
As = sum(Nu[:]*abar[:])
Astart = sum(Nu[:]*astartbar[:])
Trstart = sum(Nu[:])*TrB
C = sum(Nu[:]*cbar[:])

for jc in range(J):
    for s in range(ns):
        Trn[s,jc] = Nu[jc]*(1 - SurvProb[jc])*sum(sum(Phi[:,s,:,jc]*afun[:,s,:,jc]))

EarnDist = np.zeros((nty, ns, na, J))
for jc in range(J):
    for tyc in range(nty):
        for s in range(ns):
            for a in range(na):
                if jc >= jr:
                    TOTEA = r * (grida[a] + TrB)
                else:
                    TOTEA = w * eta[s] * ep[tyc, jc] * lfun[tyc, s, a, jc] + r * (grida[a] + TrB)
                EarnDist[tyc,s,a,jc] = TOTEA
EarnDist = np.sort(EarnDist.ravel())

Tr = (1 + r)*sum(sum(Trn))/(1 + nn)
Transagg = (1 + r)*sum(sum(Trn))
TrBn = (sum(sum(Trn))/(1 + nn))/sum(Nu) # accidental bequest lump-sum transferred to each agent
SSn = TotSStax/sum(Nu[jr:J-1])
