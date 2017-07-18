import math

def TIDELV(ng, t, ampl, alpha, fndcst, acst):
    deg2rad = math.pi/180.0
    tidelv = 0.0

    for nc in range(len(ampl)):
        arg = (acst[nc]*t + alpha[nc][ng - 1])*deg2rad
        tidelv = tidelv + fndcst[nc]*ampl[nc]*math.cos(arg)

    return tidelv
