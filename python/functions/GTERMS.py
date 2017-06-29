import math

def GTERMS(yr,dayj,hr,daym,hrm):

    rad2deg=180/math.pi

    dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi=ORBIT(yr,dayj,hr)
    s=ds
    p=dp
    h=dh
    p1=dp1
    t=ANG360(180+hr*(360/24))

    dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi=ORBIT(yr,daym,hrm)
    Nu=dNu
    xi=dxi
    nup=dnup
    nup2=dnup2

    eqcest = []

    eqcst[1]=2*(t-s+h)+2*(xi-Nu)
    eqcst[2]=2*t
    eqcst[3]=2*(t+h)-3*s+p+2*(xi-Nu)
    eqcst[4]=t+h-90-nup
    eqcst[5]=4*(t-s+h)+4*(xi-Nu)
    eqcst[6]=t-2*s+h+90+2*xi-Nu
    eqcst[7]=6*(t-s+h)+6*(xi-Nu)
    eqcst[8]=3*(t+h)-2*s-90+2*(xi-Nu)-nup
    eqcst[9]=4*t
    eqcst[10]=4*(t+h)-5*s+p+4*(xi-Nu)
    eqcst[11]=2*t-3*s+4*h-p+2*(xi-Nu)
    eqcst[12]=6*t
    eqcst[13]=2*(t+2*(h-s))+2*(xi-Nu)
    eqcst[14]=2*(t-2*s+h+p)+2*(xi-Nu)
    eqcst[15]=t+2*s+h-90-2*xi-Nu
    eqcst[16]=2*t-s+p+180+2*(xi-Nu)
    eqcst[17]=t

    I=dI/rad2deg
    pc=dpc/rad2deg
    y=(5*cos(I)-1)*tan(pc)
    x=7*cos(I)+1
    Q=atan2(y,x)
    if Q<0:
        Q=(2*math.pi)+Q
    Q=Q*rad2deg

    eqcst[18]=t-s+h-90+xi-Nu+Q
    eqcst[19]=t+s+h-p-90-Nu
    eqcst[20]=s-p
    eqcst[21]=2*h
    eqcst[22]=h
    eqcst[23]=2*(s-h)
    eqcst[24]=2*s-2*xi
    eqcst[25]=t+3*(h-s)-p+90+2*xi-Nu
    eqcst[26]=t-3*s+h+p+90+2*xi-Nu
    eqcst[27]=2*t-h+p1
    eqcst[28]=2*t+h-p1+180
    eqcst[29]=t-4*s+h+2*p+90+2*xi-Nu
    eqcst[30]=t-h+90
    eqcst[31]=2*(t+s-h)+2*(Nu-xi)
    eqcst[32]=3*(t-s+h)+3*(xi-Nu)

    y=sin(2*pc)
    x=(1/6)*((1/tan(0.5*I))^2)-cos(2*pc)
    r=atan2(y,x)
    if r<0:
        r=(2*math.pi)+r
    r=r*rad2deg

    eqcst[33]=2*(t+h)-s-p+180+2*(xi-Nu)-r
    eqcst[34]=3*(t+h)-4*s+90+4*(xi-Nu)+nup
    eqcst[35]=2*(t+h)-2*nup2
    eqcst[36]=8*(t-s+h)+8*(xi-Nu)
    eqcst[37]=2*(2*t-s+h)+2*(xi-Nu)

    eqcst=ANG360(eqcst)

    return eqcst
