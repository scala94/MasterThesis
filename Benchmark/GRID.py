# DEFINING GRID FOR INDIVIDUAL ASSET HOLDING
blimit = 0
scale = 75
curve = 2.5

grida = np.zeros((na))
grida[0] = blimit
for a in range(1,na):
    grida[a] = grida[0] + scale*((a)/(na))**curve

# DEFINING GRID FOR INDIVIDUAL LABOUR SUPPLY
gridl = np.linspace(0,maxl,nl)
