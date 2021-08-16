martax = np.linspace(0.21,0.35,15)

def LabTax(param,thresold,earnlab,earncap):
    if earnlab + earncap <= param*thresold:
        LabTaxes = -(param*thresold - earnlab - earncap)
    else:
        LabTaxes = tafl*earnlab
    Taxes = LabTaxes + earncap * tauk
    return Taxes


for i in range(1):
    tafl = martax[i]
    import quantecon.markov as q
    execfile("MAIN.py")
