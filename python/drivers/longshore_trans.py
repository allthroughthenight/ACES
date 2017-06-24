from helper_functions import *
import math

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Longshore Sediment Transport (page 6-1 in ACES User's Guide).
# Provides estimates of the potential longshore transport rate under the
# action of waves

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 21, 2011
# Date Modified:

# Requires the following functions:
# DEEP_TRANS
# BREAK_TRANS

# MAIN VARIABLE LIST:
#   INPUT
#   H: Wave height (either deepwater or breaking) [ft]
#   alpha: wave angle (either deepwater angle of wave crest or crest angle
#          with shoreline) [deg]
#   K: dimensionless coefficient [default value 0.39]

#   OUTPUT
#   Q: sediment transport rate [yd^3/year]

#   OTHERS
#   g: gravity [32.17 ft/s^2]
#   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs/ft^3]
#   rhos: density of sediment [5.14 slugs/ft^3 in FORTRAN source code]
#-------------------------------------------------------------

def longshore_trans():

    # rho = 1.989 #(64 lb/ft^3)/g  =  1.989 slugs/ft^3

    # single multi
    # imperial metric
    # salt or fresh
    g = 0
    rho = 0

    metric = True
    metric = input('Input in imperial or SI units? (m or s): ')

    if metric == 'm':
        metric = True
        g = 9.81
    elif metric == 'M':
        metric = True
        g = 9.81
    else:
        g = 32.17
        metric = False

    salt_water = True
    salt_water = input('Fresh or Salt water? (F or S): ')

    if salt_water == 's':
        salt_water = True
    elif salt_water == 'S':
        salt_water = True
    else:
        salt_water = False

    if metric:
        labelUnitDist = 'meters'
    else:
        labelUnitDist = 'feet'

    if salt_water:
        rho = 1.989
    else:
        rho = 1.94

    rhos=165.508/g

    print('Calculation options: ')
    print('[1] Transport using deepwater wave conditions')
    print('[2] Transport using breaking wave conditions')

    option = input('Select option: ')
    print('\n')

    Ho = 0
    Hb = 0
    alpha = 0
    K = 0

    Ho = input('Enter Ho: depp water wave height ('+ labelUnitDist+ '): ')
    Hb = input('Enter Hb: breaking wave height(' + labelUnitDist + '): ')
    alpha = input('Enter alpha: wave crest angle with shoreline (deg): ')
    K = input('Enter K: emprical coefficient: ')

    Ho = 0
    Hb = 0
    alpha = 0
    K = 0

    if option == 1:
        Q = DEEP_TRANS(Ho, alpha, K, rho, g, rhos)
    else:
        Q = BREAK_TRANS(Hb, alpha, K, rho, g, rhos)

    #Q = Q*1168800 #ACES conversion
    Q = Q * 1168775.04 #convert from ft^3/s to yd^3/yr

    print('%s \t %13.0f \n' % ('Sediment transport rate', Q))

    return Q

longshore_trans()
