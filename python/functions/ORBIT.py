import math

from ANG360 import ANG360

def ORBIT(yr,dayj,hr):

    pi180=math.pi/180

    x=math.floor((yr-1901)/4)
    dday=dayj+x-1 # adding in multiple leap years
    dyr=yr-1900

    # Determine primary and seconday orbital functions
    # Moon's node
    Nepoch=259.1560564 # for Jan 1, 1900
    # epoch=125.069 for Jan 1, 2000
    dN=Nepoch-19.328185764*dyr-0.0529539336*dday-0.0022064139*hr

    # redefines angle in 0-360 format
    dN=ANG360(dN)
    N=dN*pi180

    # Lunar perigee
    pepoch=334.3837214 # for Jan 1, 1990
    # epoch=83.294 for Jan 1, 2000
    dp=pepoch+40.66246584*dyr+0.111404016*dday+0.004641834*hr
    dp=ANG360(dp)

    I=math.acos(0.9136949-0.0356926*math.cos(N))
    dI=ANG360(I/pi180)

    Nu=math.asin(0.0897056*math.sin(N)/math.sin(I))
    dNu=Nu/pi180
    xi=N-2*math.atan(0.64412*math.tan(N/2))-Nu
    dxi=xi/pi180
    dpc=ANG360(dp-dxi)

    # Mean longitude of the sun
    hepoch=280.1895014 # for Jan 1, 1900
    # Hepoch=270.973 for Jan 1, 2000
    dh=hepoch-0.238724988*dyr+0.9856473288*dday+0.0410686387*hr
    dh=ANG360(dh)

    # Solar perigee
    p1epoch=281.2208569 # for Jan 1, 1900
    # p1epoch=282.940 for Jan 1, 2000
    dp1=p1epoch+0.01717836*dyr+0.000047064*dday+0.000001961*hr
    dp1=ANG360(dp1)

    # Mean longitude of the moon
    sepoch=277.0256206 # for Jan 1, 1900
    # sepoch=211.744 for Jan 1, 2000
    ds=sepoch+129.38482032*dyr+13.176396768*dday+0.549016532*hr
    ds=ANG360(ds)
    nup=math.atan(math.sin(Nu)/(math.cos(Nu)+0.334766/math.sin(2*I)))
    dnup=nup/pi180
    nup2=math.atan(math.sin(2.*Nu)/(math.cos(2.*Nu)+0.0726184/int(math.sin(I))^2))/2
    dnup2=nup2/pi180

    return dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi
