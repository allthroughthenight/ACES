import math
import cmath
import numpy as np

#
# function wavelength(d,T,n,g);
#
# n = # of iterations
#
# d = depth, this can be an array
# T = period
# n = number of iterations
# g = 32.2lb/ft^2 or 9.81N/m^2

def WAVELEN(d, T, n, g):
    Leck = (g * (T**2) * 0.5 / math.pi) * cmath.sqrt(math.tanh(4.0 * math.pi * math.pi * d / (T * T * g))) # 1984 SPM, p.2-7

    L1 = Leck

    for i in range(n):
        if np.isclose(L1, 0.0):
            L2 = (g * (T**2) * 0.5 / math.pi)
        else:
            L2 = (g * (T**2) * 0.5 / math.pi) * cmath.tanh(2.0 * math.pi * d / L1)
        L1 = L2 # redo

    L = L2
    if np.isclose(L, 0.0):
        k = float('inf')
    else:
        k = 2.0 * math.pi / L

    # if isinstance(d, list):
    #     ko = [index for index, value in enumerate(d) if value <= 0.0]
    #     for index in ko:
    #         L[index] = 0.0
    # else:
    #     if d <= 0.0:
    #         L[0] = 0.0;
    if d <= 0.0:
        L = 0.0

    return L, k
