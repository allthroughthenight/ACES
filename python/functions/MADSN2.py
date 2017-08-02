import math
import cmath
import scipy.integrate as integrate
import scipy.special as sp

from helper_objects import ComplexUtil

# Solves for reflection coefficient, non-dimensional runup amplitude, and
# friction slope for rough impermeable slopes

#   INPUT
#   lsub: water depth x cotangent of structure slope
#   phi: friction angle [rads]
#   ko: wavenumber

#   OUTPUT
#   R: reflection coefficient
#   Ru: nondimensional runup amplitude
#   sfc: friction slope constant

def MADSN2(lsub, phi, k):
    L = (2.0*math.pi)/k
    lsol = lsub/L

    fb = math.tan(2.0*phi)
    c1 = 2.0*k*lsub
    c2 = cmath.sqrt(complex(1.0, -fb))

    arg = complex(c1, 0.0)*c2

    J0 = sp.jv(0.0, arg)
    J1 = sp.jv(1.0, arg)

    c3 = (complex(0.0, 1.0)/c2)*J1

    denom = J0 + c3

    psi = complex(c1/2.0, 0.0)*c2

    req = ((J0 - c3)/denom)*cmath.exp(complex(0.0, c1))
    R = abs(req)

    rueq = cmath.exp(complex(0.0, c1/2.0))/denom
    Ru = abs(rueq)

    if ComplexUtil.lessThan(lsol, 0.05):
        fsc = 0.84242
    else:
        topint, err = integrate.quad(integrandTop, 0.0, 1.0, args=(psi))
        botint, err = integrate.quad(integrandBottom, 0.0, 1.0, args=(psi))

        fsc = (4.0/(3.0*math.pi))*(topint/botint)

    return R, Ru, fsc


def integrandTop(y, psi):
    return abs((sp.jv(1.0, 2.0*psi*cmath.sqrt(y))/(psi*cmath.sqrt(y)))**3)

def integrandBottom(y, psi):
    return abs(y*(sp.jv(1.0, 2.0*psi*cmath.sqrt(y))/(psi*cmath.sqrt(y)))**2)