from numpy import pi, sqrt, array, arange
from traits.api import HasTraits, Float, Int,  Array, Property, Range, String
from  scipy.special import ellipk, ellipj
from ellipke import ellipke
from ERRWAVBRK1 import ERRWAVBRK1
from matplotlib.pyplot import *
#pi=numpy.pi;




class O1(HasTraits):
    """
    determining m using bisection method
    """

    H   =Float(10);
    T   =Float(15.0);
    d   =Float(25.0);
    z   =Float(-12.50);
    xL  =Float(0.5);
    g   =Float(32.17);
    rho =Float(1.989); #%seawater set at 1025.09 kg/m^3, fresh set at 999.8 kg/m^3
    time=Float(0);

    # Values at which to evaluate the function.
    K   = Array
    m   = Float #Array
    A0  = Array
    A1  = Float #Array
    B00 = Array
    B10 = Float #Array
    L   = Array
    
    C   = Array
    E   = Array
    Ef  = Array
    Ur  = Array
    eta = Array
    u   = Array#Float
    w   = Array#Float
    dudt= Array#Float
    dwdt= Array#Float
    pres= Array#Float
    
    plotxL  =Array
    ploteta =Array
    plotuDat=Array
    plotwDat=Array
    


    descString=String("")
    

    step =0.001


    
    def __init__(self,H=9.8):
        self.on_trait_change(self.calcCnoidal,name=['H','T','d'])
        self.H=H
   
    def calcCnoidal(self):
         ##print 'The %s trait changed from %s to %s '% (name, old, new)

         H=self.H
         T=self.T
         d=self.d
         z=self.z
         xL=self.xL
         g=self.g
         rho=self.rho
         time=self.time
         
         def F(m):
             f1=(16*m*ellipk(m)**2/3.0)-(g*H*T**2/d**2)
             return f1

         twopi=(2*pi);
         epsi=H*1.0/d;
         a=1*10**-12;
         b=1-10**-12;
         
         while ((b-a)/2>=0.00001):
             xi=(a+b)/2;
             if (F(xi)==0):
                 break
             else:
                 if (F(xi)*F(b)<0):
                     a=xi;
                 elif (F(xi)*F(a)<0):
                     b=xi;
    
         m=xi #array([xi]); #
         K,E=ellipke(m);
         lam=(1-m)/m;
         mu=E/(m*K);
         theta=2*K*(xL-(time/T));
         
         SN,CN,DN,PH = ellipj(theta,m);
         CSD=CN*SN*DN;
         
         C2=(-6-16*lam+5*mu-16*lam**2+10*lam*mu+15*mu**2)/40;
         C1=(1+2*lam-3*mu)/2;
         C0=1;
         C=sqrt(g*d)*(C0+epsi*C1+epsi**2*C2); #%celerity

         L=C*T; #wave length
         Ur=(H*(L**2))/(d**3);

         if any(Ur<26):
             print('Error: Ursell parameter test failed.')

         #SN,CN,DN,PH = ellipj(theta,m);

         CSD=CN*SN*DN;
    
         A0=epsi*(lam-mu);
         A1=epsi;
         eta=d*(A0+A1*CN**2); #water surface elevation

         if any(~((z<eta) & ((z+d)>0))):
             print('Error: Point outside waveform.')

         E0=(-lam+2*mu+4*lam*mu-lam**2-3*mu**2)/3.0;
         E =rho*g*H**2*E0; #average energy density
         
         F0=E0;
         Ef=rho*g*H**2*sqrt(g*d)*F0; #%energy flux

         B00=epsi*(lam-mu);
         B10=epsi;
         u=sqrt(g*d)*(B00+B10*CN**2); #%horizontal velocity

         w=sqrt(g*d)*(4*K*d*CSD/L)*((z+d)/d)*B10; #vertical velocity
    
         dudt=sqrt(g*d)*B10*(4*K/T)*CSD; #horizontal acceleration

         term=sqrt(g*d)*(4*K*d/L)*((z+d)/d)*B10*(2*K/T);
         dwdt=term*((SN*DN)**2-(CN*DN)**2+(m*SN*CN)**2); #vertical acceleration

         P1=(1+2*lam-3*mu)/2.0;
         P0=3.0/2.0;
         Pb=rho*g*d*(P0+epsi*P1);
         pres=Pb-(rho/2)*((u-C)**2+w**2)-g*rho*(z+d); #pressure


         step=self.step  ##0.001
         plotxL=arange(-1,1+step,step);
         plottheta=2*K*(plotxL-(time/T));
         pSN,pCN,pDN,pPH = ellipj(plottheta,m);
         pCSD=pSN*pCN*pDN;
         
         ploteta =d*(A0+A1*pCN**2);
         plotuDat=sqrt(g*d)*(B00+B10*pCN**2);
         plotwDat=sqrt(g*d)*(4*K*d*pCSD/L)*((z+d)/d)*B10;
         

         self.K  = K  
         self.m  = m  
         self.A0 = A0 
         self.A1 = A1 
         self.B00= B00
         self.B10= B10
         self.L  = L  

         self.C  = C
         self.E  = E
         self.Ef = Ef
         self.Ur = Ur
         self.eta= eta
         self.u  = u
         self.w  = w
         self.dudt=dudt
         self.dwdt=dwdt
         self.pres=pres

         self.plotxL  =plotxL
         self.ploteta =ploteta
         self.plotuDat=plotuDat
         self.plotwDat=plotwDat


         formatString='%18s\t%10.2f'
         p=""
         p=p+'First Order Approximations\n'
         p=p+formatString%('Wavelength',L)+"\n";
         p=p+formatString%('Celerity',C)+"\n";
         p=p+formatString%('Energy density',E)+"\n";
         p=p+formatString%('Energy flux',Ef)+"\n";
         p=p+formatString%('Ursell number',Ur)+"\n";
         p=p+formatString%('Elevation',eta)+"\n";
         p=p+formatString%('Horz. velocity',u)+"\n";
         p=p+formatString%('Vert. velocity',w)+"\n";
         p=p+formatString%('Horz. acceleration',dudt)+"\n";
         p=p+formatString%('Vert. acceleration',dwdt)+"\n";
         p=p+formatString%('Pressure',pres)+"\n";
         self.descString=p
         
if __name__ == "__main__":
    # If run as a script, create an instance of DampedOsc, and print
    # some function values.
    osc = O1(H=9.8)
    #osc.H=9.8
