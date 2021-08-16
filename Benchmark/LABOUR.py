# THIS SUBROUTINE DEFINES THE STOCHASTIC PROCESS FOR LABOR PRODUCTIVITY
pilab = np.zeros((ns,jr-1))
stdlel = np.zeros((jr-1))
iden = np.zeros((ns,ns))
theta = np.zeros(3)

# ENDOWMENT PROCESS PARAMETER
rho = 0.9394318181818182
sigmaeps = 1.8081632653061224
sigma2alpha = 0.2973579382613107 - np.var(np.log(ephansen[0:jr]))

if ns==1:
    eta = [1]
    pi = np.zeros((ns,ns))
    pi[0,0] = 1
    pini = [1]
    ep = np.empty((nty, J))
    for j in range(J):
        ep[0, j] = np.exp(-np.sqrt(sigma2alpha)) * ephansen[j]
        ep[1, j] = np.exp(np.sqrt(sigma2alpha)) * ephansen[j]
elif ns==3:
    eta = np.array((0.1,0.8,0.1))
    pi = np.array((((0.1,0.8,0.1),(0.1,0.8,0.1),(0.1,0.8,0.1))))
    pini[0] = 0
    pini[1] = 1
    pini[2] = 0
    ep = np.empty((nty, J))
    for j in range(J):
        ep[0, j] = np.exp(-np.sqrt(sigma2alpha)) * ephansen[j]
        ep[1, j] = np.exp(np.sqrt(sigma2alpha)) * ephansen[j]
    eta = np.exp(eta)
    eta = eta/sum(eta/3)
else:
    pilab = np.zeros((ns, jr - 1))
    stdlel = np.zeros((jr - 1))
    iden = np.zeros((ns, ns))

    theta[0] = 0
    theta[1] = rho
    theta[2] = (sigmaeps * (1 - rho ** 2) ** (1 / 2)) ** 2

    bbb = q.approximation.tauchen(theta[1], theta[2], theta[0], 3.5172413793103448, ns)
    bbbb = solveStationary(bbb.P)
    bbbb = bbbb.ravel()
    ttt = bbb.state_values
    ttt = np.exp(ttt)

    eta = ttt / (sum(sum(bbbb.__array__() * ttt)))
    pistat = bbbb
    pi = bbb.P
    # DETERMINE THE INITIAL DISTRIBUTION OF LABOUR PRODUCTIVITY
    # FIXED EFFECTS: sigma^2_alpha = 0.247
    ep = np.empty((nty, J))
    for j in range(J):
        ep[0, j] = np.exp(-np.sqrt(sigma2alpha)) * ephansen[j]
        ep[1, j] = np.exp(np.sqrt(sigma2alpha)) * ephansen[j]
    pini[2] = 1
    # Do Markov Mixing with Identity Matrix to increase persistance
    iden[:, :] = 0
    for s in range(ns):
        iden[s, s] = 1
    stdle = sum(pistat.__array__() * (np.log(eta) - sum(pistat.__array__() * np.log(eta))) ** 2)
    stdleini = sum(pini * (np.log(eta) - sum(pini * np.log(eta))) ** 2)
    # Compute cross-sectional variance of labour productivity over time
    pilab[:, 0] = pini
    for t in range(1, jr - 1):
        for s in range(ns):
            pilab[s, t] = sum(pi[:, s] * pilab[:, t - 1])
    for t in range(jr - 1):
        stdlel[t] = sum(pilab[:, t] * (np.log(eta) - sum(pistat.__array__() * np.log(eta))) ** 2)
    permanent_component = sigma2alpha + np.var(np.log(ephansen[0:jr])) # it is the permanent component of the variance, given by the ability type and the age dependent component
    stdlel = stdlel + permanent_component