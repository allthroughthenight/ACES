from helper_functions import *
import math

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Constituent Tide Record Generation (page 1-4 in ACES User's Guide)
# Provides a tide elevation record at a specific time and locale using
# known amplitudes and epochs for individual harmonic constiuents

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Transferred: April 11, 2011
# Date Verified: May 30, 2012

# Requires the following functions:
# ANG360
# DAYOYR
# GAGINI
# GTERMS
# NFACS
# ORBIT
# TIDELV

# MAIN VARIABLE LIST:
#   INPUT
#   year: year simulation starts
#   mon: month simulation starts
#   day: day simulation starts
#   hr: hr simulation starts
#   tlhrs: length of record (hr)
#   nogauge: total number of gauges (default=1)
#   ng: gauge of interest (default=1)
#   glong: gauge longitude (deg)
#   delt: output time interval (min)
#   gauge0: mean water level height above datum
#   cst: constituents name (read-in from file called tides.txt)
#   amp: amplitdutes of constituents (m, read-in from file)
#   ep: epochs of constituents (read-in from file)
#   requires constituent data entry in tides.txt

#   OUTPUT
#   ytide: tidal surface elevations

#   OTHERS
#   dayj: Julian day of the year (1-365/366 if leap year)
#   alpha: angular arguments for constiuents (deg)
#   fndcst: node factors for constiuents (deg)
#   eqcst: Greenwhich equlibrium arguments for constituents (deg)
#   acst: orbital speeds of constituents (deg/hr)
#   pcst: number of tide cycles per day per constiuent
#-------------------------------------------------------------

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
