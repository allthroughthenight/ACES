import math
import numpy as np

# Error check for monochromatic wave breaking

#   INPUT
#   T: wave period
#   d: water depth
#   kappa: breaking index
#   struct: =0 for no structure, =1 for structure

#   OUTPUT
#   Hb: breaking wave height

def ERRWAVBRK(T, d, m, kappa, struct):
    if np.isclose(m, 0.0): #where the nearshore slope is flat or unknown
        Hb = kappa*d
    elif struct == 1: #maximum wave height in prescence of a structure
        a = 1.36 * (1.0 - math.exp(-19.0*m))
        b = 1.0 / (0.64*(1.0 + math.exp(-19.5*m)))
        term = (d / T**2)
        P = a + (1.0 + 9.25*m**2*b - 4.0*m*b)/term

        term1 = d / (m*a*(18.5*m - 8.0))
        term2 = P**2 - (((4.0*m*b*a)/term) * (9.25*m - 4.0))
        Hb = term1 * (P - math.sqrt(term2))

    return Hb