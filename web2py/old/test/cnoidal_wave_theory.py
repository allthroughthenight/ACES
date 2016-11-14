from numpy import pi, sqrt, array, arange
from  scipy.special import ellipk, ellipj
from ellipke import ellipke
from ERRWAVBRK1 import ERRWAVBRK1
from matplotlib.pyplot import *
#pi=numpy.pi;



H=10;
T=15.0;
d=25;
z=-12.50;
xL=0.5;
twopi=2*pi;
g=32.17;
rho=1.989; #%seawater set at 1025.09 kg/m^3, fresh set at 999.8 kg/m^3
time=0;
O=1;

epsi=H*1.0/d;

def F1(m):
    F=(16*m*ellipk(m)**2/3.0)-(g*H*T**2/d**2)
    return F

def F2(m):
    F=(16*m*ellipk(m)**2/3.0)-(g*H*T**2/d**2)*(1-epsi*((1+2*((1-m)/m))/4.0));
    return F

Hb =ERRWAVBRK1(d,0.78)
if (H>=Hb):
    print 'Error: Input wave broken (Hb = %6.2f m)'%Hb
    
#%% First Order Approximation
if (O==1): #determining m using bisection method
    a=1*10**-12;
    b=1-10**-12;
    F=F1
    while ((b-a)/2>=0.00001):
        xi=(a+b)/2;
        if (F(xi)==0):
            break
        else:
            if (F(xi)*F(b)<0):
                a=xi;
            elif (F(xi)*F(a)<0):
                b=xi;
    
    m=xi
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

    SN,CN,DN,PH = ellipj(theta,m);


    CSD=CN*SN*DN;
    
    A0=epsi*(lam-mu);
    A1=epsi;
    eta=d*(A0+A1*CN**2); #water surface elevation

    if any(~((z<eta) & ((z+d)>0))):
        print('Error: Point outside waveform.')
    
    E0=(-lam+2*mu+4*lam*mu-lam**2-3*mu**2)/3;
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
    
    P1=(1+2*lam-3*mu)/2;
    P0=3/2;
    Pb=rho*g*d*(P0+epsi*P1);
    pres=Pb-(rho/2)*((u-C)**2+w**2)-g*rho*(z+d); #pressure

    

    print('First Order Approximations')
    print('%s \t\t\t %-6.2f \t \n'%('Wavelength',L));
    print('%s \t\t\t %-6.2f \t \n'%('Celerity',C));
    print('%s \t\t %-8.2f \t \n'%('Energy density',E));
    print('%s \t\t %-8.2f \t \n'%('Energy flux',Ef));
    print('%s \t\t %-6.2f \n'%('Ursell number',Ur));
    print('%s \t\t\t %-6.2f \t \n'%('Elevation',eta));
    print('%s \t\t %-6.2f \t \n'%('Horz. velocity',u));
    print('%s \t\t %-6.2f \t \n'%('Vert. velocity',w));
    print('%s \t %-6.2f \t \n'%('Horz. acceleration',dudt));
    print('%s \t %-6.2f \t \n'%('Vert. acceleration',dwdt));
    print('%s \t\t\t %-8.2f \t \n'%('Pressure',pres));
    
    #Plotting waveform
    step=0.001
    plotxL=arange(-1,1+step,step);
    plottheta=2*K*(plotxL-(time/T));
    pSN,pCN,pDN,pPH = ellipj(plottheta,m);
    pCSD=pSN*pCN*pDN;
    
    ploteta=d*(A0+A1*pCN**2);
    plotu=sqrt(g*d)*(B00+B10*pCN**2);
    plotw=sqrt(g*d)*(4*K*d*pCSD/L)*((z+d)/d)*B10;
    
    
    subplot(3,1,1); 
    plot(plotxL,ploteta); 
    ylim(ymin=min(ploteta)-1,ymax=max(ploteta)+1)
    xmin, xmax = xlim()
    hline = plot([xmin,xmax],[0,0]);
    hline[0].set_color('red')
    hline[0].set_linestyle('--')
    ##set(hline,'Color','r','LineStyle','--')
    ylabel('Elevation [m]')
    
    subplot(3,1,2); 
    plot(plotxL,plotu); 
    ylim(ymin=min(plotu)-1,ymax=max(plotu)+1)
    #ylim([min(plotu)-1 max(plotu)+1])
    xmin, xmax = xlim()
    hline = plot([xmin,xmax],[0,0]);
    #hline = refline([0 0]);
    hline[0].set_color('red')
    hline[0].set_linestyle('--')
    #set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, u [m/s]')
    
    subplot(3,1,3); 
    plot(plotxL,plotw); 
    ylim(ymin=min(plotw)-1,ymax=max(plotw)+1)
    #ylim([min(plotw)-1 max(plotw)+1])
    #hline = refline([0 0]);
    xmin, xmax = xlim()
    hline = plot([xmin,xmax],[0,0]);
    hline[0].set_color('red')
    hline[0].set_linestyle('--')
    #set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, w [m/s]')
    xlabel('x/L')

#Second Order Approximations
elif (O==2): #%determining m using bisection method
    a=1e-12;
    b=1-10**-12;
    while ((b-a)/2>=0.00001):
        xi=(a+b)/2;
        if (F2(xi)==0):
            break
        else:
            if (F2(xi)*F2(b)<0):
                a=xi;
            elif (F2(xi)*F2(a)<0):
                b=xi;

    m=array([xi]);
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
    if (Ur>26):
        print('Error: Ursell parameter test failed.')

    A2=(3.0/4.0)*epsi**2;
    A1=epsi-A2;
    A0=epsi*(lam-mu)+epsi**2*((-2*lam+mu-2*lam**2+2*lam*mu)/4.0);
    eta=d*(A0+A1*CN**2+A2*CN**4); #%wave surface elevation

    if ((z<eta)&((z+d)>0)):
        print('Error: Point outside waveform.')

    E1=(1/30.0)*(lam-2*mu-17*lam*mu+3*lam**2-17*lam**2*mu+2*lam**3+15*mu**3);
    E0=(-lam+2*mu+4*lam*mu-lam**2-3*mu**2)/3.0;
    E =rho*g*H**2*(E0+epsi*E1); ##%average energy density

    f1=(1/30.0)*(-4*lam+8*mu+53*lam*mu-12*lam**2-60*mu**2+53*lam**2*mu-120*lam*mu**2 -8*lam**3+75*mu**3);
    
    f0=E0;
    Ef=rho*g*H**2*sqrt(g*d)*(f0+epsi*f1); ##%energy flux
    
    term=(z+d)/d;

    B21=-(9/2)*epsi**2;
    B11=3*epsi**2*(1-lam);
    B01=((3*lam)/2)*epsi**2;
    B20=-(epsi**2);

    B10=epsi+epsi**2*((1-6*lam+2*mu)/4);
    B00=epsi*(lam-mu)+epsi**2*((lam-mu-2*lam**2+2*mu**2)/4);
    u=sqrt(g*d)*((B00+B10*CN**2+B20*CN**4)-(1/2)*term**2*(B01+B11*CN**2+B21*CN**4)); ##%horizontal velocity
    
    w1=term*(B10+2*B20*CN**2);
    w2=(1/6)*term**3*(B11+2*B21*CN**2);
    w=sqrt(g*d)*(4*K*d*CSD/L)*(w1-w2); ##%vertical velocity

    u1=(B10-(1/2)*term**2*B11)*(4*K*CSD/T);
    u2=(B20-(1/2)*term**2*B21)*(8*K*CN**2*CSD/T);
    dudt=sqrt(g*d)*(u1+u2); #%horizontal acceleration

    w1=(8*K*CSD**2/T)*(term*B20-(1/6)*term**3*B21);
    w2=term*(B10+2*B20*CN**2)-(1/6)*term**3*(B11+2*B21*CN**2);
    w3=(2*K/T)*((SN*DN)**2-(CN*DN)**2+(m*SN*CN)**2);
    dwdt=sqrt(g*d)*(4*K*d/L)*(w1+w2*w3); #%vertical acceleration

    P2=(-1-16*lam+15*mu-16*lam**2+30*lam*mu)/40;
    P1=(1+2*lam-3*mu)/2;
    P0=3/2.0;
    Pb=rho*g*d*(P0+epsi*P1+epsi**2*P2);
    pres=Pb-(rho/2)*((u-C)**2+w**2)-g*rho*(z+d);

    print('Second Order Approximations')
    print('%s \t\t\t %-6.2f \t \n'%('Wavelength',L));
    print('%s \t\t\t %-6.2f \t \n'%('Celerity',C));
    print('%s \t\t %-8.2f \t \n'%('Energy density',E));
    print('%s \t\t %-8.2f \t \n'%('Energy flux',Ef));
    print('%s \t\t %-6.2f \n'%('Ursell number',Ur));
    print('%s \t\t\t %-6.2f \t \n'%('Elevation',eta));
    print('%s \t\t %-6.2f \t \n'%('Horz. velocity',u));
    print('%s \t\t %-6.2f \t \n'%('Vert. velocity',w));
    print('%s \t %-6.2f \t \n'%('Horz. acceleration',dudt));
    print('%s \t %-6.2f \t \n'%('Vert. acceleration',dwdt));
    print('%s \t\t\t %-8.2f \t \n'%('Pressure',pres));

    #%Plotting waveform
    step=0.001
    plotxL=arange(-1,1+step,step);
    plottheta=2*K*(plotxL-(time/T));
    pSN,pCN,pDN,pPH = ellipj(plottheta,m);
    pCSD=pSN*pCN*pDN;

    ploteta=d*(A0+A1*pCN**2+A2*pCN**4);
    plotu=sqrt(g*d)*((B00+B10*pCN**2+B20*pCN**4)-(1/2)*((z+d)/d)**2*(B01+B11*pCN**2+B21*pCN**4));

    pw1=((z+d)/d)*(B10+2*B20*pCN**2);
    pw2=(1/6.0)*(((z+d)/d)**3)*(B11+2*B21*pCN**2);
    plotw=sqrt(g*d)*(4*K*d*pCSD/L)*(pw1-pw2);

    subplot(3,1,1); 
    plot(plotxL,ploteta); 
    ylim(ymin=min(ploteta)-1,ymax=max(ploteta)+1) #ylim([min(ploteta)-1 max(ploteta)+1])
    xmin,xmax=xlim()
    hline = plot([xmin,xmax],[0,0]);
    hline[0].set_color('red')
    hline[0].set_linestyle('--')
    #set(hline,'Color','r','LineStyle','--')
    ylabel('Elevation [m]')
    
    subplot(3,1,2); 
    plot(plotxL,plotu); 
    ylim(ymin=min(plotu)-1,ymax=max(plotu)+1)
    #ylim([min(plotu)-1 max(plotu)+1])
    xmin, xmax = xlim()
    hline = plot([xmin,xmax],[0,0]);
    #hline = refline([0 0]);
    hline[0].set_color('red')
    hline[0].set_linestyle('--')
    #set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, u [m/s]')
    
    subplot(3,1,3); 
    plot(plotxL,plotw); 
    ylim(ymin=min(plotw)-1,ymax=max(plotw)+1)
    #ylim([min(plotw)-1 max(plotw)+1])
    #hline = refline([0 0]);
    xmin, xmax = xlim()
    hline = plot([xmin,xmax],[0,0]);
    hline[0].set_color('red')
    hline[0].set_linestyle('--')
    #set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, w [m/s]')
    xlabel('x/L')
