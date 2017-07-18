import math

from ANG360 import ANG360
from ORBIT import ORBIT

def GTERMS(yr,dayj,hr,daym,hrm):
    rad2deg=180.0/math.pi

    dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi=ORBIT(yr,dayj,hr)
    s=ds
    p=dp
    h=dh
    p1=dp1
    t=ANG360(180.0+hr*(360.0/24.0))

    dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi=ORBIT(yr,daym,hrm)
    Nu=dNu
    xi=dxi
    nup=dnup
    nup2=dnup2

    eqcst = []

    eqcst.append(2*(t-s+h)+2*(xi-Nu))
    eqcst.append(2*t)
    eqcst.append(2*(t+h)-3*s+p+2*(xi-Nu))
    eqcst.append(t+h-90-nup)
    eqcst.append(4*(t-s+h)+4*(xi-Nu))
    eqcst.append(t-2*s+h+90+2*xi-Nu)
    eqcst.append(6*(t-s+h)+6*(xi-Nu))
    eqcst.append(3*(t+h)-2*s-90+2*(xi-Nu)-nup)
    eqcst.append(4*t)
    eqcst.append(4*(t+h)-5*s+p+4*(xi-Nu))
    eqcst.append(2*t-3*s+4*h-p+2*(xi-Nu))
    eqcst.append(6*t)
    eqcst.append(2*(t+2*(h-s))+2*(xi-Nu))
    eqcst.append(2*(t-2*s+h+p)+2*(xi-Nu))
    eqcst.append(t+2*s+h-90-2*xi-Nu)
    eqcst.append(2*t-s+p+180+2*(xi-Nu))
    eqcst.append(t)

    I=dI/rad2deg
    pc=dpc/rad2deg
    y=(5*math.cos(I)-1)*math.tan(pc)
    x=7*math.cos(I)+1
    Q=math.atan2(y,x)
    if Q<0:
        Q=(2*math.pi)+Q
    Q=Q*rad2deg

    eqcst.append(t-s+h-90+xi-Nu+Q)
    eqcst.append(t+s+h-p-90-Nu)
    eqcst.append(s-p)
    eqcst.append(2*h)
    eqcst.append(h)
    eqcst.append(2*(s-h))
    eqcst.append(2*s-2*xi)
    eqcst.append(t+3*(h-s)-p+90+2*xi-Nu)
    eqcst.append(t-3*s+h+p+90+2*xi-Nu)
    eqcst.append(2*t-h+p1)
    eqcst.append(2*t+h-p1+180)
    eqcst.append(t-4*s+h+2*p+90+2*xi-Nu)
    eqcst.append(t-h+90)
    eqcst.append(2*(t+s-h)+2*(Nu-xi))
    eqcst.append(3*(t-s+h)+3*(xi-Nu))

    y=math.sin(2*pc)
    x=(1.0/6.0)*((1.0/math.tan(0.5*I))**2)-math.cos(2*pc)
    r=math.atan2(y,x)
    if r<0.0:
        r=(2*math.pi)+r
    r=r*rad2deg

    eqcst.append(2*(t+h)-s-p+180+2*(xi-Nu)-r)
    eqcst.append(3*(t+h)-4*s+90+4*(xi-Nu)+nup)
    eqcst.append(2*(t+h)-2*nup2)
    eqcst.append(8*(t-s+h)+8*(xi-Nu))
    eqcst.append(2*(2*t-s+h)+2*(xi-Nu))

    eqcst=[ANG360(i) for i in eqcst]

    return eqcst