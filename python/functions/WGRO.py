import math

from ERRWAVBRK1 import ERRWAVBRK1
from WGDL import WGDL
from WGFD import WGFD
from WGFL import WGFL

# Simple wave growth equations (calculated in metric units)
#   Modified SPM-like technology
#       Garratt's drag law used to estimated Ua
#       Ua used in fetch- and duration-limited forms
#       Ue used only for fully developed forms

#   INPUT
#   d: average water depth across fetch
#   F: wind fetch length
#   phi: angle between winds and waves
#   tfin: wind duration
#   ue: equivalent neutral windspeed (at 10 m)
#   wgtyp: wave-growth equation type
#           1 = open water (deep)
#           2 = open water (shallow)
#           3 = restricted fetch (deep)
#           4 = restricted fetch (shallow)

#   OUTPUT
#   ua: adjusted windspeed
#   Hmo: estimated wave height
#   Tp: estimated wave period
#   wgmsg: message describing wave growth type

def WGRO(d, F, phi, tfin, ue, wgtyp):
    g = 9.81
    ua = ue*math.sqrt(0.75+0.067*ue)

    if wgtyp > 2:
        cosphi = math.cos(phi*math.pi/180.0)
        uecos = ue*cosphi
        uacos = ua*cosphi

    if wgtyp == 1:
        #Open water - deep

        #Determine min duration required for fetch-limited conditions
        durfl = 68.8*(F**(2.0/3.0)/(g**(1.0/3.0)*ua**(1.0/3.0)))
        
        #Check for fetch-limited or duration-limited 
        if tfin > durfl:
            #Fetch-limited
            wgmsg = "Deepwater fetch-limited"
            Hmo, Tp = WGFL(ua, F, d, g, wgtyp)
        else:
            #Duration-limited
            wgmsg = "Deepwater duration-limited"
            Hmo, Tp = WGDL(ua, tfin, g, wgtyp)
        
        #Check for full-developed conditions
        Hfd, Tfd = WGFD(ue, g)
        
        if Hmo > Hfd or Tp > Tfd:
           Hmo = Hfd
           Tp = Tfd
           wgmsg = "Deepwater full-developed"
    elif wgtyp == 2:
        #Open water - shallow
        wgmsg = "Shallow water fetch-limited"
        Hmo, Tp = WGFL(ua, F, d, g, wgtyp)
        
        Hb = ERRWAVBRK1(d, 0.78);
        if not (Hmo < Hb):
            errorMsg = "Error: Wave broken (Hb = %6.2f m)" % Hb
            print(errorMsg)
            return None, None, None, errorMsg
    elif wgtyp == 3:
        #Restricted fetch - deep

        #Determin min duraction required for fetch-limited conditions
        durfl = 51.09*(F**0.72/(g**0.28*uacos**0.44))
        
        #Check for fetch-limited or duration-limited 
        if tfin > durfl:
            #Fetch-limited
            wgmsg = "Deepwater fetch-limited"
            Hmo, Tp = WGFL(uacos, F, d, g, wgtyp)
        else:
            #Duration-limited
            wgmsg = "Deepwater duration-limited"
            Hmo, Tp = WGDL(uacos, tfin, g, wgtyp)

        #Check for full-developed conditions
        Hfd, Tfd = WGFD(uecos, g)
       
        if Hmo > Hfd or Tp > Tfd:
            Hmo = Hfd
            Tp = Tfd
            wgmsg = "Deepwater full-developed"
    elif wgtyp == 4:
        #Restricted fetch - shallow
        wgmsg = "Shallow water fetch-limited"
        Hmo, Tp = WGFL(uacos, F, d, g, wgtyp)
        
        Hb = ERRWAVBRK1(d, 0.78)
        if not (Hmo < Hb):
            errorMsg = "Error: Wave broken (Hb = %6.2f m)" % Hb
    # end if

    return ua, Hmo, Tp, wgmsg