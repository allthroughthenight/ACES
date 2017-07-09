import math
from GODA5 import GODA5


# Subroutine calculates the effective refraction coefficeint Kreff based
# on Goda's method for random wave refraction analysis. The frequencies to
# be analyzed are calculated based on an assumed Bretschnieder-Mitsuyasu
# spectrum. The refraction coefficient of each frequency and direction
# component (based on Snell's Law) are then weight according to the Goda's
# method to yield Kreff.

def GODA4(direc, Ts, d, Hdeep, g):
    deg2rad = math.pi / 180.0
    M = 10
    diff = 100.0
    sumsq = 0.0
    sumkr = 0.0
    d10 = [0.05, 0.11, 0.21, 0.26, 0.21, 0.11, 0.05]
    d25 = [0.02, 0.06, 0.23, 0.38, 0.23, 0.06, 0.02]
    d75 = [0.00, 0.02, 0.18, 0.60, 0.18, 0.02, 0.00]
    theta = [0.0 for i in range(8)]
    Cr = []
    kr = []
    [kr.append([]) for i in range(7)]
    sumsqkr = []

    for i in range(7):
        direcr = direc * deg2rad

        for j in range(10):
            if j == 0:
                if direcr > 0:
                    theta[0] = (direcr - (67.5 * deg2rad))
                else:
                    theta[0] = -(abs(direcr) + (67.5 * deg2rad))

            F = (1.007 / Ts) * (math.log(2.0 * M / (2.0 * (j + 1) - 1))**(-0.25))
            omg = 2.0 * math.pi * F
            T = 2.0 * math.pi / omg
            Lo = (g / (2.0 * math.pi)) * T**2
            Co = Lo / T
            dLo = d / Lo
            dL = GODA5(dLo)
            L = d / dL
            Cr.append(L / T)
            th = theta[i]
            argu = (Cr[j] / Co) * math.sin(th)
            if abs(argu) > 1.00:
                argu = 0.9999999
            theta2 = math.asin(argu)
            if th >= (math.pi / 2.0):
                theta2 = math.pi-theta2
            elif th <= (-math.pi / 2.0):
                theta2 = -(math.pi - theta2)
            argm = math.cos(th) / math.cos(theta2)
            kr[i].append(math.sqrt(abs(argm)))
            sumsq = sumsq + kr[i][j]**2
        # end for loop

        sumsqkr.append(sumsq)
        sumsq = 0.0
        theta[i + 1] = theta[i] + (22.5 * deg2rad)
    # end for loop

    Kreff2 = 1.0
    N = 0

    while diff > 0.005 and N <= 20:
        Los = (g / (2.0 * math.pi)) * Ts**2
        dLos = d / Los
        dLs = GODA5(dLos)
        H = Kreff2 * Hdeep
        L = d / dLs
        HL = H / L

        if Ts <= 10.0:
            for i in range(7):
                sumkr = sumkr + (d10[i] / 10.0) * sumsqkr[i]
        elif Ts > 10.0 and HL > 0.02:
            for i in range(7):
                sumkr = sumkr + (d25[i] / 10.0) * sumsqkr[i]
        else:
            for i in range(7):
                sumkr = sumkr + (d75[i] / 10.0) * sumsqkr[i]

        Kreff = math.sqrt(sumkr)
        sumkr = 0.0
        diff = abs(Kreff2 - Kreff) / Kreff2
        Kreff2 = Kreff

        N = N + 1

    return Kreff
