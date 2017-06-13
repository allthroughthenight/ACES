import math

# Determine runup on a smooth simple slope

#   INPUT
#   H: incident wave height at toe of structure
#   L: wave length
#   ds: water depth at structure
#   theta: structure slope
#   xi: surf parameter

#   OUTPUT
#   runups: runup on a smooth slope

def RUNUPS(H, L, d, theta, xi):

    Cp = 1.002 * xi
    nonlin = (H / L) / (math.tanh(2 * math.pi * d / L)**3)
    Cnb = 1.087 * math.sqrt(math.pi / (2 * theta)) + 0.775 * nonlin

    if xi <= 2:
        C = Cp
    elif xi >= 3.5:
        C = Cnb
    else:
        C = ((3.5 - xi) / 1.5) * Cp + ((xi - 2) / 1.5) * Cnb

    runups = C * H

    return runups
