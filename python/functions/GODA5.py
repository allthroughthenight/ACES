import math

def GODA5(dLo):

    diff = 100
    Ld = 1.0 / dLo
    Lod = Ld

    while diff > 0.0005:
        arg = 2.0 * math.pi / Ld
        Ldnew = Lod * math.tanh(arg)
        diff = abs(Ldnew - Ld)
        Ld = (Ldnew + Ld) / 2.0
        
    dL = 1.0 / Ldnew

    return dL
