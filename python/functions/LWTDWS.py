import math
import cmath
from helper_objects import ComplexUtil

# Snell's Law applied to determine deepwater values

#   INPUT
#   alpha: wave crest angle with shoreline
#   c: wave celerity
#   cg: group velocity
#   c0: deepwater wave celerity
#   H: wave height

#   OUTPUT
#   alpha0: deepwater angle of wavecrest
#   H0: deepwater wave height

def LWTDWS(alpha, c, cg, c0, H):
    alpha0 = None
    H0 = None
    errorMsg = None
    
    deg2rad = math.pi / 180.0

    arg = (c0 / c) * cmath.sin(alpha * deg2rad)
    if ComplexUtil.greaterThanEqual(arg, 1):
        errorMsg = "Error: Violation of assumptions for Snells Law"
        return alpha0, H0, errorMsg

    alpha0 = (cmath.asin(arg)) / deg2rad

    ksf = cmath.sqrt(c0 / (2 * cg)) # shoaling coefficient
    
    alphaCos = cmath.cos(alpha0 * deg2rad) / cmath.cos(alpha * deg2rad)
    if ComplexUtil.lessThan(alphaCos, 0):
        errorMsg = "Error: Alpha1 data out of range"
        return alpha0, H0, errorMsg
    
    krf = cmath.sqrt(alphaCos) # refraction coefficient

    H0 = H / (ksf * krf)

    return alpha0, H0, errorMsg