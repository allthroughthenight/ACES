from helper_objects import ComplexUtil

# Input value 'p' includes hydrostatic pressure
# To define wave pressure 'wp' remove hydrostatic pressue from values of
# 'p' below SWL. Pressure is the same above SWL for both values (0).
# Hydrostatic pressue is waves & hydrostatic pressure minus wave pressure.
# Hydrostatic pressue increases from 0 at SWL to rho*g*d at the bottom.

def WFVW4(N, y, p, ww):
    wp = [0.0 for i in range(N + 1)]
    hp = [0.0 for i in range(N + 1)]
    
    for i in range(N + 1):
        if y[i].real < 0.0:
            wp[i] = p[i] + ww * y[i].real
            hp[i] = p[i] - wp[i]
        else:
            wp[i] = p[i]
            hp[i] = 0.0
    
    return hp, wp