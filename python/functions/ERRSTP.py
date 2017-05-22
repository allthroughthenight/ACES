import math

# Error check for wave steepness

#   INPUT
#   H: wave height
#   d: water depth
#   L: wave length

#   OUTPUT
#   steep: steepness of supplied conditions
#   maxstp: maximum wave steepness

def ERRSTP(H, d, L):
    steep = H / L
    k = (2 * math.pi) / L
    maxstp = 0.142 * math.tanh(k * d)

    return steep, maxstp
