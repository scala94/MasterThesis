# THIS SUBROUTINE BUILDS GRIDS FOR LABOR EFFICIENCY UNITS, SURVIVAL RATES AND AGE-DISTRIBUTION
# AGE EFFICIENCY UNITS FROM HANSEN (1993)

# def fun1(x):
#     return 1.13 - (0.020545474634160316*x -0.9450918331713745)**2

ephansen = np.array(((0.9438466111771701, 0.96115338882283, 0.977615933412604, 0.9932342449464923, 1.0080083234244945,
                      1.0219381688466112, 1.0350237812128418, 1.0472651605231866, 1.0586623067776457, 1.0692152199762188,
                      1.078923900118906, 1.0877883472057075, 1.095808561236623, 1.1029845422116527, 1.1093162901307965,
                      1.1148038049940545, 1.1194470868014268, 1.123246135552913, 1.1262009512485136, 1.1283115338882281,
                      1.129577883472057, 1.13, 1.129577883472057, 1.1283115338882281, 1.1262009512485136, 1.123246135552913,
                      1.1194470868014268, 1.1148038049940545, 1.1093162901307965, 1.102984542211652, 1.0958085612366228,
                      1.0877883472057073, 1.078923900118906, 1.0692152199762186, 1.0586623067776455, 1.0472651605231866,
                      1.0350237812128418, 1.0219381688466112, 1.0080083234244945, 0.9932342449464922, 0.977615933412604,
                      0.9611533888228299, 0.94384661117717, 0.925695600475624, 0.9067003567181925, 0.8868608799048752,
                      0.8661771700356716, 0.8446492271105825, 0.8222770511296076, 0.7990606420927466, 0.7749999999999999)))

ephansen = ephansen/0.9438466111771701
ephansen[jr:len(ephansen)] = 0

while len(ephansen) < J:
    ephansen = np.append(ephansen, 0)
ephansen = np.round(ephansen,decimals = 8)

measty = np.zeros((nty))
measty[:] = 1/nty

# POPULATION NUMBERS FROM BELL AND MILLER (2002)
SurvProb = np.array(([0.99904782, 0.99905201, 0.99903581,0.99899913, 0.99895212, 0.99888451, 0.99882691, 0.99875373,
                      0.99868028, 0.99860655, 0.99852223,0.99842722, 0.99832145, 0.99819446, 0.99806162, 0.99791246,
                      0.99774677, 0.99757479, 0.99740159,0.9972166 , 0.99700383, 0.99676812, 0.99651962, 0.99626862,
                      0.9959776 , 0.9956618 , 0.99529906,0.99489901, 0.99444966, 0.99394948, 0.9933857 , 0.99275595,
                      0.99205744, 0.99130937, 0.99049177,0.9902129 , 0.98993402, 0.98965515, 0.98937627, 0.9890974 ,
                      0.98881852, 0.98853965, 0.98826077,0.9879819 , 0.98770302, 0.98742415, 0.98714527, 0.9868664 ,
                      0.98658752, 0.98630865, 0.98602977,0.98575090, 0.98547202, 0.98519315, 0.98491427, 0.98403540,
                      0.98107258, 0.97806348, 0.97343528,0.96814236, 0.95807708, 0.94818626, 0.93837765, 0.92762881,
                      0.91095017, 0.89828875, 0.88068644,0.86010839, 0.84162041, 0.81782224, 0.79360599, 0.76504265,
                      0.74543674, 0.72273525, 0.70126761,0.00]))

# NUMBER OF AGENTS IN POPULATION
Nu = np.zeros((J))
Nu[0] = 1
for i in range(1,J):
    Nu[i] = SurvProb[i-1]*Nu[i-1]/(1+nn)

# FRACTION OF AGENTS IN THE POPULATION
mu = np.zeros((J))
for i in range(J):
    mu[i] = Nu[i]/sum(Nu)

# TO UNDERSTAND LAST PART
# CHECKED UNTIL HERE

topop = sum(Nu)