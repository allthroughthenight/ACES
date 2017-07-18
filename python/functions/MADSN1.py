import cmath

# Determine transmission and reflection coefficients for crib-style
# breakwaters

#   INPUT
#   nors: N/sqrt(S) = 0.45
#   fos: F/S
#   nkol: wavenumber x porosity of reference material x equivalent length

#   OUTPUT
#   Ti: transmission coefficient
#   Ri: reflection coefficeint

#   OTHER:
#   k: complex wave number

def MADSN1(nors, fos, nkol):
    # intermediate values
    eps = complex(nors, 0.0)/cmath.sqrt(complex(1,-fos));
    theta = complex(0.0, 1.0)*complex(nkol, 0.0)/eps;

    c1 = (complex(1.0, 0.0) + eps)**2
    c2 = (complex(1.0, 0.0) - eps)**2
    c3 = complex(1.0, 0.0) - eps**2
    denom = c1*cmath.exp(theta) - c2*cmath.exp(-theta)
 
    # transmission coefficient
    teq = complex(4.0, 0.0)*eps/denom
    Ti = abs(teq)

    #reflection coefficient
    req = (c3*(cmath.exp(theta) - cmath.exp(-theta)))/denom
    Ri = abs(req)

    return Ti, Ri