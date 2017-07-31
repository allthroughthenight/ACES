import math
import cmath
from WAVELEN import WAVELEN

# Linear wave theory approximations

#   INPUT
#   h: still water depth at waveform
#   T: wave period
#   g: gravitational acceleration

#   OUTPUT
#   c: wave celerity
#   c0: deepwater wave celerity
#   cg: group velocity
#   cg0: deepwater group velocity
#   k: wavenumber
#   L: wave length
#   L0: deepwater wave length
#   reldep: relative depth

def LWTGEN(h, T, g):

    # General deepwater conditions
    c0 = g * T / (2 * math.pi)
    cg0 = 0.5 * c0
    L0 = c0 * T

    # Local wave conditions
    L, k = WAVELEN(h, T, 50, g)

    reldep = h / L

    c = L / T
    n = 0.5 * (1 + ((2 * k * h) / cmath.sinh(2 * k * h)))
    cg = n * c

    return c, c0, cg, cg0, k, L, L0, reldep
