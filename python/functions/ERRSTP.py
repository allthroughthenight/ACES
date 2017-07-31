import math
import cmath
import numpy as np

# Error check for wave steepness

#   INPUT
#   H: wave height
#   d: water depth
#   L: wave length

#   OUTPUT
#   steep: steepness of supplied conditions
#   maxstp: maximum wave steepness

def ERRSTP(H, d, L):
    if np.isclose(L, 0.0):
        steep = float('inf')
        k = float('inf')
    else:
        steep = H / L
        k = (2.0 * math.pi) / L
    maxstp = 0.142 * cmath.tanh(k * d)

    return steep, maxstp
