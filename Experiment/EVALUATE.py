# INITIALIZE VALUE FUNCTION AND POLICY FUNCTIONS

fu = 0.35
for tyc in range(nty):
    for s in range(ns):
        for a in range(na):
            for jc in range(J):
                Vfun[tyc,s,a,jc] = 0
                cfun[tyc,s,a,jc] = eta[s]*fu
                afun[tyc,s,a,jc] = grida[a]
                lfun[tyc,s,a,jc] = fu

# LOOP OF POLICIES TO EVALUATE

guesr = 0.04451757429430503 # 0.05
guesN = 8.372741032844008 # 9
guesP = 0.339540575106917 # 0.7
guesB = 0.008111485080549754 # 0.01
guesS = 0.0708986797833663 # 0.1
Newton(resid,guesr,guesN,guesP,guesB,guesS)
socwelf = 0
for j in range(J):
    socwelf = socwelf + Nu[j]*sum(sum(sum(Phi[:,:,:,j]*Vfun[:,:,:,j])))
# EX-ANTE
socwelf2 = sum(sum(sum(Phi[:, :, :, 0] * Vfun[:, :, :, 0])))
# LOW AND HIGH
socwelf_L = sum(sum(Phi[0,:,:,0]*Vfun[0,:,:,0]))
socwelf_H = sum(sum(Phi[1,:,:,1]*Vfun[1,:,:,1]))
# UTILITALIAN
socwelf_U = 0
for tyc in range(nty):
    for s in range(ns):
        for a in range(na):
            for jc in range(J):
                con = cfun[tyc,s,a,jc]
                lab = lfun[tyc,s,a,jc]
                socwelf_U = socwelf_U + Phi[tyc,s,a,jc]*Nu[jc]/sum(Nu)*(1/(1 - sigma))*(((con**gamma)*((1 - lab)**(1 - gamma)))**(1 - sigma))
# SAVE WELFARE MEASURE
############################################
# MEASURES OF INEQUALITY
for jc in range(J):
    phitot[:,:,:,jc] = mu[jc]*Phi[:,:,:,jc]
if sum(sum(sum(sum(phitot)))) < 0.999 or sum(sum(sum(sum(phitot)))) > 1.001:
    print(sum(sum(sum(sum(phitot)))),"should be one")
print('(a)', 'COMPUTED AN EQUILIBRIUM FOR THE TAX SYSTEM:')