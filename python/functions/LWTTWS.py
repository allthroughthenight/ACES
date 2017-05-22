import math

# Snell's law applied to determine transitional case

#   INPUT
#   alpha0: deepwater angle of wavecrest
#   c: wave celerity
#   cg: group velocity
#   c0: deepwater wave celerity
#   H0: deepwater wave height

#   OUTPUT
#   alpha: wave crest angle with shoreline
#   H: wave height
#   Kr: refraction coeffieint
#   Ks: shoaling coefficient

def LWTTWS(alpha0, c, cg, c0, H0):

    deg2rad = math.pi / 180

    arg = (c / c0) * math.sin(alpha0 * deg2rad)
    alpha = (math.asin(arg)) / deg2rad

    ksf = math.sqrt(c0 / (2 * cg))
    krf = math.sqrt(math.cos(alpha0 * deg2rad) / math.cos(alpha * deg2rad))

    H = H0 * ksf * krf

    return alpha, H, krf, ksf
