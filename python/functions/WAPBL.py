import math

from WAPSI import WAPSI

#Solution of PBL equations for 10 m elevation wind velocity (with known
#geostrophic wind velocity)

#   INPUT
#   vg: geostrophic windspeed
#   delt: air-sea temperature difference
#   f: Coriolis parameter
#   H: horizontal temperature gradient
#   phi: angle between vg and H

#   OUTPUT
#   gpbl: equivalent neutral windspped at 10 m elevation


def WAPBL(vg, delt, f, H, phi):
    phi = phi*(math.pi/180.0)
    z = 1000.0
    diff1 = 100.0
    diff2 = 100.0
    diff3 = 100.0

    if abs(delt) > 15.0:
        delt = 15.0*(abs(delt)/delt)

    k = 0.4
    L = delt

    as0 = 0.8
    bs0 = 3.5
    aml = 7.0 - as0

    ab = k*(H/3.0)*math.cos(phi)
    bb = k*(H/3.0)*math.sin(phi)
    a = as0 + ab
    b = bs0 + bb

    ustar = 0.15*vg/abs(b)

    c1 = 0.1525
    c2 = 0.0144/980
    c3 = -0.00317

    while diff3 > 0.1:
        while diff1 > 0.1:
            z0 = (c1/ustar) + (c2*ustar**2) + c3
            theta = math.asin(b*ustar/(vg*k))
            ustarn = k*vg*math.cos(theta)/(math.log(ustar/(f*z0))-a)
            diff1 = abs(ustarn - ustar)
            ustar = (ustar + ustarn)/2

            if ustar < 0.0:
                ustar = 0.1
                z0 = (c1/ustar) + (c2*ustar**2) + c3
                gpbl = (ustar/k)*math.log(z/z0)
                return gpbl

            if abs(b*ustar) > k*vg:
                ustar = k*vg/abs(b) - 1.0**(-10);
        # end while loop

        ustar = ustarn
        z0 = (c1/ustar) + (c2*ustar**2) + c3

        if abs(delt) < 1.0:
            gpbl = (ustar/k)*math.log(z/z0)
            return gpbl

        while diff2 > 1.0:
            lnzz0 = math.log(1005.0/z0)
            psi = WAPSI((1005.0/L), -7.0)
            Ln = 1.79*(ustar**2/delt)*(lnzz0 - psi)
            diff2 = abs(Ln - L)
            L = Ln
        # end while loop
        
        mu = (k*ustar)/(f*L)
        if mu <= 0.0:
            asf = as0 + aml*(1.0 - math.exp(0.015*mu))
            bsf = bs0 - (bs0 - 0.23)*(1.0 - math.exp(0.03*mu))
        else:
            asf = as0 - 0.96*math.sqrt(mu) + math.log(math.sqrt(mu+1.0))
            bsf = bs0 + 0.7*math.sqrt(mu)

        an = max((asf + ab), -15.0)
        bn = min((bsf + bb), 15.0)

        diff3 = abs(a - an)
        a = an
        b = bn
        if abs(b*ustar) > k*vg:
            ustar = k*vg/abs(b) - 1.0**(-10)
        diff1 = 100.0
        diff2 = 100.0
    # end while loop

    z0 = (c1/ustar) + (c2*ustar**2) + c3
    gpbl = (ustar/k)*math.log(z/z0)

    return gpbl