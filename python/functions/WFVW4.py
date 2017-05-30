
# Input value 'p' includes hydrostatic pressure
# To define wave pressure 'wp' remove hydrostatic pressue from values of
# 'p' below SWL. Pressure is the same above SWL for both values (0).
# Hydrostatic pressue is waves & hydrostatic pressure minus wave pressure.
# Hydrostatic pressue increases from 0 at SWL to rho*g*d at the bottom.

def WFVW4(N, y, p, ww):

    for i in range(1, n  +  1):
        if y[i] < 0:
            wp[i][1] = p[i] + ww * y[i]
            hp[i][1] = p[i] - wp[i][1]
        else:
            wp[i][1] = p[i]
            hp[i][1] = 0

    return hp, wp
