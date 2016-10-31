from numpy import tanh, sinh, sqrt, pi, exp, nonzero, array, \
    sin, arcsin, cos, arccos, tan,  arctan, abs, zeros, isscalar
from scipy.special import jn
from scipy.integrate import quad

def FWTPRE(g,T,H,d,u):
    Hnon=H/(g*T**2);
    L=((g*T**2)/(2*pi))*sqrt(tanh(1.22718*d/T**2));
    if (d/L>1.5):
        Hod=0.0;
    else:
        Hod=H/d;
    unon=u/sqrt(g*H);
    return Hnon,L,Hod,unon


def ERRWAVBRK1(d,kappa):
    Hb=kappa*d;
    return Hb

def ERRSTP(H,d,L):
    steep=H/L;
    k=(2*pi)/L;
    maxstp=0.142*tanh(k*d);
    return steep,maxstp

def RUNUPR(H,xi,a,b):
    
    runupr=(H*a*xi)/(1+b*xi)
    return runupr


def ERRWAVBRK3(Ho,Lo,T,m):
    """
    % Error check for wave breaking where a finite slope is known (m>0)
    
    %   INPUT
    %   Ho: deepwater wave height
    %   m: nearshore slope
    %   Lo: deepwater wave length
    
    %   OUTPUT
    %   Hb: breaking wave height
    %   db: breaker depth
    """
    a=1.36*(1-exp(-19*m));
    b=1/(0.64*(1+exp(-19.5*m)));
    
    Hb=Ho*0.575*(m**0.031)*((Ho/Lo)**(-0.254));
    gamma=b-a*Hb/(T**2);
    db=Hb/gamma;
    return Hb,db


def WAVELEN(d,T,n,g):
    """
    %
    % function wavelength(d,T,n,g);
    %
    % n = # of iterations
    %
    % d = depth, this can be an array
    % T = period
    % n = number of iterations
    % g = 32.2 or 9.81
    """
    Leck = (g*(T**2)*0.5/pi)*sqrt(tanh(4*pi*pi*d/(T*T*g)));  #% 1984 SPM, p.2-7
    L1 = Leck;
    
    for k in range(1,n+1):
        L2 = (g*(T**2)*0.5/pi)*tanh(2*pi*d/L1);   #% check if it's right
        L1 = L2;
        
    L = L2;
    k=2*pi/L;
    if not(isscalar(d)):
        ko = nonzero(d<=0);
        L[ko] = 0;
    return L,k

def ERRWAVBRK2(T,m,ds):
    a=1.36*(1-exp(-19*m))
    b=1/(0.64*(1+exp(-19.5*m)))
    term=(ds/T**2)
    P=a+(1+9.25*m**2*b-4*m*b)/term
    
    term1=ds/(m*a*(18.5*m-8))
    term2=P**2-(((4*m*b*a)/term)*(9.25*m-4))
    Hbs=term1*(P-sqrt(term2))
    
    return Hbs


def HTP(bb,hs,R,H,free):
    """
    % Transmitted wave height by overtopping of an impermebale structure

    %   INPUT
    %   bb: structure crest width
    %   H: total structure height above sea floor
    %   R: wave runup
    %   H: incident wave height
    %   free: freeboard (difference between height of structure and still water
    %   depth at structure)
    
    %   OUTPUT
    %   Ht: transmitted wave height
    """
    
    c=0.51-0.11*(bb/hs);
    Kt=c*(1-(free/R));
    if (Kt<0):
        Kt=0.0;
    Ht=Kt*H;

    return Ht

def RUNUPS(H,L,d,theta,xi):
    """
    % Determine runup on a smooth simple slope
    
    %   INPUT
    %   H: incident wave height at toe of structure
    %   L: wave length
    %   ds: water depth at structure
    %   theta: structure slope
    %   xi: surf parameter
    
    %   OUTPUT
    %   runups: runup on a smooth slope
    """

    Cp=1.002*xi;
    nonlin=(H/L)/(tanh(2*pi*d/L)**3);
    Cnb=1.087*sqrt(pi/(2*theta))+0.775*nonlin;
    if (xi<=2):
        C=Cp;
    elif (xi>=3.5):
        C=Cnb;
    else:
        C=((3.5-xi)/1.5)*Cp+((xi-2)/1.5)*Cnb;
    runups=C*H;
    return runups


def LWTTWM(cg,h,H,L,reldep,rho,g,k):
    """
    % Miscellaneous linear wave theory bulk values
    
    %   INPUT
    %   cg: group velocity
    %   h: still water depth at waveform
    %   H: wave height
    %   L: wave length
    %   reldep: relative depth
    %   rho: water density
    %   g: gravitational acceleration
    %   k: wavenumber
    
    %   OUTPUT
    %   E: mean energy density
    %   P: mean energy flux
    %   Ur: Ursell parameter
    %   setdown: setdown
    """

    E=(1/8)*rho*g*(H**2);
    P=E*cg;
    Ur=(H*(L**2))/(h**3);

    if (reldep<0.5):
        setdown=(k*H**2)/(8*sinh(2*k*h));
    else:
        setdown=0;
    return E,P,Ur,setdown



def LWTTWS(alpha0,c,cg,c0,H0):
    """
    % Snell's law applied to determine transitional case

%   INPUT
%   alpha0: deepwater angle of wavecrest
%   c: wave celerity
%   cg: group velocity
%   c0: deepwater wave celerity
%   H0: deepwater wave height

%   OUTPUT
%   alpha: wave crest angle with shoreline
%   H: wave height
%   Kr: refraction coeffieint
%   Ks: shoaling coefficient
"""
    deg2rad=pi/180;

    arg=(c/c0)*sin(alpha0*deg2rad);
    alpha=(arcsin(arg))/deg2rad;

    ksf=sqrt(c0/(2*cg));
    krf=sqrt(cos(alpha0*deg2rad)/cos(alpha*deg2rad));
    
    H=H0*ksf*krf;
    return alpha,H,krf,ksf



def LWTGEN(h,T,g):
    """
    % Linear wave theory approximations

    %   INPUT
    %   h: still water depth at waveform
    %   T: wave period
    %   g: gravitational acceleration
    
    %   OUTPUT
    %   c: wave celerity
    %   c0: deepwater wave celerity
    %   cg: group velocity
    %   cg0: deepwater group velocity
    %   k: wavenumber
    %   L: wave length
    %   L0: deepwater wave length
    %   reldep: relative depth
    """

    #%General deepwater conditions
    c0=g*T/(2*pi);
    cg0=0.5*c0;
    L0=c0*T;

    #Local wave conditions
    L,k=WAVELEN(h,T,50,g);
    reldep=h/L;

    c=L/T;
    n=0.5*(1+((2*k*h)/sinh(2*k*h)));
    cg=n*c;
    return c,c0,cg,cg0,k,L,L0,reldep


def LWTDWS(alpha,c,cg,c0,H):
    """
    % Snell's Law applied to determine deepwater values

    %   INPUT
    %   alpha: wave crest angle with shoreline
    %   c: wave celerity
    %   cg: group velocity
    %   c0: deepwater wave celerity
    %   H: wave height
    
    %   OUTPUT
    %   alpha0: deepwater angle of wavecrest
    %   H0: deepwater wave height
    """
    deg2rad=pi/180;

    arg=(c0/c)*sin(alpha*deg2rad);
    #assert(arg<1,'Error: Violation of assumptions for Snells Law')

    alpha0=(arcsin(arg))/deg2rad;

    ksf=sqrt(c0/(2*cg)); #shoaling coefficient
    krf=sqrt(cos(alpha0*deg2rad)/cos(alpha*deg2rad)); #refraction coefficient
 
    H0=H/(ksf*krf);

    return alpha0,H0


def ERRWAVBRK(T,d,m,kappa,struct=1):
    """
    % Error check for monochromatic wave breaking

    %   INPUT
    %   T: wave period
    %   d: water depth
    %   kappa: breaking index
    %   struct: =0 for no structure, =1 for structure
    
    %   OUTPUT
    %   Hb: breaking wave height
    """


    if (m==0): #%where the nearshore slope is flat or unknown
        Hb=kappa*d;
    elif ((m!=0) & (struct==1)): #%maximum wave height in prescence of a structure
        a=1.36*(1-exp(-19*m));
        b=1/(0.64*(1+exp(-19.5*m)));
        term=(d/T**2);
        P=a+(1+9.25*m**2*b-4*m*b)/term;
    
        term1=d/(m*a*(18.5*m-8));
        term2=P**2-(((4*m*b*a)/term)*(9.25*m-4));
        Hb=term1*(P-sqrt(term2));
    return Hb


def MADSN1(nors,fos,nkol):
    """
    % Determine transmission and reflection coefficients for crib-style
    % breakwaters

    %   INPUT
    %   nors: N/sqrt(S) = 0.45
    %   fos: F/S
    %   nkol: wavenumber x porosity of reference material x equivalent length
    
    %   OUTPUT
    %   Ti: transmission coefficient
    %   Ri: reflection coefficeint
    
    %   OTHER:
    %   k: complex wave number
    
    """

    #% intermediate values
    eps=complex(nors,0)/sqrt(complex(1,-fos));
    theta=complex(0,1)*complex(nkol,0)/eps;
    c1=(complex(1,0)+eps)**2;
    c2=(complex(1,0)-eps)**2;
    c3=complex(1,0)-eps**2;
    denom=c1*exp(theta)-c2*exp(-theta);
 
    # transmission coefficient
    teq=complex(4,0)*eps/denom;
    Ti=abs(teq);

    #reflection coefficient
    req=(c3*(exp(theta)-exp(-theta)))/denom;
    Ri=abs(req);
    return Ti,Ri

def MADSN2(lsub,phi,k):
    """
    % Solves for reflection coefficient, non-dimensional runup amplitude, and
    % friction slope for rough impermeable slopes

    %   INPUT
    %   lsub: water depth x cotangent of structure slope
    %   phi: friction angle [rads]
    %   ko: wavenumber
    
    %   OUTPUT
    %   R: reflection coefficient
    %   Ru: nondimensional runup amplitude
    %   sfc: friction slope constant
    """
    
    def fun1(y):
        f=abs((jn(1,2*psi*sqrt(y))/(psi*sqrt(y)))**3);
        return f 

    def fun2(y):
        f=abs(y*(jn(1,2*psi*sqrt(y))/(psi*sqrt(y)))**2);

    L=(2*pi)/k;
    lsol=lsub/L;

    fb=tan(2*phi);
    c1=2*k*lsub;
    c2=sqrt(complex(1.0,-fb));

    arg=complex(c1,0)*c2;
    
    J0=jn(0.0,arg);
    J1=jn(1.0,arg);

    c3=(complex(0,1)/c2)*J1;

    denom=J0+c3;

    psi=complex(c1/2,0)*c2;

    req=((J0-c3)/denom)*exp(complex(0,c1));
    R=abs(req);

    rueq=exp(complex(0,c1/2))/denom;
    Ru=abs(rueq);

    if (lsol<0.05):
        fsc=0.84242;
    else:
        topint=quad(fun1,0,1);
        botint=quad(fun2,0,1);
        fsc=(4/(3*pi))*(topint/botint);
    return R,Ru,fsc


def VERTKT(H,free,bb,ds,dl):
    """
    % Transmission coefficient for a vertical breakwater

    %   INPUT
    %   H: incident wave height
    %   free: freeboard
    %   bb: crest width of vertical breakwater
    %   ds: still water level depth (from base of structure)
    %   dl: depth of water between still water level and top of berm
    
    %   OUTPUT
    %   Ht: transmitted wave height
    """
    aspect=bb/ds;
    ratio=dl/ds;
    frerat=free/H;

    if (aspect<1):
        alpha=1.8+0.4*aspect;
        beta1=0.1+0.3*aspect;
    else:
        alpha=2.2;
        beta1=0.4;

    if (dl/ds<=0.3):
        alpha=2.2;
        beta2=0.1;
    else:
        beta2=0.527-0.130/ratio;
    

    c1=max(0,1-aspect);
    c2=min(1,aspect);
    beta=c1*beta1+c2*beta2;

    if (frerat<=-(alpha+beta)):
        Kt=1.0;
    elif (frerat>=(alpha-beta)):
        Kt=0.0;
    else:
        Kt=0.5*(1-sin((pi/(2*alpha))*(frerat+beta)));
    
    Ht=Kt*H;
    return Ht


def MADSN2(lsub,phi,k):
    """
    % Solves for reflection coefficient, non-dimensional runup amplitude, and
    % friction slope for rough impermeable slopes

    %   INPUT
    %   lsub: water depth x cotangent of structure slope
    %   phi: friction angle [rads]
    %   ko: wavenumber

    %   OUTPUT
    %   R: reflection coefficient
    %   Ru: nondimensional runup amplitude
    %   sfc: friction slope constant
    """
    
    def fun1(y):
        f=abs((jn(1,2*psi*sqrt(y))/(psi*sqrt(y)))**3);
        return f

    def fun2(y):
        f=abs(y*(jn(1,2*psi*sqrt(y))/(psi*sqrt(y)))**2);
        return f

    L=(2*pi)/k;
    lsol=lsub/L;

    fb=tan(2*phi);
    c1=2*k*lsub;
    c2=sqrt(complex(1.0,-fb));

    arg=complex(c1,0)*c2;

    J0=jn(0.0,arg);
    J1=jn(1.0,arg);

    c3=(complex(0,1)/c2)*J1;
    denom=J0+c3;

    psi=complex(c1/2,0)*c2;

    req=((J0-c3)/denom)*exp(complex(0,c1));
    R=abs(req);

    rueq=exp(complex(0,c1/2))/denom;
    Ru=abs(rueq);
    
    if (lsol<0.05):
        fsc=0.84242;
    else:
        topint=quad(fun1,0,1);
        botint=quad(fun2,0,1);
        fsc=(4/(3*pi))*(topint[0]/botint[0]);
    return R,Ru,fsc



def EQBWLE(rechd,traphd,d,nummat,numlay,diam,por,thk,len1,pref,dref):
    """
    % Transforms trapezoidal breakwater into a hydraulically equivalent
    % rectangular breakwater

    %   INPUT
    %   rechd: head difference across equivalent rectangular breakwater
    %   traphd: head difference across trapezoidal breakwater
    %   d: water depth
    %   nummat: number of materials in the breakwater
    %   numlay: number of layers in the breakwater
    %   diam: mean diameter of material in the breakwater
    %   por: porosity of the various materials
    %   thk: thickness of each layer
    %   len: length of each material in the breakwater
    %   pref: porosity of reference material (0.435)
    %   dref: one half mean diameter of reference material
    
    %   OUTPUT
    %   lequiv: equivalent length of rectangular breakwater
    
    %   OTHER:
    %   betar and beta: turbulent resistance coefficients for the equivalent
    %                   and trapezoidal breakwater

    """

    #find betar and beta
    beta0=2.7;
    betar=beta0*((1-pref)/(pref**3*dref));
    beta=zeros(nummat)

    for k in range(nummat):
        beta[k]=beta0*((1-por[k])/(por[k]**3*diam[k]));

    #find equivalent rectangular breakwater length
        
    ind =zeros(nummat)
    ind2=zeros(numlay)
    len1=array(len1)
    len1=len1.reshape(nummat,numlay)
    for j in range(numlay): #layer is columns
        for k in range(nummat): #% material number is rows
            ind[k]=(beta[k]/betar)*len1[k,j];
        
        sum1=sum(ind);
        ind2[j]=(thk[j]/d)/sqrt(sum1);
    
        sum2=sum(ind2);
        lequiv=1/sum2**2*(rechd/traphd);

    return lequiv


def EQBWTRCO(pref,k,dref,aI,d,nu,lequ,g):
    """
    % Determines wave transmission and reflection coefficients for the
    % equivalent rectangular breakwater found in function EQBWLE
    
    %   INPUT
    %   pref: porosity of reference material (0.435)
    %   k: wavenumber
    %   dref: one half mean diameter of reference material
    %   aI: wave amplitude of equivalent incident wave
    %   d: water depth
    %   nu: kinematic viscosity (0.0000141)
    %   lequ: equivalent length of rectangular breakwater from EQBWLE
    %   g: acceleration of gravity

    %   OUTPUT
    %   Ti: transmission coefficient
    %   Ri: reflection coefficient

    %   OTHER
    %   Rc: critical Reynolds number
    %   F: friction factor
    %   U: complex horizontal velocity component
    %   Rd: particle Reynolds number
    %   betar: hydrodynamic characterisitc of reference material

    """
    Rc=170.0;

    #used in solving the transmission and reflection coefficients
    nors=0.45;
    ss=(pref/0.45)**2;
    kon=k*pref;
       
    betar=2.7*((1-pref)/(pref**3*dref));

    ##% guess a lambda (intermediate value) and a value for F...iterate until the
    ##% difference is less than 2%

    diff=100;
    lam=1.0;
    F=0.0;

    while (diff>0.02):
        Fnew=F;
        U=aI*sqrt(g/d)/(1+lam);
        Rd=U*dref/nu;
        F=pref/(k*lequ);
        F=F*(sqrt(1+(1+Rc/Rd)*(16*betar*aI*lequ/(3*pi*d)))-1);
        lam=k*lequ*F/(2*pref); ##calculate new lam
        diff=abs(Fnew-F)/F;

    #% used in solving the transmission and reflection coefficients
    fos=F/ss;
    #%call function MADSN1 which solves for Ti and Ri
    Ti,Ri=MADSN1(nors,fos,kon*lequ);

   
    return Ti,Ri

