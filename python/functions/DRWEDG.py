import math
import cmath
import numpy as np
import scipy.special as sp

# Calculates wave amplification factor,  phase angle,  and amplified wave
# height for the combined diffraction and reflection of monochromatic
# incident waves (small amplitude wave theory) approaching (from infinitiy)
# a vertical wedge of arbitrary wedge angle

#   INPUT
#   x: x-coordinate [m] (Cartesian coord system)
#   y: y-coordinate [m] (Cartesian coord system)
#   Hi: incident wave height [m]
#   waveA: approach angle of incident wave [deg] (measured counter-clockwise
#          from x-axis)
#   wedgeA: internal angle of wedge [deg] (measured clockwise from x-axis)
#   L: wavelength [m]

#   OUTPUT
#   H: modified wave height at (x, y) [m]
#   phi: modulus of velocity potential at (x, y)
#   beta: phase angle of velocity potential at (x, y) [rad]
#   error: triggers error

def DRWEDG(x, y, Hi, waveA, wedgeA, L):

    error = 0
    twopi = 2.0 * math.pi
    deg2rad = math.pi / 180.0

    r = math.sqrt(x**2 + y**2) #convert to polar coordinates

    if np.isclose(x, 0.0) and np.isclose(y, 0.0):
        theta = 0.0
    else:
        theta = math.atan2(y, x)
        if theta < 0.0:
            theta = twopi + theta

    #check to see if (x, y) is located within the structure
    radwed = wedgeA * deg2rad
    totang = theta + radwed
    if totang > twopi:
        error = 1
        phi = 0
        beta = 0
        H = 0
        return phi, beta, H, error

    #solve for velocity potential function at (r, theta)
    kr = (2.0 * math.pi / L) * r
    nu = (360.0 - wedgeA) / 180.0
    
    J0 = sp.jv(0, kr)

    n = 0
    order = []
    Jnu = []
    order.append((n + 1) / nu)
    Jnu.append(sp.jv(order, kr))
    tolr = 10.0**-8
    count = 0

    while count < 9:
        n = n + 1
        order.append((n + 1) / nu)
        Jnu.append(sp.jv(order[n], kr))
        if Jnu[n] < tolr:
            count = count + 1
        else:
            count = 0

    wa = waveA * deg2rad

    F = []
    for j in range(len(Jnu)):
        F.append((cmath.exp(1j * order[j] * math.pi / 2.0)) *\
            Jnu[j] * math.cos(order[j] * wa) * math.cos(order[j] * theta))
    F = sum(F)
    Fpot = (2.0 / nu) * (J0 + 2.0 * F)

    #determine modulus
    fr = Fpot.real
    fi = Fpot.imag
    phi = math.sqrt(fr**2 + fi**2) #modulus
    if wa < tolr:
        phi = phi / 2.0

    #determine phase angle
    if phi < tolr:
        beta = 0 #phase difference
    else:
        beta = math.atan2(fi, fr)

    H = Hi * phi #modified wave height

    return phi, beta, H, error
