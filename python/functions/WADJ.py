import math
import numpy as np

from WASBL import WASBL

# Perform wind adjustments

#   INPUT
#   uobs: observed windspeed
#   zobs: elevation of wind observation
#   delt: air-sea temperature difference
#   F: fetch length
#   tobs: duration of wind observation
#   tfin: duration of final desired windspeed
#   latt: Latitude of wind observation
#   obstyp: Type of wind observation
#           1 = overwater (shipboard)
#           2 = overwater (not shipboard)
#           3 = at shore (off to onshore)
#           4 = at shore (on to offshore)
#           5 = over land
#           6 = geostrophic wind

#   OUTPUT
#   ue: equivalent neutral windspeed at 10 m elevation and at desired final
#       duration
#   error: message indication non-convergence

def WADJ(uobs, zobs, delt, F, tobs, tfin, latt, obstyp):
    m2cm = 100.0

    if obstyp == 1:
        #Ship-based wind observations over water
        u = 1.864*uobs**(7.0/9.0)
        u10m = WASBL(u*m2cm,delt, zobs*m2cm)
        u10m = u10m / m2cm
    elif obstyp == 2 or obstyp == 3:
        #Wind observation over water (not ship-based) or at the shoreline
        #(wind direction from offshore to onshore)
        u10m = WASBL(uobs*m2cm, delt, zobs*m2cm)
        u10m = u10m / m2cm
    elif obstyp == 4 or obstyp == 5:
        #Winds over land or at the shoreline (wind direction from onshore
        #to offshore)
        u = WAGEOS(uobs*m2cm, zobs*m2cm, 30)
        omega = 7.2921150*10**-5 #Earth's angular velocity (2pi/86164.09)
        f = 2*omega*math.sin(latt) #Coriolis force
        u10m = WAPBL(u, delt, f, 0, 0)
        u10m = u10m / m2cm
    elif obstyp == 6:
        #Geostrophic winds
        omega = 2*math.pi / (24*3600) #Earth's angular velocity
        f = 2*omega*math.sin(latt) #Coriolis force
        u10m = WAPBL(uobs*m2cm, delt, f, 0, 0)
        u10m = u10m / m2cm

    ue = u10m

    if F < 16000.0:
        ue *= 0.9

    if tobs <= 1.0:
        if not (tobs > 1.0):
            print("Error: Observed windspeed duration must be > 1 s.")
            return
    elif np.isclose(tobs, 3600.0):
        u3600 = ue
    elif tobs < 3600.0:
        eqshrt = 1.277 + 0.296*math.tanh(0.9*math.log10(45.0/tobs))
        u3600 = ue / eqshrt
    elif tobs > 3600.0:
        eqlong = -0.15*math.log10(tobs) + 1.5334
        u3600 = ue/eqlong

    if tfin <= 1.0:
        print("Error: Final windspeed duration must be > 1 s.")
        return
    elif np.isclose(tfin, 3600.0):
        ue = u3600
    elif tfin < 3600.0:
        eqshrt = 1.277 + 0.296*math.tanh(0.9*math.log10(45.0/tfin))
        ue = u3600*eqshrt
    elif tfin > 3600.0:
        eqlong = -0.15*math.log10(tfin) + 1.5334
        ue = u3600*eqlong

    return ue