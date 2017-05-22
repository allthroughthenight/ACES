from helper_functions import *
import math

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Wave Transmission on Impermeable Structures (page 5-3 in ACES
# User's Guide). Provides estimates of wave runup and transmission on rough
# and smooth slope structures. It also addresses wave transmission over
# impermeable vertical walls and composite structures.

# Updated by: Mary Anderson,  USACE-CHL-Coastal Processes Branch
# Date Created: April 19,  2011
# Date Verified: June 6,  2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK2
# HTP
# LWTGEN
# RUNUPR
# RUNUPS
# VERTKT
# WAVELEN

# MAIN VARIABLE LIST:
#   MANDATORY INPUT
#   H: incident wave height (Hs for irregular waves)
#   T: wave period (Tp for irregular waves)
#   cotphi: cotan of nearshore slope
#   ds: water depth at structure toe
#   hs: structure height above toe
#   wth: structure crest width
#   cottheta: cotan of structure slope (0.0 for vertical wall)

#   OPTIONAL INPUT
#   a: empirical coefficient for rough slope runup
#   b: empirical coefficeint for rough slope runup
#   R: wave runup (if known)
#   hb: toe protection or composite breakwater berm height above structure
#   toe

#   MANDATORY OUTPUT
#   Ht: transmitted wave height

#   OPTIONAL OUTPUT
#   R: wave runup

#   OTHERS
#   freeb: freeboard
#-------------------------------------------------------------

def wavetrans_imperm():
    H = 7.50
    T = 10.00
    cotphi = 100.0
    ds = 10.0
    cottheta = 3.0
    hs = 15.0
    wth = 7.50
    g = 32.17

    a = 0.956
    b = 0.398
    hb = 6.00
    R = 15.0

    m = 1 / cotphi

    print('%s \n\n' % 'Calculation and slope type options: ')
    print('%s \n' % '[1] Wave transmission only for smooth slope')
    print('%s \n' % '[2] Wave transmission only for vertical wall')
    print('%s \n' % '[3] Wave runup and transmission for rough slope')
    print('%s \n\n' % '[4] Wave runup and transmission for smooth slope')

    option = raw_input('Select option: ')
    print('\n')

    if option == 2:
        if ds >= hs:
            print('Error: Method does not apply to submerged structures.')
            return

    c, c0, cg, cg0, k, L, L0, reldep = lwtgen(ds, T, g)

    Hbs = ERRWAVBRK2(T, m, ds)
    if H >= Hbs:
        print('Error: Wave broken at structure (Hbs  =  #6.2f m)' %  Hbs)
        return

    steep, maxstp = ERRSTP(H, ds, L)
    if steep >=maxstp:
        print('Error: Input wave unstable (Max: #0.4f,  [H/L]  =  #0.4f)' % (maxstp, steep))
        return

    if cottheta == 0:
        if option != 2:
            print('Error: A cotangent of zero indicates a vertical wall.')
            return
        reldep = ds / L
        if reldep <= 0.14 and reldep >= 0.5:
            print('Error: d/L conditions exceeded - 0.14 <= (d/L) <= 0.5')
            return
    else:
        theta = math.atan(1 / cottheta)
        ssp = (1 / cottheta) / math.sqrt(H / L0)

    if option == 3:
        a = 0.956
        b = 0.398
        R = RUNUPR(H, ssp, a, b)
        print('%s \t\t\t\t\t\t %-6.3f \n' %  ('Runup', R))
    elif option == 4:
        R = RUNUPS(H, L, ds, theta, ssp)
        print('%s \t\t\t\t\t\t %-6.3f \n' % ('Runup', R))

    freeb = hs - ds

    if option == 2:
        Ht = HTP(wth, hs, R, H, freeb)
        print('%s \t %-6.3f \n' % ('Transmitted wave height', Ht))
    else:
        dl = ds - hb
        Ht = VERTKT(H, freeb, wth, ds, dl)
        print('%s \t %-6.3f \n' % ('Transmitted wave height', Ht))

wavetrans_imperm()
