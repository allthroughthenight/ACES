import math

from ORBIT import ORBIT

def NFACS(yr,dayj,hr):
    deg2rad=math.pi/180

    dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi=ORBIT(yr,dayj,hr)

    I=dI*deg2rad
    Nu=dNu*deg2rad
    pc=dpc*deg2rad

    sinI=math.sin(I)
    sinI2=math.sin(I/2)
    sin2I=math.sin(2*I)
    cosI=math.cos(I)
    cosI2=math.cos(I/2)
    tanI2=math.tan(I/2)

    eq73=(2.0/3.0-sinI**2)/0.5021
    eq74=sinI**2/0.1578
    eq75=sinI*cosI2**2/0.3800
    eq76=sin2I/0.7214
    eq77=sinI*sinI2**2/0.0164
    eq78=cosI2**4/0.9154
    eq149=cosI2**6/0.8758
    eq196=math.sqrt(0.25+1.5*(cosI*math.cos(2*pc)/cosI2**2)+(9.0/4.0)*(cosI**2/cosI2**4))
    eq207=eq75*eq196
    eq213=math.sqrt(1.0-12*tanI2**2*math.cos(2*pc)+36*tanI2**4)
    eq215=eq78*eq213
    eq227=math.sqrt(0.8965*sin2I**2+0.6001*sin2I*math.cos(Nu)+0.1006)
    eq235=0.001+math.sqrt(19.0444*sinI**4+2.7702*sinI**2*math.cos(2*Nu)+0.0981)

    fndcst = []

    fndcst.append(eq78)
    fndcst.append(1.0)
    fndcst.append(eq78)
    fndcst.append(eq227)
    fndcst.append(fndcst[0]**2)
    fndcst.append(eq75)
    fndcst.append(fndcst[0]**3)
    fndcst.append(fndcst[0]*fndcst[3])
    fndcst.append(1.0)
    fndcst.append(fndcst[0]**2)
    fndcst.append(eq78)
    fndcst.append(1.0)
    fndcst.append(eq78)
    fndcst.append(eq78)
    fndcst.append(eq77)
    fndcst.append(eq78)
    fndcst.append(1.0)
    fndcst.append(eq207)
    fndcst.append(eq76)
    fndcst.append(eq73)
    fndcst.append(1.0)
    fndcst.append(1.0)
    fndcst.append(eq78)
    fndcst.append(eq74)
    fndcst.append(eq75)
    fndcst.append(eq75)
    fndcst.append(1.0)
    fndcst.append(1.0)
    fndcst.append(eq75)
    fndcst.append(1.0)
    fndcst.append(eq78)
    fndcst.append(eq149)
    fndcst.append(eq215)
    fndcst.append(fndcst[0]**2*fndcst[3])
    fndcst.append(eq235)
    fndcst.append(fndcst[0]**4)
    fndcst.append(eq78)

    return fndcst