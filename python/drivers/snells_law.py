import sys
sys.path.append('../functions')
from ERRSTP import ERRSTP
from ERRWAVBRK1 import ERRWAVBRK1
from ERRWAVBRK3 import ERRWAVBRK3
from LWTDWS import LWTDWS
from LWTGEN import LWTGEN
from LWTTWM import LWTTWM
from LWTTWS import LWTTWS

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Lineat Wave Theory with Snell's Law (page 3-1 in ACES User's Guide)
# Provides a simple estimate for wave shoaling and refraction using Snell's
# Law with wave properties predicted by linear wave theory

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 11, 2011
# Date Verified: June 6, 2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK1
# ERRWAVBRK3
# LWTDWS
# LWTGEN
# LWTTWM
# LWTTWS
# ERRWAVBRK3
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   H1: wave height at known location (m)
#   T: wave period at known location (sec)
#   d1: water depth at known location (m)
#   alpha1: wave crest angle (deg)
#   cotphi: cotan of nearshore slope
#   d2: water depth at desired location (m)

#   OUTPUT
#   H0: deepwater wave height (m)
#   H2: wave height at subject location (m)
#   alpha0: deepwater wave crest angle (deg)
#   alpha2: wave crest angle at subject location (deg)
#   L0: deepwater wavelength (m)
#   L1: wavelength at known location (m)
#   L2: wavelength at subject location (m)
#   c1: wave celerity at known location (m/s)
#   c0: deepwater wave celerity (m/s)
#   c2: wave celerity at subject location (m/s)
#   cg1: group speed at known location (m/s)
#   cg0: deepwater group speed (m/s)
#   cg2: group speef at subject location (m/s)
#   E1: energy density at known location (N-m/m^2)
#   E0: deepwater energy density (N-m/m^2)
#   E2: enery density at subject location (N-m/m^2)
#   P1: energy flux at known location (N-m/m-s)
#   P0: deepwater wave flux (N-m/m-s)
#   P2: wave flux at subject location (N-m/m-s)
#   HL: deepwater wave steepness
#   Ur1: Ursell number at known location
#   Ur2: Ursell number at desired location
#   Hb: breaking wave height (m)
#   db: breaking wave depth (m)
#-------------------------------------------------------------

def snells_law(H1, T, d1, alpha1, cotphi, d2):
    # default input
    H1 = 10.0
    T = 7.50
    d1 = 25.0
    alpha1 = 10.0
    cotphi = 100.0
    d2 = 20.0

    # variables being set for imperial units
    rho = 1.989
    g = 32.17
    m = 1 / cotphi

    Hb = ERRWAVBRK1(d1, 0.78)
    if H1 >= Hb:
        print("Error: Known wave broken (Hb = %6.2f m)" % Hb)
        return

    # determine known wave properties
    c1, c0, cg1, cg0, k1, L1, L0, reldep1 = LWTGEN(d1, T, g)
    E1, P1, Ur1, setdown1 = LWTTWM(cg1, d1, H1, L1, reldep1, rho, g, k1)

    steep, maxstp = ERRSTP(H1, d1, L1)
    if steep >= maxstp:
        print("Error: Known wave unstable (Max: %0.4f, [H/L] = %0.4f)" % (maxstp, steep))
        return

    # determine deepwater wave properties
    alpha0, H0 = LWTDWS(alpha1, c1, cg1, c0, H1)

    E0 = rho * g * (H0 * H0) / 8
    P0 = E0 * cg0
    HL = H0 / L0

    if HL >= (1.0 / 7.0):
        print("Error: Deepwater wave unstable, [H0/L0] > (1/7)")
        return

    # determine subject wave properties
    c2, c0, cg2, cg0, k2, L2, L0, reldep2 = LWTGEN(d2, T, g)
    alpha2, H2, kr, ks = LWTTWS(alpha0, c2, cg2, c0, H0)
    E2, P2, Ur2, setdown2 = LWTTWM(cg2, d2, H2, L2, reldep2, rho, g, k2)

    Hb, db = ERRWAVBRK3(H0, L0, T, m)
    if H2 >= Hb:
        print("Error: Subject wave broken (Hb = %6.2f m, hb = %6.2f m)" % (Hb, db))
        return

    steep, maxstp = ERRSTP(H2, d2, L2)
    if steep >= maxstp:
        print("Error: Subject wave unstable (Max: %0.4f, [H/L] = %0.4f)" % (maxstp, steep))
        return

    print('\t\t\t %s \t\t %s \t\t %s \t\t\n' % ('Known', 'Deepwater', 'Subject'))
    print('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n' % ('Wave height', H1, H0, H2))
    print('%s \t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n' % ('Wave crest angle', alpha1, alpha0, alpha2))
    print('%s \t\t %-5.2f \t %-5.2f \t\t %-5.2f \t\t\n' % ('Wavelength', L1, L0, L2))
    print('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n' % ('Celerity', c1, c0, c2))
    print('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n' % ('Group speed', cg1, cg0, cg2))
    print('%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t\n' % ('Energy density', E1, E0, E2))
    print('%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t\n' % ('Energy flux', P1, P0, P2))
    print('%s \t\t %-5.2f \t\t\t\t\t\t %-5.2f \n' % ('Ursell number', Ur1, Ur2))
    print('%s \t\t\t\t\t %-5.2f \n' % ('Wave steepness', HL))
    print('\n')
    print('%s \t\t\t\n' % 'Breaking parameters')
    print('%s \t\t %-5.2f \t\n' % ('Breaking height', Hb))
    print('%s \t\t\t %-5.2f \t\n' % ('Breaking depth', db))

snells_law(10, 7.50, 25, 10.0, 100, 20)
