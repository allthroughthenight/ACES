import sys
sys.path.append('../functions')
from ERRSTP import ERRSTP
from ERRWAVBRK2 import ERRWAVBRK2
from LWTDWS import LWTDWS
from LWTGEN import LWTGEN
from QOVERT import QOVERT
from QOVERT_IRR import QOVERT_IRR
from RUNUPR import RUNUPR
from RUNUPS import RUNUPS
from WAVELEN import WAVELEN

#check for option 3, vert wall
## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Wave Runup and Overtopping on Impermeable Structures (page 5-2
# in ACES User's Guide). Provides estimates of wave runup and overtopping
# on rough and smooth slope structures that are assumed to be impermeable

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 18, 2011
# Date Verified: June 6, 2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK2
# LWTDWS
# LWTGEN
# QOVERT
# QOVERT_IRR
# RUNUPR
# RUNUPS
# WAVELEN

# MAIN VARIABLE LIST:
#   MANDATORY INPUT
#   H: incident wave height (Hs for irregular waves)
#   T: wave period (Tp for irregular waves)
#   cotphi: cotan of nearshore slope
#   ds: water depth at structure toe
#   cottheta: cotan of structure slope (0.0 for vertical walls)
#   hs: structure height above toe

#   OPTIONAL INPUT
#   a: empirical coefficient for rough slope runup
#   b: empirical coefficeint for rough slope runup
#   alpha: empirical coefficient for overtopping
#   Qstar0: empiricial coefficient for overtopping
#   U: onshore wind velocity for overtoppping
#   R: wave runup (if known)

#   MANDATORY OUTPUT
#   H0: deepwater wave height
#   relht0: deepwater realtive height (d / H)
#   steep0: deepwater wave steepness

#   OPTIONAL OUTPUT
#   R: wave runup
#   Q: overtopping

#   OTHERS
#   freeb: freeboard
#-------------------------------------------------------------

def runup_overtopping(H, T, cotphi, ds, cottheta, hs):

    H = 7.5
    T = 10.0
    cotphi = 100.0
    ds = 12.50
    cottheta = 3.0
    hs = 20.00
    g = 32.17

    m = 1 / cotphi

    print('%s \n\n' % 'Calculation and slope type options: ')
    print('%s \n' % 'Monochromatic Waves')
    print('%s \n' % '[1] Rough <------------- Runup -------------> [2] Smooth')
    print('%s \n' % '[3] Rough <----------- Overtopping ---------> [4] Smooth')
    print('%s \n\n' % '[5] Rough <----- Runup and Overtopping -----> [6] Smooth')
    print('%s \n' % 'Irregular Waves')
    print('%s \n\n' % '[7] Rough <----- Runup and Overtopping -----> [8] Smooth')

    option = raw_input('Select option: ')
    print('\n')

    assert (ds < hs), ('Error: Method does not apply to submerged structures.')

    Hbs = ERRWAVBRK2(T, m, ds)
    assert (H < Hbs), ('Error: Wave broken at structure (Hbs  =  %6.2f m' % Hbs)

    c, c0, cg, cg0, k, L, L0, reldep = LWTGEN(ds, T, g)

    steep, maxstp = ERRSTP(H, ds, L)
    assert (steep < maxstp), ('Error: Input wave unstable (Max: %0.4f,  [H / L]  =  %0.4f' % (maxstp, steep))

    alpha0, H0 = LWTDWS(0, c, cg, c0, H)

    relht0 = ds / H0
    steep0 = H0 / (g * T**2)

    if cottheta == 0:
        assert (option != 1 and option != 5 and option and 7), ('Error: Vertical wall cannot have rough slope.')
        theta = 0.5 * math.pi
        ssp = 1000
    else:
        theta = math.atan(1 / cottheta)
        ssp = (1 / cottheta) / math.sqrt(H / L0)

    print('%s \n' % 'Deepwater')
    print('\t %s \t\t %-6.3f \n' % ('Wave height', H0))
    print('\t %s \t %-6.3f \n' % ('Relative height', relht0))
    print('\t %s \t %-6.6f \n\n' % ('Wave steepness', steep0))

    freeb = hs - ds

    if option == 1 or option == 5 or option  == 7 or option == 8:
        # Empirical coefficients for rough slope runup
        a = 0.956
        b = 0.398

    if option > 2:
        # Empirical coefficients and values for overtopping
        alpha = 0.076463
        Qstar0 = 0.025
        U = 35.0 * 1.15077945 # 1 knots  =  1.15077945 mph
        if option == 3 or option == 4:
            R = 20.0

    if option == 1:
        R = RUNUPR(H, ssp, a, b)
        print('%s \t %-6.3f \n' % ('Runup', R))
    elif option == 2:
        R = RUNUPS(H, L, ds, theta, ssp)
        print('%s \t %-6.3f \n' % ('Runup', R))
    elif option == 3:
        Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, g)
        print('%s \t %-6.3f \n' % ('Overtopping rate per unit width', Q))
    elif option == 4:
        Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, g)
        print('%s \t %-6.3f \n' % ('Overtopping rate per unit width', Q))
    elif option == 5:
        R = RUNUPR(H, ssp, a, b)
        Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, g)
        print('%s \t %-6.3f \n' % ('Runup', R))
        print('%s \t %-6.3f \n' % ('Overtopping rate per unit width', Q))
    elif option == 6:
        R = RUNUPS(H, L, ds, theta, ssp)
        Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, g)
        print('%s \t %-6.3f \n' % ('Runup', R))
        print('%s \t %-6.3f \n' % ('Overtopping rate per unit width', Q))
    elif option == 7:
        R = RUNUPR(H, ssp, a, b)
        Q = QOVERT_IRR(H0, freeb, R, Qstar0, alpha, theta, U, g)
        print('%s \t %-6.3f \n' % ('Runup', R))
        print('%s \t %-6.3f \n' % ('Overtopping rate per unit width', Q))
    elif option == 8:
        R = RUNUPS(H, L, ds, theta, ssp)
        Q = QOVERT_IRR(H0, freeb, R, Qstar0, alpha, theta, U, g)
        print('%s \t %-6.3f \n' % ('Runup', R))
        print('%s \t %-6.3f \n' % ('Overtopping rate per unit width', Q))

runup_overtopping(0, 0, 0, 0, 0, 0,)
