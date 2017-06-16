import math
from GODA5 import GODA5

# Subroutine to find the shoaling coefficient based on the methof of Shuto

def GODA3(Ts, Hdeep, d, g, Csave, itest):
    # temporary rename for del
    del1 = 100

    Lo = (g / (2 * math.pi)) * Ts**2
    dLo = d  /  Lo
    dL = GODA5(dLo)
    n = 0.5 * (1 + 4 * math.pi * dL / math.sinh(4 * math.pi * dL))
    L = d / dL
    C = L / Ts
    Co = (g / (2 * math.pi)) * Ts
    Ks = math.sqrt(0.5 / n * Co / C)
    H = Hdeep * Ks
    F = 980 * H * Ts**2 / (d**2)

    if itest == 1:
        Ks = Csave / (d**(2 / 7) * H)
        H = Hdeep * Ks
        F = 980 * H * Ts**2 / (d**2)
        if F < 50:
            itest = 1
            return Ks, Csave, itest
        else:
            itest = 2
            Csave = H * d**(5 / 2) * (math.sqrt(980 * H * Ts**2 / (d**2)) - 2 * (math.sqrt(3)))
            return Ks, Csave, itest
    elif itest == 2:
        while del1 > 0.05:
            Hn = Csave / (d**(5 / 2) * (math.sqrt(980 * H * Ts**2 / (d**2))-2 * math.sqrt(3)))
            del1 = abs((Hn - H) / Hn)
            if del1 < 0.05:
                break
            H = Hn
        Ks = Hn / Hdeep
    elif itest == 0:
        if F < 30:
            itest = 0
            return Ks, Csave, itest
        else:
            itest = 1
            Csave = H * d**(2 / 7)
            return Ks, Csave, itest

    return Ks, Csave, itest
