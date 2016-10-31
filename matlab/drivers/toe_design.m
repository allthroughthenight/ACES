clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Toe Protection Design (page 4-2 in ACES User's Guide). 
% Determines armor stone size and width of a toe protection apron for
% vertical structures, such as seawalls, bulkheads, quay walls, breakwaters,
% and groins.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 13, 2011
% Date Verified: June 5, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   Hi: wave height (m)
%   T: wave period (sec)
%   ds: water depth at structure (m)
%   cotphi: cotangent of nearshore slope
%   Kp: passive earth pressure coefficient
%   de: sheet-pile penetration depth (m)
%   ht: height of toe protection layer above mudline
%   unitwt: unit weight of rock (N/m^3)

%   OUTPUT
%   width: width of toe protection apron (m)
%   w: weight of individual armor unit (N)
%   dt: water depth at top of toe protection layer (m)

%   OTHERS
%   H20weight: specific weight of water
%-------------------------------------------------------------

addpath('../functions'); % Path to functions folder

H=3;
T=14.1;
ds=20;
cotphi=500.0;
Kp=0;
de=0;
ht=5.50;
unitwt=105;

rho=1.989;
g=32.17;
H20weight=g*rho;

specgrav=unitwt/H20weight;

dl=ds-ht;
m=1/cotphi;

assert(ds/(T^2)>0.0037424,'Error: Limiting value detected...Hbs cannot be solved.')

[Hbs]=ERRWAVBRK2(T,m,ds);
assert(H<Hbs,'Error: Wave broken at structure (Hbs = %6.2f m)',Hbs)

[L,k]=WAVELEN(dl,T,50,g);

[steep,maxstp]=ERRSTP(H,dl,L);
assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

b1=de*Kp;
b2=2*H;
b3=0.4*ds;
b=cat(1,b1,b2,b3);
b=max(b);

arg1=(4*pi*dl/L);
kappa=(arg1/sinh(arg1))*((sin(2*pi*b/L))^2);
arg2=((1-kappa)/(kappa^(1/3)))*(dl/H);
Ns=1.3*arg2+1.8*exp(-1.5*(1-kappa)*arg2);

if Ns<1.8
    Ns=1.8;
end

w=(unitwt*(H^3))/((Ns^3)*((specgrav-1)^3));

fprintf('\t\t\t\t\t\t\t\t\t\t\t\t\n')
fprintf('%s \t\t\t\t\t %-6.2f \t\n','Width of toe apron',b)
fprintf('%s \t %-6.2f \t\n','Weight of individual armor unit',w)
fprintf('%s \t\t\t %-6.2f \t\n','Water depth at top of tow',dl)


