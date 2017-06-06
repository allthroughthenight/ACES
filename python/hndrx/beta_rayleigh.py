from helper_functions import *
import math

# ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Beta-Rayleigh Distribution (page 1-2 of ACES User's Guide).
# Provides a statistical representation for a shallow-water wave height
# distribution.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 28, 2011
# Date Verified: June 27, 2012
# Modifications done by Yaprak Onat
# Last Verified:

# Requires the following functions:
# ERRWAVBRK1
# WAVELEN
# ERRSTP

# MAIN VARIABLE LIST:
#   INPUT
#   Hmo: zero-moment wave height [m]
#   Tp: peak wave period [s]
#   d: water depth [m]

#   OUTPUT
#   Hrms: root-mean-square wave height [m]
#   Hmed: median wave height [m]
#   H13: significant wave height (average of the 1/3 highest waves) [m]
#   H110: average of the 1/10 highest waves [m]
#   H1100: average of the 1/100 highest waves [m]

#   OTHER:
#------------------------------------------------------------

def tide_generation():
    Hs0 = 4.6
    Tp = 9.50
    cottheta = 13.0
    g = 32.17

    #Coefficients provided by Mase (1989)
    amax = 2.32
    bmax = 0.77
    a2 = 1.86
    b2 = 0.71
    a110 = 1.70
    b110 = 0.71
    a13 = 1.38
    b13 = 0.70
    aavg = 0.88
    bavg = 0.69

    # Meters to feet constant for conversion
    m2ft=3.28084;

    L0 = g * (Tp**2) / (2 * math.pi)
    steep = Hs0 / L0
    if steep >= 0.142:
        print('Error: Input wave unstable (Max: 0.142,  [H / L]  =  %0.4f)' % steep)
        return

    tantheta = 1 / cottheta
    I = tantheta / math.sqrt(Hs0 / L0)

    Rmax = Hs0 * amax * (I**bmax)
    R2 = Hs0 * a2 * (I**b2)
    R110 = Hs0 * a110 * (I**b110)
    R13 = Hs0 * a13 * (I**b13)
    Ravg = Hs0 * aavg * (I**bavg)

    print('%s \t %-6.2f \n' % ('Maximum runup', Rmax))
    print('%s \t %-6.2f \n' % ('Runup exceeded by 2% of runup', R2))
    print('%s \t %-6.2f \n' % ('Avg. of highest 1 / 10 runups', R110))
    print('%s \t %-6.2f \n' % ('Avg. of highest 1 / 3 runups', R13))
    print('%s \t %-6.2f \n' % ('Maximum runup', Ravg))

tide_generation()
