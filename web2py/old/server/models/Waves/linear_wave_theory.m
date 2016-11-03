##clear all
##clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Linear Wave Theory (page 2-1 in ACES User''s Guide)
% Yields first-order approximations for various wave parameters of wave
% motion as predicted by linear wave theory

% Transferred by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: March 17, 2011
% Date Modified: 

% Requires the following functions:
% ERRWAVBRK1
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   H: wave height (m)
%   T: wave period (sec)
%   d: water depth (m)
%   z: vertical coordinate (m)
%   xL: horizontal coordinate as fraction of wavelength (x/L)

%   OUTPUT    
%   L: wavelength (m)
%   C: wave celerity (m/sec)
%   Cg: group celerity (m/sec)
%   E: energy density (N-m/m^2)
%   Ef: energy flux (N-m/sec-m)
%   Ur: Ursell number
%   eta: surface elevation (m)
%   px: horizontal particle displacement (m)
%   pz: vertical particle displacement (m)
%   u: horizontal particle velocity (m/sec)
%   w: vertical particle velocity (m/sec)
%   dudt: horizontal particle acceleration (m/sec^2)
%   dwdt: vertical particle accleration (m/sec^2)
%   pres: pressure (N/m^2)
%-------------------------------------------------------------
g=9.81;
varList={"H", "T",  "d", "z", "xL", "twopi", "rho" };
varVals={0.85, 3.0, 4.1, 0.2, 0.0,  2*pi,    1025};
for k=1:length(varList)
  vark=varList{1,k};
  valk=varVals{1,k};
  if !exist(vark,"var")
    eval(sprintf("%s=%f;",vark,valk));
  endif
endfor
##T=3; 
##d=4.1;
##z=0.2; 
##xL=0.0; 
##twopi=2*pi; 
##rho=1025; %kg/m^3 (sea water)
addpath('applications/ACES/models/Waves/')
[L,k]=WAVELEN(d,T,50,g);

theta=xL*twopi; %theta=(kx-wt) where arbitrarily t=0 and k=2*pi/L

% Check for monochromatic wave breaking (depth limited - no slope)
[Hb]=ERRWAVBRK1(d,0.78);
if H<Hb
  assert(H<Hb,"Error: Input wave broken (Hb = %6.2f m)",Hb)
endif;

				% Check to make sure vertical coordinate is within waveform
eta=(H/2)*cos(theta);
if (z<eta && (z+d)>0)
  assert(z<eta && (z+d)>0,'Error: Point outside waveform.')
endif

% Main Computations
arg=(2*k*d/(sinh(2*k*d)));
tot=d+z;

C=L/T;
Cg=0.5*(1+arg)*C;
E=(1/8)*rho*g*(H^2);
Ef=E*Cg;
Ur=L^2*H/(d^3);
px=(-H/2)*(cosh(k*tot)/sinh(k*d))*sin(theta); 
py=(H/2)*(sinh(k*tot)/sinh(k*d))*cos(theta);
u=(H*pi/T)*(cosh(k*tot)/sinh(k*d))*cos(theta); 
w=(H*pi/T)*(sinh(k*tot)/sinh(k*d))*sin(theta);
dudt=(H*2*pi^2/(T^2))*(cosh(k*tot)/sinh(k*d))*sin(theta);
dwdt=(-H*2*pi^2/(T^2))*(sinh(k*tot)/sinh(k*d))*cos(theta); 
pres=-rho*g*z+rho*g*(H/2)*(cosh(k*tot)/cosh(k*d))*cos(theta);

fprintf('\t\t\t\t\t\t\t\t %s \n','Units');
fprintf('%s \t\t\t %-6.2f \t %s \n','Wavelength',L,'m');
fprintf('%s \t\t\t %-6.2f \t %s \n','Celerity',C,'m/s');
fprintf('%s \t\t %-6.2f \t %s \n','Group speed',Cg,'m/s');
fprintf('%s \t\t %-8.2f \t %s \n','Energy density',E,'N-m/m^2');
fprintf('%s \t\t %-8.2f \t %s \n','Energy flux',Ef,'N-m/m-s');
fprintf('%s \t\t %-6.2f \n','Ursell number',Ur);
fprintf('%s \t\t\t %-6.2f \t %s \n','Elevation',eta,'m');
fprintf('%s \t %-6.2f \t %s \n','Horz. displacement',px,'m');
fprintf('%s \t %-6.2f \t %s \n','Vert. displacement',py,'m');
fprintf('%s \t\t %-6.2f \t %s \n','Horz. velocity',u,'m/s');
fprintf('%s \t\t %-6.2f \t %s \n','Horz. velocity',w,'m/s');
fprintf('%s \t %-6.2f \t %s \n','Horz. acceleration',dudt,'m/s^2');
fprintf('%s \t %-6.2f \t %s \n','Vert. acceleration',dwdt,'m/s^2');
fprintf('%s \t\t\t %-8.2f \t %s \n','Pressure',pres,'N/m^2');

%Plotting waveform
plotxL=(-1:0.001:1);
plottheta=plotxL*twopi;

ploteta=(H/2)*cos(plottheta);
plotu=(H*pi/T)*(cosh(k*tot)/sinh(k*d))*cos(plottheta);
plotw=(H*pi/T)*(sinh(k*tot)/sinh(k*d))*sin(plottheta);

figure(1)
subplot(3,1,1); plot(plotxL,ploteta); ylim([min(ploteta)-1 max(ploteta)+1])
hline = refline([0 0]);
set(hline,'Color','r','LineStyle','--')
ylabel('Elevation [m]')
    
subplot(3,1,2); plot(plotxL,plotu); ylim([min(plotu)-1 max(plotu)+1])
hline = refline([0 0]);
set(hline,'Color','r','LineStyle','--')
ylabel('Velocity, u [m/s]')
  
subplot(3,1,3); plot(plotxL,plotw); ylim([min(plotw)-1 max(plotw)+1])
hline = refline([0 0]);
set(hline,'Color','r','LineStyle','--')
ylabel('Velocity, w [m/s]')
xlabel('x/L')

print(gcf,'applications/ACES/static/images/Waves.svg','-dsvg')




    
