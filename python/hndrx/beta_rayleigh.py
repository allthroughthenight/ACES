from helper_functions import *
import math

# ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Beta-Rayleigh Distribution (page 1-2 of ACES User's Guide).
# Provides a statistical representation for a shallow-water wave height
# distribution.

# Requires the following functions:
# ERRWAVBRK1
# WAVELEN
# ERRSTP

# MAIN VARIABLE LIST:
#   INPUT
#   Hmo: zero-moment wave height [m]
#   Tp: peak wave period [s]
#   d: water depth [m]

#   OUTPUT
#   Hrms: root-mean-square wave height [m]
#   Hmed: median wave height [m]
#   H13: significant wave height (average of the 1/3 highest waves) [m]
#   H110: average of the 1/10 highest waves [m]
#   H1100: average of the 1/100 highest waves [m]

#   OTHER:
#------------------------------------------------------------

def beta_rayleigh():

    # input
    Hmo = 9
    Tp = 4
    d = 4
    g = 10

    Hb=errwavbrk1(d,0.9)
    if Hmo < Hb:
        print('Error: Input wave broken (Hb = ', Hb, ')')

    L = wavelen(d, Tp, 50, g)
    k = wavelen(d, Tp, 50, g)
    steep = errstp(Hmo, d, l)
    maxstep = errstp(Hmo, d, l)

    if steep < maxstep:
        print('Error: Input wave unstable (Max:', maxstep, '[H/L] =', steep,'')

    dterm = d / ( g * Tp^2 )
    k = 1
    sum1 = 0

    if dterm > 0.01:
        print('Input conditions indicate Rayleigh distribution')
        Hb=sqrt(5)*Hmo
        Hinc=Hb/10000
        sigma=Hmo/4
        Hrms=2*sqrt(2)*sigma

        for x in range(2, 1001):
            H(i)=Hinc*(i-1)
            term1=exp(-(H(i)/Hrms)^2)
            term2=(2*H(i))/Hrms^2
            p(i)=term1*term2
            sum1=sum1+(p(i)*Hinc)

            if k<5 and sum1>Htype(k):
                index(k)=i
                k=k+1
        for k in xrange(4):
            sum2=0
            Hstart=H(index(k))
            Hinc=(Hb-Hstart)/10000
            pprv=p(index(k))
            Hprv=Hstart
            for i in range(1, 1001):
                Hnxt=Hstart+Hinc*(i-1)
                term1=exp(-(Hnxt/Hrms)^2)
                term2=(2*Hnxt)/Hrms^2
                pnxt=term1*term2
                darea=0.5*(pprv+pnxt)*Hinc
                sum2=sum2+(Hinc/2.0+Hprv)*darea
                pprv=pnxt
                Hprv=Hnxt
            Hout(k)=sum2/(1-Htype(k))
    else:
        Hb=d
        Hinc=Hb/100
        disp('Input conditions indicate Beta-Rayleigh distribution')
        a1=0.00089
        b1=0.834
        a2=0.000098
        b2=1.208

        d1=a1*dterm^(-b1)
        if d1<=35.0:
            print('Error: d/gT^2 approaching infinity')

        Hrms=(1/sqrt(2))*exp(d1)*Hmo

        d2=a2*dterm^(-b2)
        if d2<=35.0:
            print('Error: d/gT^2 approaching infinity')

        Hrmsq=(1/sqrt(2))*exp(d2)*Hmo^2

        # computing alpha and beta
        K1=(Hrms/Hb)^2
        K2=(Hrmsq^2)/(Hb^4)

        alpha=(K1*(K2-K1))/(K1^2-K2)
        beta=((1-K1)*(K2-K1))/(K1^2-K2)

        term1=(2*gamma(alpha+beta))/(gamma(alpha)*gamma(beta))

        for i in range(1, 101):
            H(i)=Hinc*(i-1)
            term2=(H(i)^(2*alpha-1))/(Hb^(2*alpha))
            term3=(1-(H(i)/Hb)^2)^(beta-1)
            p(i)=term1*term2*term3

            sum1=sum1+(p(i)*Hinc)
            if k<5 and sum1>Htype(k):
                index(k)=i
                k=k+1
