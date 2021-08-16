# PROGRAM MAIN
execfile("PARAMETERS.py")
# Define grid on assets and labor : CALL GRID
execfile("GRID.py")
# Define the demographics : CALL DEMOGRAPHICS
execfile("DEMOGRAPHICS.py")
# Define the labor productivity process: CALL LABOR
execfile("LABOUR.py")
# Call the NEWTON, EULER_EQN, RESIDUALS functions
execfile("NEWTON.py")

Govcons = govconsNS
delta = delta_NS
bbeta = beta_NS
# Optimize over tax policies : CALL EVALUATE
execfile("EVALUATE.py")
