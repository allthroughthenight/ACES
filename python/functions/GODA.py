import math
import numpy as np
from GODA2 import GODA2
from GODA3 import GODA3
from GODA4 import GODA4
from GODA5 import GODA5

# Input required in centimeters

def GODA(Ho, dloc, Ts, S, direc, g):
    Ksout = [0.0, 0.0]
    Krout = 0.0
    Hmaxout = [0.0, 0.0]
    Hrmsout = [0.0, 0.0]
    Hmeanout = [0.0, 0.0]
    Hsigout = [0.0, 0.0]
    H10out = [0.0, 0.0]
    H02out = [0.0, 0.0]
    dLout = [0.0, 0.0]
    SBout = [0.0, 0.0]
    dLoout = [0.0, 0.0]
    dHoout = [0.0, 0.0]
    theta2dout = [0.0, 0.0]
    etaout = [0.0, 0.0]

    # Ht1 = [0.0 for loopIndex in range(int(is1)*150)]
    # Ht2 = [0.0 for loopIndex in range(int(is1)*150)]
    # cdf = [0.0 for loopIndex in range(int(is1)*150)]
    # cdf2 = [0.0 for loopIndex in range(int(is1)*150)]
    Ht1 = []
    Ht2 = []
    cdf = []
    cdf2 = []

    deg2rad = math.pi / 180
    Csave = 0
    itest = 0
    ym1 = 1
    ym2 = 0
    etam1 = 0
    etam2 = 0
    zm1 = 0
    jpn = 0
    #
    # Hx1 = 1
    # cdf1 = 1
    # Hx2 = 1
    # cdf2 = 1

    sbn = [3.2831, 2.3158, 1.3832, 0.4599, -0.4599, -1.3832, -2.3158, -3.2831]
    delp = [0.0014, 0.0214, 0.1359, 0.3413, 0.3413, 0.1359, 0.0214, 0.0014]

    # Calcuate deepwater wavelength
    Lo = (g / (2 * math.pi)) * Ts**2
    xsave = Lo
    if (20 * Ho) > Lo:
        xsave = 20 * Ho
    d = xsave

    # Calculate deepwater wave steepness
    HoLo = Ho / Lo

    # Find effective slope of beach (i.e.,  beach slope in the approach
    # direction of propagation) for deepwater. This effective slope will change
    # as the principal approach direction chenged due to Snell's Law
    # refraction.
    direcr = direc * deg2rad
    Seff = S / math.cos(direcr)

    # Main computational portion of program. Calculations proceed as follows:
    #   -Still water depth in deepwater divided into 100 increments.
    #   -First depth increment acted upon.
    #   -A first estimate for setup is linearly extrapolated from the setup
    #       gradient from the previous step. This gradient is zero in
    #       deepwater.
    #   -In deepwater where d / Lo > 0.5,  the calculation goes back to the first
    #       step for the next depth increment. Once d / Lo  = < 0.5,  the remainder
    #       of the calculations performed where the increment is reduced to
    #       1 / 500th of the original still water depth.
    #   -The effective refraction coefficient from subroutine GODA4 is
    #       calculated.
    #   -Probabilites at eight levels of surf beat are calculated. For each
    #       level of surf beat,  the still water depth,  the first setup
    #       estimated,  and surf beat are added together.
    #   -Wave characterisitcs are computed with the first estimate of setup. A
    #       new value of setup is calculated directly from the radiation stress
    #       equation.
    #   -Program then checks to see if the 2nd value of setup is approximately
    #       equal to the first estimated. If not,  the program recalculates the
    #       surf beat level probabilities at the new value of setup,  and redoes
    #       the calculation of setup from the radiation stress equation. If so,
    #       the program calculates the total probabilities of wave height
    #       occurrence. It will output the results if the water depth at a
    #       point is approximately the same as a water depth of interest.
    #
    #   This is the beginning of the depth "loop" (i.e.,  beginning of the depth
    #   incrementation along profile).

    N = 0
    M = 0
    while d > dloc:
        if M == 1:
            deld = xsave / 100.0
        elif M == 2:
            deld = xsave / 500.0

        if N == 0:
            d = xsave
        else:
            d = d - deld

        y = Seff * (xsave - d)

        #Find still water depth at location y
        dswl = d
        dHo = dswl / Ho

        N = N + 1

        diffy = ym1 - ym2
        if np.isclose(diffy, 0.0):
            diffy = 0.125
            deld = diffy / Seff

        eta = etam1 + (y - ym1) * (etam1 - etam2) / diffy
        dLo = d / Lo
        Cso = Lo / Ts

        dL = GODA5(dLo)

        #Final coefficient of shoaling by method of Shuto
        Ks, Csave, itest = GODA3(Ts, Ho, d, g, Csave, itest)

        if (d / Lo) > 0.5 and N != 1 and d > (dloc + 30):
            ym1 = y
            M = 1
            L = d / dL
            Cs = L / Ts
            argum = Cs / Cso * math.sin(direcr)
            theta2 = math.asin(argum)
            Seff = S / math.cos(theta2)
        else:
            diff2 = 100.0
            Hop = Ho
            M = 2
            d = dswl + eta
            while diff2 >= 0.07:
                Kreff = GODA4(direc, Ts, d, Ho, g)
                sbrms = 0.01 * Hop / math.sqrt(Hop / Lo * (1.0 + d / Hop))
                A2 = (1.416 / Ks)**2
                p = [0.0 for loopIndex in range(150)]
                di = [0.0 for loopIndex in range(8)]
                x1 = [0.0 for loopIndex in range(8)]
                x2 = [0.0 for loopIndex in range(8)]
                q = [0.0 for loopIndex in range(150)]

                for j in range(8):
                    di[j] = sbrms * sbn[j] + dswl + eta
                    arg =  - 1.5 * math.pi * di[j] / Lo * (1.0 + 15.0 * ((1 / Seff)**(4.0 / 3.0)))
                    arg = min(arg, 100.0)
                    arg = max(arg, - 100.0)

                    x1[j] = 0.18 * (Lo / Hop) * (1.0 - math.exp(arg)) * Kreff
                    x1[j] = min(x1[j], 2.8)

                    if x1[j] > 0.0:
                        x = 0.0
                        x2[j] = (2.0 / 3.0) * x1[j]
                        delxx = (x1[0] / 150.0)
                        arg2 =  - A2 * (x1[j]**2)
                        arg2 = min(arg2, 100.0)
                        arg2 = max(arg2, - 100.0)

                        for i in range (150):
                            x = x + delxx
                            arg =  - A2 * (x**2)
                            arg = max(arg, - 100.0)
                            arg = min(arg, 100.0)

                            if x > x1[j]:
                                q[i] = 0.0
                            elif x <= x2[j]:
                                q[i] = 2.0 * A2 * x * math.exp(arg)
                            else:
                                q[i] = 2.0 * A2 * x * math.exp(arg) - (x - x2[j]) / (x1[j] - x2[j]) * 2.0 * A2 * x1[j] * math.exp(arg2)
                        sumq = sum(q)

                        fact = delp[j] / sumq
                        for i in range(150):
                            p[i] = p[i] + q[i] * fact
                sump = sum(p)

                Hmax, Hrms, Hmean, Hsig, H10, H02, etan, z = GODA2(p, delxx, Ho, sump, dL, etam1, d, zm1)

                diff2 = abs((etan - eta) / etan)
                if diff2 > 0.07:
                    eta = etan

            dL = GODA5(dLo)
            L = d / dL
            Cs = L / Ts
            argum = Cs / Cso * math.sin(direcr)
            theta2 = math.asin(argum)
            theta2d = theta2 / deg2rad
            Seff = S / math.cos(theta2)

            if N == 1:
                Ksout[0] = Ks
                Hmaxout[0] = Hmax
                Hrmsout[0] = Hrms
                Hmeanout[0] = Hmean
                Hsigout[0] = Hsig
                H10out[0] = H10
                H02out[0] = H02
                dLout[0] = dL
                SBout[0] = sbrms
                dLoout[0] = dLo
                dHoout[0] = dHo
                theta2dout[0] = theta2d
                etaout[0] = eta
            else:
                Ksout[1] = Ks
                Krout = Kreff
                Hmaxout[1] = Hmax
                Hrmsout[1] = Hrms
                Hmeanout[1] = Hmean
                Hsigout[1] = Hsig
                H10out[1] = H10
                H02out[1] = H02
                dLout[1] = dL
                SBout[1] = sbrms
                dLoout[1] = dLo
                dHoout[1] = dHo
                theta2dout[1] = theta2d
                etaout[1] = eta

            x = 0.0
            if Hsig < 20.0:
                delh = 1.0
            elif Hsig < 50.0:
                delh = 2.0
            else:
                delh = 10.0

            ijk = 0
            ikj = 0
            H1 = 0
            cump1 = 0
            if N <= 1:
                Kreff = 1.0
            jpn = jpn + 1

            for i in range(150):
                x = x + delxx
                H2 = x * Hop
                cump2 = cump1 + p[i] / sump
                if cump2 > 0.9999:
                    cump1 = cump2
                    H1 = H2
                else:
                    i1 = H1 / delh
                    i2 = H2 / delh

                    # renamed is to is1
                    is1 = i2 - i1
                    if is1 == 0:
                        cump1 = cump2
                        H1 = H2
                    elif is1 > 0:
                        if is1 < 1:
                            is1 = 1

                        for it in range(int(is1)):
                            Ht = delh * (i1 + it)

                            if np.isclose(H1, H2):
                                cump = float('inf')
                            else:
                                cump = cump1 + (Ht - H1) / (H2 - H1) * (cump2 - cump1)

                            if cump > 0.999:
                                cump1 = cump2
                                H1 = H2
                            else:
                                if jpn == 1:
                                    if len(Ht1) < ijk + 1:
                                        for loopIndex in range(len(Ht1), ijk + 1):
                                            Ht1.append(0.0)
                                    Ht1[ijk] = Ht

                                    if len(cdf) < ijk + 1:
                                        for loopIndex in range(len(cdf), ijk + 1):
                                            cdf.append(0.0)
                                    cdf[ijk] = cump

                                    ijk = ijk + 1
                                else:
                                    if len(Ht2) < ikj + 1:
                                        for loopIndex in range(len(Ht2), ikj + 1):
                                            Ht2.append(0.0)
                                    Ht2[ikj] = Ht

                                    if len(cdf2) < ikj + 1:
                                        for loopIndex in range(len(cdf2), ikj + 1):
                                            cdf2.append(0.0)
                                    cdf2[ikj] = cump

                                    ikj = ikj + 1
                        cump1 = cump2
                        H1 = H2
            zm1 = z
            etam2 = etam1
            etam1 = etan
            ym2 = ym1
            ym1 = y
        # end if

    Ht1 = Ht1[1:]
    Ht2 = Ht2[1:]
    cdf = cdf[1:]
    cdf2 = cdf2[1:]
    return Ksout, Krout, Hmaxout, Hrmsout, Hmeanout, Hsigout, H10out, H02out, SBout, HoLo, dLoout, dHoout, xsave, theta2dout, etaout, Ht1, cdf, Ht2, cdf2
