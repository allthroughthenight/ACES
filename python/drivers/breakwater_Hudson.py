
## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Breakwater Design Using Hudson and Related Equations
# (page 4-1 in ACES User's Guide). Estimates armor weight, minimum crest,
# width, armor thickness, and the number of armor units per unit area of
# a breakwater using Hudson and related equations.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 13, 2011
# Date Modified:

# Requires the following functions:
# no functions required

# MAIN VARIABLE LIST:
#   INPUT
#   unitwt: armor specific unit weight (N/m^3) - 1 N/m^3 = 157 ft/lb^3
#   H: wave height (m)
#   Kd: stability coefficient
#   kdelt: layer coefficient
#   P: average porosity of armor layer
#   cotssl: cotangent of structure slope
#   n: number of armor units comprising the thickness of the armor layer

#   OUTPUT
#   w: weight of individual armor unit (N)
#   b: crest width of breakwater (m)
#   r: average cover layer thickness (m)
#   Nr: number of single armor units per unit surface area

#   OTHERS
#   rho: density of water (kg/m^3)
#   H20weight: specific weight of water
#-------------------------------------------------------------

def breakwater_Hudson(unitwt, H, Kd, kdelt, P, cotssl, n):
    unitwt = 165
    H = 11.50
    Kd = 10.0
    kdelt = 1.02
    P = 54.0
    cotssl = 2.00
    n = 2

    g = 32.17
    rho = 1.989
    H20weight = rho * g # 64 lb/ft^3 for seawater, 62.4 for fresh

    specgrav = unitwt / H20weight

    w = (unitwt * H**3) / (Kd * (specgrav - 1.0)**3 * cotssl)
    r = n * kdelt * (w / unitwt)**(1 / 3)
    Nr = 1000 * n * kdelt * (1 - P / 100) * (unitwt / w)**(2 / 3)
    b = 3 * kdelt * (w / unitwt)**(1 / 3)

    if g == 9.81:
        if w > 8000:
            w = w / 8896.4 # 1 ton=8896.4 N
            units = 'tons'
        else:
            units = 'N'
    elif g == 32.17:
        if w > 2000:
            w = w / 2000
            units = 'tons'
        else:
            units = 'lbs'

    print('%s \t\t %-6.2f \t \n' % ('Weight of individual unit', w))
    print('%s \t\t\t\t %-6.2f \t \n' % ('Crest width',b))
    print('%s \t\t %-6.2f \t \n' % ('Average cover layer thickness', r))
    print('%s \t\t %-6.2f \t \n' % ('Number of single armor unit', Nr))

breakwater_Hudson(165, 11.50, 10.0, 1.02, 54.0, 2.00, 2)
