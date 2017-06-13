import math

# Transmission coefficient for a vertical breakwater

#   INPUT
#   H: incident wave height
#   free: freeboard
#   bb: crest width of vertical breakwater
#   ds: still water level depth (from base of structure)
#   dl: depth of water between still water level and top of berm

#   OUTPUT
#   Ht: transmitted wave height

def VERTKT(H, free, bb, ds, dl):

    aspect = bb / ds
    ratio = dl / ds
    frerat = free / H

    if aspect < 1:
        alpha = 1.8 + 0.4 * aspect
        beta1 = 0.1 + 0.3 * aspect
    else:
        alpha = 2.2
        beta1 = 0.4

    if (dl / ds) <= 0.3:
        alpha = 2.2
        beta2 = 0.1
    else:
        beta2 = 0.527-0.130 / ratio

    c1 = max(0, 1 - aspect)
    c2 = min(1, aspect)
    beta = c1 * beta1 + c2 * beta2

    if frerat <= -(alpha + beta):
        Kt = 1.0
    elif frerat >= (alpha - beta):
        Kt = 0.0
    else:
       Kt = 0.5 * (1 - math.sin((math.pi / (2 * alpha)) * (frerat + beta)))

    Ht = Kt * H

    return Ht
