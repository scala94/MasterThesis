# THIS IS THE MODULE FOR PARAMETERS AND VARIABLES DEFINITION
# SIZE FOR GRIDS
ns = 5
na = 51
nl = 33
nty = 2
maxit = 10000

# POPULATION
jr = 42
J = 76
nn = 0.00236

# PARAMETERS TO BE CALIBRATED FOR EACH PREFERENCE SPECS (TO BE CALIBRATED)
beta_NS = 0.965  # non separable
delta_NS = 0.077

# PARAMETERS FOR NON SEPARABLE PREFERENCE
gamma = 0.4
sigma = 3

# PRODUCTION FUNCTION
alpha = 0.35
TFP = 1

# GOVERNMENT POLICIES
govconsNS = 4.2 # 4.2  # Gov consumption Non Separable utility

tauc = 0.185 # CONSUMPTION TAX
tauk = 0.26  # CAPITAL INCOME TAX
b = 2/3      # share of SS contributions paid by the agents

# LABOUR GRID parameters
umin = 100
penscale = 10000000
maxl = 0.99

# VALUE OF BORROWING CONSTRAINT
blimit = 0

# SHOCKS AND TRANSITION PROBABILITIES
pi = np.zeros((ns,ns))
pistat = np.zeros((ns))
eta = np.zeros((ns))
pini = np.zeros((ns))

# DEMOGRAPHIC PARAMETERS
ep = np.empty((nty,J))
opttax = np.zeros((5))
optvfun = np.zeros((nty,ns,na,J))
optcfun = np.zeros((nty,ns,na,J))
optlfun = np.zeros((nty,ns,na,J))
optafun = np.zeros((nty,ns,na,J))

# DISTRIBUTION OVER STATE SPACE
Phi = np.zeros((nty,ns,na,J))
phitot = np.zeros((nty,ns,na,J))
optphi = np.zeros((nty,ns,na,J))

# HOUSEHOLD VALUE AND POLICY FUNCTION
Vfun =  np.zeros((nty,ns,na,J))
cfun = np.zeros((nty,ns,na,J))
lfun = np.zeros((nty,ns,na,J))
afun = np.zeros((nty,ns,na,J))
vpfun = np.zeros((nty,ns,na,J))

# ASSET DISTRIBUTION
Adis = np.zeros((na))

# AVERAGE VARIABLES BY AGE
abar = np.zeros((J))
lbar = np.zeros((J))
labar = np.zeros((J))
cbar = np.zeros((J))
astartbar = np.zeros((J))
meanearn = np.zeros((J))
logmean = np.zeros((J))
varlogearn = np.zeros((J))

# AVERAGE VARIABLES BY AGE AND TYPE
abartype = np.zeros((J,nty))
lbartype = np.zeros((J,nty))
labartype = np.zeros((J,nty))
cbartype = np.zeros((J,nty))
astartbartype = np.zeros((J,nty))
meanearntype = np.zeros((J,nty))
logmeantype = np.zeros((J,nty))
varlogearntype = np.zeros((J,nty))

# Prices of capital and labor; labor supply and capital stock, and other (r,w,N,LabS,K,As,Astart,Y,C,Tr,exdem,Totinctax,hours,Transagg,stdle,stdleini)

#SS TAXES AND BENEFITS
taup = 0.124
maxSSrat = 1000000000000

# WELFARE MEASURES
equivar = np.zeros((nty,ns,na,J))
equivarss = np.zeros((nty,ns,na,J))

# HOUSEHOLDS
vhelp = np.zeros((nl))
ahelp = np.zeros((nl))
lhelp = np.zeros((nl))
chelp = np.zeros((nl))
vphelp = np.zeros((nl))
Earn = np.zeros((nty,ns,na,J))


vals = np.zeros((2))
inds = np.zeros((2))

# initial guesses
# ______________________________________________________________________________________________________________________
# FUNCTIONS
# ______________________________________________________________________________________________________________________

# FUNCTION U(c,l)
def U(c,l):
    if c <= 0:
        return umin - penscale*c**2
    elif l < 0:
        return umin - penscale*l**2
    elif l >= 1:
        return umin - penscale*(l-1)**2
    else:
        return (1/(1-sigma))*(((c**gamma)*((1-l)**(1-gamma)))**(1-sigma))

# FUNCTION marginal_utility(c,l)
def marginal_utility(c,l):
    if c > 0:
        return gamma*(c**gamma*(1 - l)**(1 - gamma))**(1 - sigma)/c
    else:
        return 1000000 + abs(c)**2

# FUNCTION TAX

def LabTax(param,thresold,earnlab,earncap):
    if earnlab == 0:
        LabTaxes = -(param*thresold - earncap)
    elif earnlab + earncap <= param*thresold:
        LabTaxes = -(param*thresold - earnlab - earncap)
        MarTax = 0
    elif earnlab + earncap <= thresold:
        LabTaxes = 0
        MarTax = 0
    elif earnlab + earncap <= bracket1:
        LabTaxes = 0.23*min(earnlab - param/17.5,0)
        MarTax = 0.23
    elif earnlab + earncap <= bracket2:
        LabTaxes = 0.23*bracket1 + 0.27*(earnlab - bracket1 - param/17.5)
        MarTax = (0.23*bracket1 + 0.27*(earnlab - bracket1))/earnlab
    elif earnlab + earncap <= bracket3:
        LabTaxes = 0.23*bracket1 + 0.27*bracket2 + 0.38*(earnlab - bracket2 - param/17.5)
        MarTax = (0.23*bracket1 + 0.27*bracket2 + 0.38*(earnlab - bracket2))/earnlab
    elif earnlab + earncap <= bracket4:
        LabTaxes = 0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*(earnlab - bracket3)
        MarTax = (0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*(earnlab - bracket3))/earnlab
    else:
        LabTaxes = 0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*bracket4 + 0.43*(earnlab - bracket4)
        MarTax = (0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*bracket4 + 0.43*(earnlab - bracket4))/earnlab
    Taxes = LabTaxes + earncap * tauk
    return Taxes

def MarTax(param,thresold,earnlab,earncap):
    if earnlab == 0:
        LabTaxes = 0
        MarTax = 0
    elif earnlab + earncap <= param * thresold:
        LabTaxes = -(param * thresold - earnlab - earncap)
        MarTax = 0
    elif earnlab + earncap <= thresold:
        LabTaxes = 0
        MarTax = 0
    elif earnlab + earncap <= bracket1:
        LabTaxes = 0.23*earnlab
        MarTax = 0.23
    elif earnlab + earncap <= bracket2:
        LabTaxes = 0.23*bracket1 + 0.27*(earnlab - bracket1)
        MarTax = (0.23*bracket1 + 0.27*(earnlab - bracket1))/earnlab
    elif earnlab + earncap <= bracket3:
        LabTaxes = 0.23*bracket1 + 0.27*bracket2 + 0.38*(earnlab - bracket2)
        MarTax = (0.23*bracket1 + 0.27*bracket2 + 0.38*(earnlab - bracket2))/earnlab
    elif earnlab + earncap <= bracket4:
        LabTaxes = 0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*(earnlab - bracket3)
        MarTax = (0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*(earnlab - bracket3))/earnlab
    else:
        LabTaxes = 0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*bracket4 + 0.43*(earnlab - bracket4)
        MarTax = (0.23*bracket1 + 0.27*bracket2 + 0.38*bracket3 + 0.41*bracket4 + 0.43*(earnlab - bracket4))/earnlab
    MarginalTax = (MarTax*earnlab + tauk*earncap)/(earnlab + earncap)
    return MarginalTax

# SUBROUTINE basefun(grid_x,npx,x,vals,inds)
# this subroutine returns the values and the indices of the two basis functions that are positive on a given x in the grid_x
def basefun(grid_x, npx,x):
    global vals
    global inds
    global jl,ju,jm
    vals = np.zeros((2))
    inds = np.zeros((2))
    if x == 0:
        vals[1] = 0
        vals[0] = 1
        inds[1] = 1
        inds[0] = 0
    else:
        jl = 1
        ju = npx
        np.argmax(grid_x > x)
        i = int(np.argmax(grid_x >= x))
        vals[1] = (x - grid_x[i - 1])/(grid_x[i] - grid_x[i - 1])
        vals[0] = (grid_x[i] - x)/(grid_x[i] - grid_x[i - 1])
        inds[1] = i
        inds[0] = i - 1
    inds = inds.astype(int)

def solveStationary( A ):
    n = A.shape[0]
    a = np.eye( n ) - A
    a = np.vstack( (a.T, np.ones( n )) )
    b = np.matrix( [0] * n + [ 1 ] ).T
    return np.linalg.lstsq( a, b )[0]