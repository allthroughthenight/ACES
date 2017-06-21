import math
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
    Leck = (g * (T**2) * 0.5 / math.pi) * math.sqrt(math.tanh(4 * math.pi * math.pi * d / (T * T * g))) # 1984 SPM, p.2-7

    L1 = Leck

    for i in range(1, n):
        L2 = (g * (T**2) * 0.5 / math.pi) * math.tanh(2 * math.pi * d / L1)
        L1 = L2

    L = L2
    k = 2 * math.pi / L

    if isinstance(d, list):
        ko = [index for index, value in enumerate(d) if value <= 0]
        for index in ko:
            L[index] = 0
    else:
        if d <= 0:
            L[0] = 0;

    return L, k
