import math

# def fwtcalc(Hnon,Hoverd,unon, nstep, nofour, d, L, deptyp, celdef )
#     number = 9; % max iteration for each wave height step
#     crit = 0.001; % convergence criterion.  If sum of magnitudes of corrections is < crit, the iteration stops
#     num = 2*nofour+10; % initialize
#     np = 61;
#     assert(num<np,'Error: Too many terms in Fourier series');
#     dpi = 4/atan(1);
#     dhe = Hnon /nstep;
#     dho = Hoverd / nstep;
#
#     for x in nstep
#         Hnon = ns * dhe;
#         Hoverd = ns * dho;
#         if ns<=1  %calculate initial linear solution
#           [ sol, z, cosa, sina ] = FWTSOL( dpi, Hoverd, Hnon, unon, number, num, nofour, deptyp, celdef );
#         else % extrapolate for next wave height
#             for i = 1:num
#                 z(i) = 2*sol(i,2) - sol(i,1);
#             end
#         end
#         for iter = 1:number
#         % Calculate right sides of equations and differentiate numerically to obtain Jacobian matrix:
#             [ rhs1 ] = FWTEQNS( d, L, z, Hoverd, nofour, Hnon, dpi, celdef, unon, cosa, sina );
#             for i = 1: num
#                 h = 0.01*z(i);
#                 if abs(z(i))<crit
#                     h = 10^-5;
#                 end
#                     z(i) = z(i) + h;
#                     [ rhs2 ] = FWTEQNS( d, L, z, Hoverd, nofour, Hnon, dpi, celdef, unon, cosa, sina );
#                     z(i) = z(i) - h;
#                     b(i) = -rhs1(i);
#                     for j = 1:num
#                         a(j,i) = (rhs2(j) - rhs1(j)) / h;
#                     end
#             end
#             % Solve matrix equation and correct variables using LINPACK routines
# % Solve the matrix equation [a(i,j)][correction vector] = [b(i)]
# % dgefa factors a double precision matrix by gaussian elimination.
# %call dgefa(a, np, num, ipvt, info)
#         [ a, ipvt, info ] = zgefa ( a, np, nofour );
#    % *    assert(info~=0, 'ERROR:  Matrix singular')
#         %call dgesl(a, np, num, ipvt, b, 0)
#         % The b(i) are now the corrections to each variable
#         b = dgesl ( a, np, nofour, ipvt, b, 0 );
#         sum = 0;
#         for i = 1:num
#             sum =  sum + abs(b(i));
#             z(i) = z(i) + b(i);
#         end
#         criter = crit;
#         if ns == nstep
#             criter = 0.01*crit;
#         end
#   %*      assert(sum>=criter, 'ERROR: Did not converge after iterations')
#         end
#         if ns == 1:
#             for i in num:
#                 sol(i,2) = z(i)
#         else
#             for i in num:
#                 sol(i,1) = sol(i,2)
#                 sol(i,2) = z(i)
#             end
#         end
#     end
# end


def wavelen(d, T, n, g):
    Leck = (g * (T**2) * 0.5 / math.pi) * math.sqrt(math.tanh(4 * math.pi * math.pi * d / (T * T * g)))

    L1 = Leck

    for i in range(0, n):
        L2 = (g * (T**2) * 0.5 / math.pi) * math.tanh(2 * math.pi * d / L1)
        L1 = L2

    L = L2
    k = 2 * math.pi / L

    # ko = find( d < =  0)
    # L(ko) = 0
    if  d <=  0:
        L = 0

    return L, k

def boverf(x):
    p = 0.3275911
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 = 1.061405429

    x1 = x/math.sqrt(2)
    t = 1/(1+p*x1)
    errf = 1.0 - (a1*t + a2*(t**2.0) + a3*(t**3.0) + a4*(t**4.0)+ a5*(t**5.0)) * math.exp(-(x1)*(x1))

    y = 0.5 + (errf * 0.5)

    return y

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
#   struct:  = 0 for no structure,  = 1 for structure

#   OUTPUT
#   Hb: breaking wave height

def ERRWAVBRK(T, d, m, kappa, struct):
    if m == 0: #where the nearshore slope is flat or unknown
        Hb = kappa * d
    elif m !=  0 and struct ==  1: #maximum wave height in prescence of a structure
        a = 1.36 * (1 - math.exp(-19 * m))
        b = 1 / (0.64 * (1 + math.exp(-19.5 * m)))
        term = (d / T**2)
        P = a + (1 + 9.25 * m**2 * b -4 * m * b) / term

        term1 = d / (m * a * (18.5 * m - 8))
        term2 = P**2 - (((4 * m * b * a) / term) * (9.25 * m - 4))
        Hb = term1 * (P - math.sqrt(term2))

    return Hb
###############################################################################

# Determine runup on a rough slope

#   INPUT
#   H: incident wave height at toe of structure
#   xi: surf parameter
#   a: dimensionless coefficient
#   b: dimensionless coefficient

#   OUTPUT
#   runupr: runup on a rough slope

def RUNUPR(H, xi, a, b):
    runupr = (H * a * xi) / (1 + b * xi)
    return runupr

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

# Transmitted wave height by overtopping of an impermebale structure

#   INPUT
#   bb: structure crest width
#   H: total structure height above sea floor
#   R: wave runup
#   H: incident wave height
#   free: freeboard (difference between height of structure and still water
#   depth at structure)

#   OUTPUT
#   Ht: transmitted wave height

def HTP(bb, hs, R, H, free):

    c = 0.51 - 0.11 * (bb / hs)

    Kt = c * (1 - (free / R))

    if Kt < 0:
        Kt = 0.0

    Ht = Kt * H

    return Ht

# Transmission coefficient for a vertical breakwater

#   INPUT
#   H: incident wave height
#   free: freeboard
#   bb: crest width of vertical breakwater
#   ds: still water level depth (from base of structure)
#   dl: depth of water between still water level and top of berm

#   OUTPUT
#   Ht: transmitted wave height

def VERTKT(H, free, bb, ds, dl):

    aspect = bb / ds
    ratio = dl / ds
    frerat = free / H

    if aspect < 1:
        alpha = 1.8 + 0.4 * aspect
        beta1 = 0.1 + 0.3 * aspect
    else:
        alpha = 2.2
        beta1 = 0.4

    if (dl / ds) <= 0.3:
        alpha = 2.2
        beta2 = 0.1
    else:
        beta2 = 0.527 - 0.130 / ratio

    c1 = max(0, 1 - aspect)
    c2 = min(1, aspect)
    beta = c1 * beta1 + c2 * beta2

    if frerat <= -(alpha + beta):
        Kt = 1.0
    elif frerat >= (alpha - beta):
        Kt = 0.0
    else:
       Kt = 0.5 * (1 - math.sin((math.pi / (2 * alpha)) * (frerat + beta)))

    Ht = Kt * H

    return Ht

# Computes sediment transport rates using deepwater wave conditions
# English units only

#   INPUT
#   Hb: deepwater wave height [ft]
#   alpha: deepwater angle of wave crest [deg]
#   K: dimensionless coefficient
#   rho: density of water [slugs/ft^3]
#   rhos: density of the sediment [slugs/ft^3 - 5.14 in FORTRAN code]

#   OUTPUT
#   Q: sediment transport rate [ft^3/s]

#   OTHER:
#   deg2rad: factor to convert deg to rads
#   Pls: longshore energy flux factor

def DEEP_TRANS(Ho, alpha, K, rho, g, rhos):

    deg2rad = math.pi / 180
    alphar = int(alpha) * int(deg2rad)

    Pls = 0.04031 * rho * (g**(3 / 2)) * (int(Ho)**(5 / 2)) * (math.cos(alphar)**(1 / 4)) * math.sin(2 * alphar)

    Q = (Pls * K) / ((rhos - rho) * g * 0.6)

    return Q

# Computes sediment transport rates using breaking wave conditions
# English units only

#   INPUT
#   Hb: breaking wave height [ft]
#   alpha: wave crest angle with the shoreline [deg]
#   K: dimensionless coefficient
#   rho: density of water [slugs/ft^3]
#   rhos: density of the sediment [slugs/ft^3 - 5.14 in FORTRAN code]

#   OUTPUT
#   Q: sediment transport rate [ft^3/s]

#   OTHER:
#   deg2rad: factor to convert deg to rads
#   Pls: longshore energy flux factor

def BREAK_TRANS(Hb, alpha, K, rho, g, rhos):

    deg2rad = math.pi / 180
    alphar = int(alpha) * int(deg2rad)

    Pls = 0.07071 * rho * (g**(3 / 2)) * (int(Hb)**(5 / 2)) * math.sin(2 * alphar)

    Q = (Pls * K) / ((rhos-rho) * g * 0.6)

    return Q
