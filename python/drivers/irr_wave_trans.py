import sys
sys.path.append('../functions')
from ERRWAVBRK1 import ERRWAVBRK1
from GODA import GODA
from GODA2 import GODA2
from GODA3 import GODA3
from GODA4 import GODA4
from GODA5 import GODA5

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Irregular Wave Transformation (page 3-2 of ACES User's
# Guide). Yields cumulative probability distributions of wave heights as
# a field of irregular waves propagate from deep water through the surf
# zone.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: July 1, 2011
# Date Verified: June 8, 2012

# Requires the following functions:
# ERRWAVBRK1
# GODA
# GODA2
# GODA3
# GODA4
# GODA5

# MAIN VARIABLE LIST:
#   INPUT
#   Ho: significant deepwater wave height
#   d: water depth
#   Ts: significant wave period
#   cotnsl: cotangent of nearshore slope
#   direc: principle direction of incident wave spectrum

#   OUTPUT
#   Hs: significant wave height
#   Hbar: mean wave height
#   Hrms: root-mean-square wave height
#   H10: average of highest 10 percent of all waves
#   H2: average of highest 2 percent of all waves
#   Hmax: maximum wave height
#   Ks: shoaling coefficient
#   psi: root-mean-square surf beat
#   Sw: wave setup
#   HoLo: deepwater wave steepness
#   Kr: effective refraction coefficient
#   doH: ratio of water depth to deepwater wave height
#   doL: relative water depth

#   OTHERS
#-------------------------------------------------------------

def irr_wave_trans(metric, g, rho, labelUnitDist, labelUnitWt):

    Ho = 6.096
    d = 15.24
    Ts = 8.0
    cotnsl = 100.0
    direc = 10.0

    m2cm = 100

    g = 9.81 * m2cm
    Ho = Ho * m2cm
    d = d * m2cm

    Hb = ERRWAVBRK1(d, 0.78)
    assert (Ho < Hb), ('Error: Input wave broken (Hb  =  #6.2f m)' % Hb)

    Ks, Kr, Hmax, Hrms, Hbar, Hs, H10, H02, SBrms, HoLo, dLo, dHo, deepd, theta, Sw, Hxo, cdfo, Hx, cdfx = GODA(Ho, d, Ts, cotnsl, direc, g)

    # TODO graphing
    '''
    figure(1)
    plot(Hxo/m2cm,cdfo)
    title('Deep Water')
    xlabel('H [m]')
    ylabel('CDF')

    figure(2)
    plot(Hx/m2cm,cdfx)
    title('Subject Depth')
    xlabel('H [m]')
    ylabel('CDF2')
    '''

    print('\t\t %s \t\t %s \n' % ('Subject','Deep'))
    print('%s \t\t %-6.2f \t %-6.2f \n' % ('Hs', Hs[2]/m2cm, Hs[1]/m2cm))
    print('%s \t %-6.2f \t %-6.2f \n' % ('Hmean', Hbar[2]/m2cm, Hbar[1]/m2cm))
    print('%s \t %-6.2f \t %-6.2f \n' % ('Hrms', Hrms[2]/m2cm, Hrms[1]/m2cm))
    print('%s \t %-6.2f \t %-6.2f \n' %('H10%', H10[2]/m2cm, H10[1]/m2cm))
    print('%s \t %-6.2f \t %-6.2f \n' % ('H02%', H02[2]/m2cm, H02[1]/m2cm))
    print('%s \t %-6.2f \t %-6.2f \n' % ('Hmax%', Hmax[2]/m2cm, Hmax[1]/m2cm))
    print(' ')
    print('%s \t\t %-6.4f \t %-6.4f \n' % ('Ks', Ks[2], Ks[1]))
    print('%s \t %-6.4f \t %-6.4f \n' % ('SBrms', SBrms[2]/m2cm, SBrms[1]/m2cm))
    print('%s \t\t %-6.4f \t %-6.4f \n' % ('Sw', Sw[2]/m2cm, Sw[1]/m2cm))
    print('%s \t %-6.4f \t %-6.4f \n' % ('Ho/Lo', HoLo[1], HoLo[1]))
    print('%s \t\t %-6.4f \n' % ('Kr', Kr[1]))
    print('%s \t %-6.4f \t %-6.4f \n' % ('d/Ho', dHo[2], dHo[1]))
    print('%s \t %-6.4f \t %-6.4f \n' % ('d/Lo', dLo[2], dLo[1]))

irr_wave_trans(0,0,0,0,0)
