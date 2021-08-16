martax = np.linspace(0.21,0.35,12)

def LabTax(param,thresold,earnlab,earncap):
    if earnlab + earncap <= param*thresold:
        LabTaxes = -(param*thresold - earnlab - earncap)
    else:
        LabTaxes = tafl*earnlab
    Taxes = LabTaxes + earncap * tafl
    return Taxes


# tax 22
print("flat tax",martax[1])
tafl = martax[1]
import quantecon.markov as q
execfile("MAIN.py")

# tax 23
print("flat tax",martax[2])
tafl = martax[2]
import quantecon.markov as q
execfile("MAIN.py")

# tax 24
print("flat tax",martax[3])
tafl = martax[3]
import quantecon.markov as q
execfile("MAIN.py")

# tax 25
print("flat tax",martax[4])
tafl = martax[4]
import quantecon.markov as q
execfile("MAIN.py")

# tax 26
print("flat tax",martax[5])
tafl = martax[5]
import quantecon.markov as q
execfile("MAIN.py")

# tax 27
print("flat tax",martax[6])
tafl = martax[6]
import quantecon.markov as q
execfile("MAIN.py")

# tax 28
print("flat tax",martax[7])
tafl = martax[7]
import quantecon.markov as q
execfile("MAIN.py")

# tax 29
print("flat tax",martax[8])
tafl = martax[8]
import quantecon.markov as q
execfile("MAIN.py")

# tax 30
print("flat tax",martax[9])
tafl = martax[9]
import quantecon.markov as q
execfile("MAIN.py")

# tax 31
print("flat tax",martax[10])
tafl = martax[10]
import quantecon.markov as q
execfile("MAIN.py")