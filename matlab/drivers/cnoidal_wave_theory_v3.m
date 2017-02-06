clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Cnoidal Wave Theory (page 2-2 in ACES User's Guide)
% Yields first-order and second-order approximations for various wave
% parameters of wave motion as predicted by cnoidal wave theory

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: March 18, 2011
% Date Modified:7/21/16 -yaprak

% Requires the following functions:
% ERRWAVBRK1

% MAIN VARIABLE LIST:
%   INPUT
%   H: wave height (m)
%   T: wave period (sec)
%   d: water depth (m)
%   z: vertical coordinate (m)
%   xL: horizontal coordinate as fraction of wavelength (x/L)
%   time: time-coordinate (default=0)
%   O: order approximation (1 or 2)

%   OUTPUT
%   L: wavelength (m)
%   C: wave celerity (m/s)
%   E: energy density (N-m/m^2)
%   Ef: energy flux (N-m/m-s)
%   Ur: Ursell number
%   eta: surface elevation (m)
%   u: horizontal particle velocity (m/s)
%   w: vertical particle velocity (m/s)
%   dudt: horizontal particle acceleration (m/s^2)
%   dwdt: vertical particle accleration (m/s^2)
%   pres: pressure (N/m^2)

%   OTHERS
%   K: complete elliptic intergral of the first kind
%   E: complete elliptical intergral of the second kind
%   m: optimized parameter
%   lambda: simplification term ((1-m)/m)
%   mu: simplification term (E/(K*m))
%   epsi: perturbation parameter (H/d)
%-------------------------------------------------------------

addpath('../functions'); % Path to functions folder

H=10;
T=15.0;
d=25;
z=-12.5;
xL=0.5;
time=0;
O=2;
unitSystem = 'I'; % Use M for metric system and I for imperial
water = 'S'; % Use S for seawater and F for freshwater

%% *********** Don't change anything here ******************
% Unit system conversion Constants
twopi=2*pi;
if unitSystem == 'I'; % imperial
    g=32.17; % gravitational acceleration (ft/sec^2)
    if water == 'S';
    rho=1.989; % rho/g = 63.99/32.17 lb sec^2/ft^4 (sea water)
    else rho = 1.940; % rho/g = 62.415475/32.17 lb sec^2/ft^4 (fresh water)
    end
   % rho=1.989; %seawater set at 1025.09 kg/m^3, fresh set at 999.8 kg/m^3
else  unitSystem == 'M'; % metric
    g = 9.81; % kg/sec^2
    if water == 'S';
    rho = 1025.09; % kg/m^3, (sea water)
    else rho = 999.8; % kg/m^3 ( fresh water)
    end
end

epsi=H/d;

[Hb]=ERRWAVBRK1(d,0.78);
assert(H<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)


%% First Order Approximation
if O==1 %determining m using bisection method
    a=1*10^-12;
    b=1-10^-12;
    F=@(m)(16*m*ellipke(m)^2/3)-(g*H*T^2/d^2);
    while (b-a)/2>=0.00001
        xi=(a+b)/2;
        if F(xi)==0
            break
        else
            if F(xi)*F(b)<0
                a=xi;
            elseif F(xi)*F(a)<0
                b=xi;
            end
        end
    end
    m=xi;

    [K,E]=ellipke(m);

    lambda=(1-m)/m;
    mu=E/(m*K);
    theta=2*K*(xL-(time/T));

    C0=1;
    C1=(1+2*lambda-3*mu)/2;
    C=sqrt(g*d)*(C0+epsi*C1); %celerity

    L=C*T; %wave length

    Ur=(H*(L^2))/(d^3);
    assert(Ur>26,'Error: Ursell parameter test failed.')

    [SN,CN,DN] = ellipj(theta,m);
    CSD=CN*SN*DN;

    A0=epsi*(lambda-mu);
    A1=epsi;
    eta=d*(A0+A1*CN^2); %water surface elevation

    assert(z<eta && (z+d)>0,'Error: Point outside waveform.')

    E0=(-lambda+2*mu+4*lambda*mu-lambda^2-3*mu^2)/3;
    E=rho*g*H^2*E0; %average energy density

    F0=E0;
    Ef=rho*g*H^2*sqrt(g*d)*F0; %energy flux

    B00=epsi*(lambda-mu);
    B10=epsi;
    u=sqrt(g*d)*(B00+B10*CN^2); %horizontal velocity

    w=sqrt(g*d)*(4*K*d*CSD/L)*((z+d)/d)*B10; %vertical velocity

    dudt=sqrt(g*d)*B10*(4*K/T)*CSD; %horizontal acceleration

    term=sqrt(g*d)*(4*K*d/L)*((z+d)/d)*B10*(2*K/T);
    dwdt=term*((SN*DN)^2-(CN*DN)^2+(m*SN*CN)^2); %vertical acceleration

    P1=(1+2*lambda-3*mu)/2;
    P0=3/2;
    Pb=rho*g*d*(P0+epsi*P1);
    pres=Pb-(rho/2)*((u-C)^2+w^2)-g*rho*(z+d); %pressure

    disp('First Order Approximations')
    fprintf('%s \t\t\t %-6.2f \t \n','Wavelength',L);
    fprintf('%s \t\t\t %-6.2f \t \n','Celerity',C);
    fprintf('%s \t\t %-8.2f \t \n','Energy density',E);
    fprintf('%s \t\t %-8.2f \t \n','Energy flux',Ef);
    fprintf('%s \t\t %-6.2f \n','Ursell number',Ur);
    fprintf('%s \t\t\t %-6.2f \t \n','Elevation',eta);
    fprintf('%s \t\t %-6.2f \t \n','Horz. velocity',u);
    fprintf('%s \t\t %-6.2f \t \n','Vert. velocity',w);
    fprintf('%s \t %-6.2f \t \n','Horz. acceleration',dudt);
    fprintf('%s \t %-6.2f \t \n','Vert. acceleration',dwdt);
    fprintf('%s \t\t\t %-8.2f \t \n','Pressure',pres);

    %Plotting waveform
    plotxL=(-1:0.001:1);
    plottheta=2*K*(plotxL-(time/T));
    [pSN,pCN,pDN] = ellipj(plottheta,m);
    pCSD=pSN.*pCN.*pDN;

    ploteta=d*(A0+A1*pCN.^2);
    plotu=sqrt(g*d)*(B00+B10*pCN.^2);
    plotw=sqrt(g*d)*(4*K*d*pCSD/L)*((z+d)/d)*B10;

    subplot(3,1,1); plot(plotxL,ploteta); ylim([min(ploteta)-1 max(ploteta)+1])
    hline = refline_v2([0 0]);
    set(hline,'Color','r','LineStyle','--')
    ylabel('Elevation [m]')

    subplot(3,1,2); plot(plotxL,plotu); ylim([min(plotu)-1 max(plotu)+1])
    hline = refline_v2([0 0]);
    set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, u [m/s]')

    subplot(3,1,3); plot(plotxL,plotw); ylim([min(plotw)-1 max(plotw)+1])
    hline = refline_v2([0 0]);
    set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, w [m/s]')
    xlabel('x/L')

    % Second Order Approximations
elseif O==2 %determining m using bisection method
    a=1*10^-12;
    b=1-10^-12;
    F=@(m)(16*m*ellipke(m)^2/3)-(g*H*T^2/d^2)*(1-epsi*((1+2*((1-m)/m))/4));
    while (b-a)/2>=0.00001
        xi=(a+b)/2;
        if F(xi)==0
            break
        else
            if F(xi)*F(b)<0
                a=xi;
            elseif F(xi)*F(a)<0
                b=xi;
            end
        end
    end
    m=xi;
    [K,E]=ellipke(m);
    lambda=(1-m)/m;
    mu=E/(m*K);

    theta=2*K*(xL-(time/T));
    [SN,CN,DN] = ellipj(theta,m);
    CSD=CN*SN*DN;

    C2=(-6-16*lambda+5*mu-16*lambda^2+10*lambda*mu+15*mu^2)/40;
    C1=(1+2*lambda-3*mu)/2;
    C0=1;
    C=sqrt(g*d)*(C0+epsi*C1+epsi^2*C2); %celerity

    L=C*T; %wave length

    Ur=(H*(L^2))/(d^3);
    assert(Ur>26,'Error: Ursell parameter test failed.')

    A2=(3/4)*epsi^2;
    A1=epsi-A2;
    A0=epsi*(lambda-mu)+epsi^2*((-2*lambda+mu-2*lambda^2+2*lambda*mu)/4);
    eta=d*(A0+A1*CN^2+A2*CN^4); %wave surface elevation

    assert(z<eta && (z+d)>0,'Error: Point outside waveform.')

    E1=(1/30)*(lambda-2*mu-17*lambda*mu+3*lambda^2-17*lambda^2*mu+2*lambda^3+15*mu^3);
    E0=(-lambda+2*mu+4*lambda*mu-lambda^2-3*mu^2)/3;
    E=rho*g*H^2*(E0+epsi*E1); %average energy density

    F1=(1/30)*(-4*lambda+8*mu+53*lambda*mu-12*lambda^2-60*mu^2+53*lambda^2*mu-120*lambda*mu^2 ...
        -8*lambda^3+75*mu^3);
    F0=E0;
    Ef=rho*g*H^2*sqrt(g*d)*(F0+epsi*F1); %energy flux

    term=(z+d)/d;

    B21=-(9/2)*epsi^2;
    B11=3*epsi^2*(1-lambda);
    B01=((3*lambda)/2)*epsi^2;
    B20=-(epsi^2);
    B10=epsi+epsi^2*((1-6*lambda+2*mu)/4);
    B00=epsi*(lambda-mu)+epsi^2*((lambda-mu-2*lambda^2+2*mu^2)/4);
    u=sqrt(g*d)*((B00+B10*CN^2+B20*CN^4)-(1/2)*term^2*(B01+B11*CN^2+B21*CN^4)); %horizontal velocity

    w1=term*(B10+2*B20*CN^2);
    w2=(1/6)*term^3*(B11+2*B21*CN^2);
    w=sqrt(g*d)*(4*K*d*CSD/L)*(w1-w2); %vertical velocity

    u1=(B10-(1/2)*term^2*B11)*(4*K*CSD/T);
    u2=(B20-(1/2)*term^2*B21)*(8*K*CN^2*CSD/T);
    dudt=sqrt(g*d)*(u1+u2); %horizontal acceleration

    w1=(8*K*CSD^2/T)*(term*B20-(1/6)*term^3*B21);
    w2=term*(B10+2*B20*CN^2)-(1/6)*term^3*(B11+2*B21*CN^2);
    w3=(2*K/T)*((SN*DN)^2-(CN*DN)^2+(m*SN*CN)^2);
    dwdt=sqrt(g*d)*(4*K*d/L)*(w1+w2*w3); %vertical acceleration

    P2=(-1-16*lambda+15*mu-16*lambda^2+30*lambda*mu)/40;
    P1=(1+2*lambda-3*mu)/2;
    P0=3/2;
    Pb=rho*g*d*(P0+epsi*P1+epsi^2*P2);
    pres=Pb-(rho/2)*((u-C)^2+w^2)-g*rho*(z+d);

    disp('Second Order Approximations')
    fprintf('%s \t\t\t %-6.2f \t \n','Wavelength',L);
    fprintf('%s \t\t\t %-6.2f \t \n','Celerity',C');
    fprintf('%s \t\t %-8.2f \t \n','Energy density',E);
    fprintf('%s \t\t %-8.2f \t \n','Energy flux',Ef);
    fprintf('%s \t\t %-6.2f \n','Ursell number',Ur);
    fprintf('%s \t\t\t %-6.2f \t \n','Elevation',eta);
    fprintf('%s \t\t %-6.2f \t \n','Horz. velocity',u);
    fprintf('%s \t\t %-6.2f \t \n','Vert. velocity',w);
    fprintf('%s \t %-6.2f \t \n','Horz. acceleration',dudt);
    fprintf('%s \t %-6.2f \t \n','Vert. acceleration',dwdt);
    fprintf('%s \t\t\t %-8.2f \t \n','Pressure',pres);

    %Plotting waveform
    plotxL=(-1:0.001:1);
    plottheta=2*K*(plotxL-(time/T));
    [pSN,pCN,pDN] = ellipj(plottheta,m);
    pCSD=pSN.*pCN.*pDN;

    ploteta=d*(A0+A1*pCN.^2+A2*pCN.^4);
    plotu=sqrt(g*d)*((B00+B10*pCN.^2+B20*pCN.^4)-(1/2)*((z+d)/d)^2*(B01+B11*pCN.^2+B21*pCN.^4));

    pw1=((z+d)/d)*(B10+2*B20*pCN.^2);
    pw2=(1/6)*(((z+d)/d)^3)*(B11+2*B21*pCN.^2);
    plotw=sqrt(g*d)*(4*K*d*pCSD/L).*(pw1-pw2);

    subplot(3,1,1); plot(plotxL,ploteta); ylim([min(ploteta)-1 max(ploteta)+1])
    hline = refline_v2([0 0]);
    set(hline,'Color','r','LineStyle','--')
    ylabel('Elevation [m]')

    subplot(3,1,2); plot(plotxL,plotu); ylim([min(plotu)-1 max(plotu)+1])
    hline = refline_v2([0 0]);
    set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, u [m/s]')

    subplot(3,1,3); plot(plotxL,plotw); ylim([min(plotw)-1 max(plotw)+1])
    hline = refline_v2([0 0]);
    set(hline,'Color','r','LineStyle','--')
    ylabel('Velocity, w [m/s]')
    xlabel('x/L')
end
% %
% %
% %
% %
% %
% %
% %
% %
% %
% %
% % %
% % %
% % % % % ST=0.0;
% % % % % epsi=H/d;
% % % % % alpha=(3.0*g*H*(T^2))/(16*d^2);
% % % % % cons=(4.0*alpha)/(pi^2);
% % % % % A=16.0/64.0;
% % % % % B=-cons/64.0;
% % % % % rad=sqrt(((B^2)/4.0)+((A^3)/27.0));
% % % % % B2=-(B/2.0);
% % % % % BA=abs(B2+rad)^(1.0/3.0);
% % % % % BB=abs(B2-rad)^(1.0/3.0);
% % % % %
% % % % % if (B2+rad)>0
% % % % %     BA=abs(BA)*1;
% % % % % else
% % % % %     BA=abs(BA)*-1;
% % % % % end
% % % % %
% % % % % if (B2-rad)>0
% % % % %     BB=abs(BB)*1;
% % % % % else
% % % % %     BB=abs(BB)*-1;
% % % % % end
% % % % %
% % % % % Q=BA+BB;
% % % % %
% % % % % if Q>1.0
% % % % %     Q=0.99;
% % % % % end
% % % % %
% % % % % theta2p=1.0;
% % % % % gamma=0.0;
% % % % % j=0;
% % % % % diff1=999;
% % % % % diff2=999;
% % % % % while diff1~=0 && diff2~=0
% % % % %     j=j+1;
% % % % %     ip2=j*j+j;
% % % % %     TNP=theta2p+(Q^ip2);
% % % % %     GN=gamma+ip2*(Q^(ip2-1));
% % % % %     diff1=abs(theta2p-TNP);
% % % % %     diff2=abs(gamma-GN);
% % % % %     theta2p=TNP;
% % % % %     gamma=GN;
% % % % % end
% % % % %
% % % % % i=0;
% % % % % F=999;
% % % % % while abs(F)>(1*10^(-15))
% % % % % theta2=theta2p*2.0*(Q^0.25);
% % % % % SG=((pi^2)/4.0)*(theta2^4);
% % % % % F=1.0-(SG/alpha);
% % % % % DGDQ=4.0*(pi^2)*((theta2p^4)+(4.0*Q*gamma*(theta2p^3)));
% % % % % DFDQ=-(DGDQ/alpha);
% % % % % H1=-(F/DFDQ);
% % % % % Q=Q+H1;
% % % % % i=i+1;
% % % % % end
% % % % %
% % % % % T03=1.0;
% % % % % T02=1.0;
% % % % % SR=0.0;
% % % % % T04=1.0;
% % % % % SGN=-1.0;
% % % % %
% % % % %
% % % % i=0;
% % % % diff1=999;
% % % % diff2=999;
% % % % diff3=999;
% % % % diff4=999;
% % % % while diff1~=0 && diff2~=0 && diff3~=0 && diff4~=0
% % % % i=i+1;
% % % % ip1=i*i+i;
% % % % ip2=i*i;
% % % ip3=2*i;
% % % TN2=T02+(Q^ip1);
% % % TN3=T03+2.0*(Q^ip2);
% % % TN4=T04+SGN*2.0*(Q^ip2);
% % % SRN=SR+((Q^ip3)/((1.0-(Q^ip3))^2));
% % % SGN=SGN*(-1.0);
% % % diff1=abs(T02-TN2);
% % % diff2=abs(T03-TN3);
% % % diff3=abs(SR-SRN);
% % % diff4=abs(T04-TN4);
% % % T02=TN2;
% % % T03=TN3;
% % % T04=TN4;
% % % SR=SRN;
% % % end
% % % T02=2.0*(Q^0.25)*T02;
% % % SR=(1.0/12.0)-2.0*SR;
% % %
% % % SM=(T02^2)/(T03^2);
% % % BK=(pi/2.0)*(T03^2);
% % % SMP=(T04^2)/(T03^2);
% % % LAMBDA_old=(T04^4)/(T02^4);
% % % BE=((1.0+(SMP^2))/3.0)*BK+((pi^2)/BK)*SR;
% % % MU_old=BE/(SM*SM*BK);
% % % TM1=(1.0+2.0*LAMBDA_old-3.0*MU_old)/2.0;
% % % C_old=sqrt(g*d)*(1.0+epsi*TM1);
% % % L_old=C_old*T;
% % % Ur_old=(H*(L_old^2))/(d^3);
% % % theta_old=(xL-(time/T))*2.0*BK;
% % %
% %
% %
% %
% %
% %
% %
