import math

def wavelen(d, T, n, g):
    Leck = (g * (T**2) * 0.5 / math.pi) * math.sqrt(math.tanh(4 * math.pi * math.pi * d / (T * T * g)))

    L1 = Leck

    for i in range(0, n):
        L2 = (g * (T**2) * 0.5 / math.pi) * math.tanh(2 * math.pi * d / L1)
        L1 = L2

    L = L2
    k = 2 * math.pi / L

    # ko = find( d <= 0)
    # L(ko) = 0
    if  d <= 0:
        L = 0

    return L, k

def lwtgen(h, T, g):
    # General deepwater conditions
    c0 = g * T / (2 * math.pi)
    cg0 = 0.5 * c0
    L0 = c0 * T

    # Local wave conditions
    L, k = wavelen(h, T, 50, g)

    reldep = h / L

    c = L / T
    n = 0.5 * (1 + ((2 * k * h) / math.sinh(2 * k * h)))
    cg = n * c

    return c, c0, cg, cg0, k, L, L0, reldep

def lwttws(alpha0,c2,cg2,c0,H0):
    deg2rad = math.pi / 180

    arg = (c / c0) * math.sin(alpha0 * deg2rad)
    alpha = (math.asin(arg)) / deg2rad

    ksf = math.sqrt(c0 / (2 * cg))
    krf = math.sqrt(math.cos(alpha0 * deg2rad) / math.cos(alpha * deg2rad))

    H = H0 * ksf * krf

    return alpha, H, krf, ksf

def lwttwm(cg, h, H, L, reldep, rho, g, k):
    E = (1 / 8) * rho * g * (H^2)
    P = E * cg
    Ur = (H * (L^2)) / (h^3)

    if reldep < 0.5:
        setdown = (k * H^2) / (8 * math.sinh(2 * k * h))
    else:
        setdown = 0

    return E, P, Ur, setdown

def ERRSTP(H, d, L):
    steep = H / L
    k = (2 * math.pi) / L
    maxstp = 0.142 * math.tanh(k * d)

    return steep, maxstp

def errwavbrk1(d, kappa):
    Hb = kappa * d

    return Hb

def ERRWAVBRK2(T, m, ds):
        a = 1.36 * (1 - math.exp( - 19 * m))
        b = 1 / (0.64 * (1 + math.exp( - 19.5 * m)))
        term = (ds / T**2)
        P = a + (1 + 9.25 * m**2 * b - 4 * m * b) / term

        term1 = ds / (m * a * (18.5 * m - 8))
        term2 = P**2 - (((4 * m * b * a) / term) * (9.25 * m - 4))
        Hbs = term1 * (P - math.sqrt(term2))

        return Hbs

def errwavbrk3(Ho, m, Lo):
    a = 1.36 * (1 - math.exp(-19 * m))
    b = 1 / (0.64 * (1 + math.exp(-19.5 * m)))

    Hb = Ho * 0.575 * (m**0.031) * ((Ho / Lo)**(-0.254))
    gamma = b - a * Hb / (T**2)
    db = Hb / gamma

    return Hb, db

###############################################################################
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

def lwtdws(alpha, c, cg, c0, H):
    deg2rad = math.pi / 180

    arg = (c0 / c) * math.sin(alpha * deg2rad)
    if arg<1:
        return "Error: Violation of assumptions for Snells Law"

    alpha0 = (math.asin(arg)) / deg2rad
    alpha0 = 0

    ksf = math.sqrt(c0 / (2 * cg)) # shoaling coefficient
    krf = math.sqrt(math.cos(alpha0 * deg2rad) / math.cos(alpha * deg2rad)) # refraction coefficient

    H0 = H / (ksf * krf)

    return alpha0, H0
###############################################################################

###############################################################################
# Error check for wave steepness

#   INPUT
#   H: wave height
#   d: water depth
#   L: wave length

#   OUTPUT
#   steep: steepness of supplied conditions
#   maxstp: maximum wave steepness

def errstp(H, d, L):
    steep = H / L
    k = (2 * math.pi) / L
    maxstp = 0.142 * math.tanh(k * d)

    return steep, maxstp
###############################################################################

###############################################################################
# Error check for monochromatic wave breaking

#   INPUT
#   T: wave period
#   d: water depth
#   kappa: breaking index
#   struct: =0 for no structure, =1 for structure

#   OUTPUT
#   Hb: breaking wave height

def ERRWAVBRK(T, d, m, kappa, struct):
    if m == 0: #where the nearshore slope is flat or unknown
        Hb = kappa * d
    elif m != 0 and struct == 1: #maximum wave height in prescence of a structure
        a = 1.36 * (1 - math.exp(-19 * m))
        b = 1 / (0.64 * (1 + math.exp(-19.5 * m)))
        term = (d / T**2)
        P = a + (1 + 9.25 * m**2 * b -4 * m * b) / term

        term1 = d / (m * a * (18.5 * m - 8))
        term2 = P**2 - (((4 * m * b * a) / term) * (9.25 * m - 4))
        Hb = term1 * (P - math.sqrt(term2))

    return Hb
###############################################################################
