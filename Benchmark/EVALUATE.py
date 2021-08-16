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

guesr = 0.05 # 0.041438697444057856
guesN = 9 # 8.970028611405061
guesP = 0 # 0.5166692838235117
guesB = 0.01 # 0.008390068117323292
guesS = 0.1 #0.075517453017608
guesT = 0 # 0.01978444082306181
bracket1 = 0.1 # 0.12294085194694512
bracket2 = 1 # 1.0740933104192982
bracket3 = 5 # 5.582503120733614
bracket4 = 10 # 12.022028601764658
Newton(resid,guesr,guesN,guesP,guesB,guesS,guesT)
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