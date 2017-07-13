import math

# Fetch-limited wave growth estimates

#   INPUT
#   u: wind velocity
#   F: wind fetch
#   d: average water depth over fetch
#   g: gravitation acceleration
#   ue: equivalent neutral windspeed (at 10 m)
#   wgtyp: wave-growth equation type
#           1 = open water (deep)
#           2 = open water (shallow)
#           3 = restricted fetch (deep)
#           4 = restricted fetch (shallow)

#   OUTPUT
#   Hfl: fetch-limited wave height
#   Tfl: fetch-limited wave period

def WGFL(u, F, d, g, wgtyp):
    xbar=g*F/(u**2);
    dbar=g*d/(u**2);

    if wgtyp == 1:
        #Open water - deep
        Hfl = 0.0016*(u**2/g)*xbar**(1.0/2.0)
        Tfl = 0.2857*(u/g)*xbar**(1.0/3.0)
    elif wgtyp == 2:
        #Open water - shallow
        c1 = math.tanh(((0.0016/0.283)*xbar**0.5)/\
            math.tanh(0.530*dbar**0.75))
        c2 = math.tanh(0.530*dbar**0.75)
        c3 = (u**2/g)*0.283
        
        Hfl = c1*c2*c3
        
        c1 = math.tanh(((0.2857/7.54)*xbar**0.333)/\
            math.tanh(0.833*dbar**0.375))
        c2 = math.tanh(0.833*dbar**0.375)
        c3 = (u/g)*7.54
        
        Tfl = c1*c2*c3;
    elif wgtyp == 3:
        #Restricted fetch - deep
        #u=uacos(phi)
        Hfl = 0.0015*(u**2/g)*xbar**(1.0/2.0);
        Tfl = 0.3704*(u/g)*xbar**(0.28);
    else:
        #Restricted fetch - shallow
        #u=uacos(phi)
        c1=math.tanh(((0.0015/0.283)*xbar**0.5)/\
            math.tanh(0.530*dbar**0.75))
        c2 = math.tanh(0.530*dbar**0.75)
        c3 = (u**2/g)*0.283
        
        Hfl = c1*c2*c3
        
        c1 = math.tanh(((0.3704/7.54)*xbar**0.28)/\
            math.tanh(0.833*dbar**0.375))
        c2 = math.tanh(0.833*dbar**0.375)
        c3 = (u/g)*7.54
        
        Tfl = c1*c2*c3
    # end if

    return Hfl, Tfl