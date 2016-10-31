##% Predicts wave transmission through rubble-mound breakwaters
##
##%   INPUT
##%   H: wave height
##%   T: wave period
##%   d: water depth
##%   hs: height of structure
##%   b: top width of structure
##%   numlay: number of horizontal layers in breakwater
##%   thk: thickness of each layer
##%   len: length of each material in each layer
##%   numat: number of materials in the breakwater
##%   diam: mean diameter of the various materials
##%   por: porosity of the materials
##%   cot: slope of the seaward face of the breakwater
##%   nu: kinematic viscosity (0.0000141 ft^2/s)
##%   g: acceleration of gravity
##
##%   OUTPUT
##%   KTt: wave transmission through structure coefficient
##%   Kto: wave transmission by overtopping coefficient
##%   KT: total wave transmission coefficient
##%   Kr: wave reflection coefficient
##%   Ht: transmitted wave height
##%   L: wave length at structure
##
##%   OTHER
##%   A: wave amplitude
##%   porref: porosity of reference material (0.435)
##%   diamref: one half mean diameter of reference material
##%   L: wavelength
##%   ko: wavenumber
##%   lsub: submerged horizontal length of breakwater
##%   lsl: relative slope length
##%   AIhomog: wave amplitude of equivalent incident wave on an equivalent
##%            homogenous breakwater
##%   traphead: head difference across trapezoidal breakwater
##%   Kr and Kt: reflection and transmission coefficients of a trapezoidal
##%              multilayered breakwater
##%   L0: deepwater wavelength
##%   surf: surf parameter
##%   R: runup on a stone breakwater
##%   freeb: breakwater freeboard
from ACES import *
from numpy import tanh, sqrt, pi, tan, arctan, abs
def MADSEELG(H,T,d,hs,b,numlay,thk,lenY,nummat,diam,por,cotssl,nu,g):
    
    deg2rads=pi/180;
    A=H/2;
    
    #%Porosity of reference material
    porref=0.435;
    
    #%Mean diameter of reference material
    diamref=diam[0]*0.5;

    L,ko=WAVELEN(d,T,50,g);

    #%Submerged horizontal length of breakwater
    lsub=d*cotssl;
    if (hs<d):
        lsub=hs*cotssl;
    
    tmin=sqrt((2*pi*1.25*lsub)/(g*tanh(2*pi*d/(1.25*lsub))));

    
    if (T<tmin):
        print('Error: Minimum wave period to be analyzed is %4.2f s.', tmin);
    
    phi=5.0*deg2rads;

    #% begin iterating for phi
    diff=100;
    while (diff>(10**-3)):
        RIi,Ru,fs=MADSN2(lsub,phi,ko);
        newphi=0.29*(diam[0]/d)**0.2*(Ru*2*A/(d/cotssl))**0.3*fs;
        newphi=arctan(newphi)/2;
        diff=abs(newphi-phi);
        phi=newphi;
    

    #%find appropriate model correction factor to account for model slope
    if ((1/cotssl)<0.4):
        cf=1.02;
    elif ((1/cotssl)>0.68):
        cf=0.89;
    else:
        cf=1.28-0.578*(1/cotssl);
    
    RIi=RIi*cf;
    AIhomog=RIi*A;
    dht=2.0*Ru*A;
    dhe=dht;
    diff=100;
    
    ##% begin iterating for recthead to find head difference across equivalent
    ##% rectangular breakwater
    while (diff>0.005 ):
        lequiv=EQBWLE(dhe,dht,d,nummat,numlay,diam,por,thk,lenY,porref,diamref);
        Ti,Ri=EQBWTRCO(porref,ko,diamref,AIhomog,d,nu,lequiv,g);
        olddhe=dhe;
        dhe=(1+Ri)*RIi*A;
        diff=abs(olddhe-dhe);
    
    Kr=Ri*RIi;
    KTt=Ti*RIi;

    L0=(g*(T**2))/(2*pi);

    surf=(1/cotssl)/sqrt(H/L0);

    R=H*((0.692*surf)/(1+0.504*surf));

    freeb=hs-d;

    ##% empirical coefficient
    c=0.51-(0.11*(b/hs));

    Kto=c*(1-(freeb/R));

    ##% adjust Kto if necessary


    if (((b/hs)>0.88)&(freeb<0.0)):
        Kto=c*(1-(freeb/R))-((1.0-(2.0*c))*(freeb/R));
    elif (Kto>1.0):
        Kto=1.0;
    elif ((freeb/R)>1.0):
        Kto=0.0;

    KT=sqrt(KTt**2+Kto**2);

    if (KT>1.0):
        KT=1.0;

    Ht=H*KT;

    return KTt,Kto,KT,Kr,Ht,L
