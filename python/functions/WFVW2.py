import math
import cmath

def WFVW2(N, d, L, H, x, ww, method):
    dd = d / N
    yo = 0.0
    k = 2 * math.pi / L

    yc = [0.0 for i in range(N + 1)]
    yt = [0.0 for i in range(N + 1)]
    pc = [0.0 for i in range(N + 1)]
    pt = [0.0 for i in range(N + 1)]
    mc = [0.0 for i in range(N + 1)]
    mt = [0.0 for i in range(N + 1)]

    #Miche-Rundgren Method
    cosh1 = cmath.cosh(k * d)
    sinh1 = cmath.sinh(k * d)
    tanh1 = cmath.tanh(k * d)

    theta1 = 1.0 + 3.0 / (4.0 * sinh1**2) - 1.0 / (4.0 * cosh1**2)
    theta2 = 3.0 / (4.0 * sinh1**2) + 1.0 / (4.0 * cosh1**2)

    for i in range(N + 1):
        cosh2 = cmath.cosh(k * (d + yo))
        cosh3 = cmath.cosh(k * (2 * d + yo))
        cosh4 = cmath.cosh(k * yo)
        sinh2 = cmath.sinh(k * (d + yo))
        sinh3 = cmath.sinh(k * (2 * d + yo))
        sinh4 = cmath.sinh(k * yo)
#        F4  =  sinh4 / sinh1 / cosh1
#        F3  =  sinh4 / sinh1 / sinh1
#        F7  =  (1 - 1 / (4 * cosh1 * cosh1)) * cosh3 - 2 * tanh1 * sinh3 + 75 * (cosh4 / (sinh1 * sinh1) - 2 * cosh2 / cosh1)
#        F8  =  cosh3 / (4 * cosh1 * cosh1) - 2 * tanh1 * sinh3 + 75 * (cosh4 / (sinh1 * sinh1) - 2 * cosh2 / cosh1)
        j = N - i

        #Sea surface elevation when crest and trough at wall (y0 = 0)
        #Miche-Rundgren valid for both methods
        if i == 0:
            ycb = yo + (H / 2) * (1 + x) * (sinh2 / sinh1) + (math.pi * H / 4) * (H / L) * (sinh2 / sinh1) * (cosh2 / sinh1) * ((1 + x)**2 * theta1 + (1 - x)**2 * theta2)
            ytb = yo - (H / 2) * (1 + x) * (sinh2 / sinh1) + (math.pi * H / 4) * (H / L) * (sinh2 / sinh1) * (cosh2 / sinh1) * ((1 + x)**2 * theta1 + (1 - x)**2 * theta2)

        if method == 0: #Miche-Rundgren (method = 0)
            yc[j] = yo + (H / 2) * (1 + x) * (sinh2 / sinh1) + (math.pi * H / 4) * (H / L) * (sinh2 / sinh1) * (cosh2 / sinh1) * ((1 + x)**2 * theta1 + (1 - x)**2 * theta2)
            yt[j] = yo - (H / 2) * (1 + x) * (sinh2 / sinh1) + (math.pi * H / 4) * (H / L) * (sinh2 / sinh1) * (cosh2 / sinh1) * ((1 + x)**2 * theta1 + (1 - x)**2 * theta2)

            theta3 = (1 - 1 / (4 * cosh1**2)) * cosh3 - 2 * tanh1 * sinh3 + (3 / 4) * (cosh4 / sinh1**2 - 2 * cosh2 / cosh1)
            theta4 = cosh3 / (4 * cosh1**2) - 2 * tanh1 * sinh3 + (3 / 4) * (cosh4 / (sinh1**2) - 2 * cosh2 / cosh1)

            pcr = -yo - (H / 2) * (1 + x) * sinh4 / (sinh1 * cosh1) - (math.pi * H / 4) * (H / L) * (sinh4 / sinh1**2) * ((1 + x)**2 * theta3 + (1 - x)**2 * theta4)
            pc[j] = ww * pcr

            ptr = -yo + (H / 2) * (1 + x) * sinh4 / (sinh1 * cosh1) - (math.pi * H / 4) * (H / L) * (sinh4 / sinh1**2) * ((1 + x)**2 * theta3 + (1 - x)**2 * theta4)
            pt[j] = ww * ptr
        else: #Sainflou (method = 1)
            yc[j] = yo + H * (sinh2 / sinh1) + math.pi * H * (H / L) * (sinh2 / sinh1) * (cosh2 / sinh1) #vertical elevation when crest at wall
            yt[j] = yo - H * (sinh2 / sinh1) + math.pi * H * (H / L) * (sinh2 / sinh1) * (cosh2 / sinh1) #vertical elevation when trough at wall

            pcr = -yo - H * (sinh4 / (sinh1 * cosh1)) #pressure when crest at wall
            pc[j] = pcr * ww

            ptr = -yo + H * (sinh4 / (sinh1 * cosh1)) #pressure when trough at wall
            pt[j] = ptr * ww

        mc[j] = pc[j] * (yc[j] + d) #incremental moment for cresh
        mt[j] = pt[j] * (yt[j] + d) #incremental moment for trough

        yo = yo - dd

    yc[N] = ycb
    yt[N] = ytb

    return yc, yt, pc, pt, mc, mt