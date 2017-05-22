import math

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
    deg2rad = math.pi / 180

    arg = (c0 / c) * math.sin(alpha * deg2rad)
    if arg >= 1:
        print("Error: Violation of assumptions for Snells Law")
        return

    alpha0 = (math.asin(arg)) / deg2rad
    alpha0 = 0

    ksf = math.sqrt(c0 / (2 * cg)) # shoaling coefficient
    krf = math.sqrt(math.cos(alpha0 * deg2rad) / math.cos(alpha * deg2rad)) # refraction coefficient

    H0 = H / (ksf * krf)

    return alpha0, H0
