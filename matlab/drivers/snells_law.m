clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Lineat Wave Theory with Snell's Law (page 3-1 in ACES User's Guide)
% Provides a simple estimate for wave shoaling and refraction using Snell's
% Law with wave properties predicted by linear wave theory

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 11, 2011
% Date Verified: June 6, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK1
% ERRWAVBRK3
% LWTDWS
% LWTGEN
% LWTTWM
% LWTTWS
% ERRWAVBRK3
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   H1: wave height at known location (m)
%   T: wave period at known location (sec)
%   d1: water depth at known location (m)
%   alpha1: wave crest angle (deg)
%   cotphi: cotan of nearshore slope
%   d2: water depth at desired location (m)

%   OUTPUT
%   H0: deepwater wave height (m)
%   H2: wave height at subject location (m)
%   alpha0: deepwater wave crest angle (deg)
%   alpha2: wave crest angle at subject location (deg)
%   L0: deepwater wavelength (m)
%   L1: wavelength at known location (m)
%   L2: wavelength at subject location (m)
%   c1: wave celerity at known location (m/s)
%   c0: deepwater wave celerity (m/s)
%   c2: wave celerity at subject location (m/s)
%   cg1: group speed at known location (m/s)
%   cg0: deepwater group speed (m/s)
%   cg2: group speef at subject location (m/s)
%   E1: energy density at known location (N-m/m^2)
%   E0: deepwater energy density (N-m/m^2)
%   E2: enery density at subject location (N-m/m^2)
%   P1: energy flux at known location (N-m/m-s)
%   P0: deepwater wave flux (N-m/m-s)
%   P2: wave flux at subject location (N-m/m-s)
%   HL: deepwater wave steepness
%   Ur1: Ursell number at known location
%   Ur2: Ursell number at desired location
%   Hb: breaking wave height (m)
%   db: breaking wave depth (m)
%-------------------------------------------------------------

% Ask user if running windows or linux to set functions path
accepted = false;
while accepted == false
    linux=input('Linux or Windows? (l or w): ', 's');
    
    if strcmp('l', linux);
        accepted = true;
        linux=true;
    elseif strcmp('w', linux);
        accepted = true;
        linux=false;
    else
        fprintf('l or w only\n');
    end
end

% Ask user for single or multi-input (from a file)
accepted = false;
single_case = '';
while accepted == false
    single_case=input('Single or Multi-case? (s or m): ', 's');
    
    if strcmp('s',single_case);
        accepted = true;
        single_case=true;
    elseif strcmp('m', single_case);
        accepted = true;
        single_case=false;
    else
        fprintf('s or m only\n');
    end
end

% Single case input
if single_case
	prompt = 'Enter H1: wave height at known location (m): ';
	H1 = input(prompt);

	prompt = 'Enter T: wave period at known location (sec): ';
	T = input(prompt);

	prompt = 'Enter d1: water depth at known location (m): ';
	d1 = input(prompt);
    
    prompt = 'Enter alpha1: wave crest angle (deg): ';
	alpha1 = input(prompt);
    
    prompt = 'Enter cotphi: cotan of nearshore slope: ';
	cotphi = input(prompt);
    
    prompt = 'Enter d2: water depth at desired location (m): ';
	d2 = input(prompt);
    
else
    % TODO 
    % Default multi-case block. Eventually to be repalced with csv/tsv file
    % reader
    H1=10;
    T=7.50;
    d1=25;
    alpha1=10.0;
    cotphi=100;
    d2=20;
end

rho=1.989;
g=32.17;
m=1/cotphi;

[Hb]=ERRWAVBRK1(d1,0.78);
assert(H1<Hb,'Error: Known wave broken (Hb = %6.2f m)',Hb)

%determine known wave properties
[c1,c0,cg1,cg0,k1,L1,L0,reldep1]=LWTGEN(d1,T,g);
[E1,P1,Ur1,setdown1]=LWTTWM(cg1,d1,H1,L1,reldep1,rho,g,k1);

[steep,maxstp]=ERRSTP(H1,d1,L1);
assert(steep<maxstp,'Error: Known wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

%determine deepwater wave properties
[alpha0,H0]=LWTDWS(alpha1,c1,cg1,c0,H1);

E0=(1/8)*rho*g*(H0^2);
P0=E0*cg0;
HL=H0/L0;

assert(HL<(1/7),'Error: Deepwater wave unstable, [H0/L0] > (1/7)')

%determine subject wave properties
[c2,c0,cg2,cg0,k2,L2,L0,reldep2]=LWTGEN(d2,T,g);
[alpha2,H2,kr,ks]=LWTTWS(alpha0,c2,cg2,c0,H0);
[E2,P2,Ur2,setdown2]=LWTTWM(cg2,d2,H2,L2,reldep2,rho,g,k2);

[Hb,db]=ERRWAVBRK3(H0,L0,T,m);
assert(H2<Hb,'Error: Subject wave broken (Hb = %6.2f m, hb = %6.2f m)',Hb,db)

[steep,maxstp]=ERRSTP(H2,d2,L2);
assert(steep<maxstp,'Error: Subject wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

fprintf('\t\t\t\t\t %s \t\t %s \t\t %s \t\t\n','Known','Deepwater','Subject');
fprintf('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n','Wave height',H1,H0,H2)
fprintf('%s \t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n','Wave crest angle',alpha1,alpha0,alpha2)
fprintf('%s \t\t\t %-5.2f \t %-5.2f \t\t %-5.2f \t\t\n','Wavelength',L1,L0,L2)
fprintf('%s \t\t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n','Celerity',c1,c0,c2)
fprintf('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t\n','Group speed',cg1,cg0,cg2)
fprintf('%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t\n','Energy density',E1,E0,E2)
fprintf('%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t\n','Energy flux',P1,P0,P2)
fprintf('%s \t\t %-5.2f \t\t\t\t\t\t %-5.2f \n','Ursell number',Ur1,Ur2)
fprintf('%s \t\t\t\t\t %-5.2f \n','Wave steepness',HL)
fprintf('\n')
fprintf('%s \t\t\t\n','Breaking parameters')
fprintf('%s \t\t %-5.2f \t\n','Breaking height',Hb)
fprintf('%s \t\t\t %-5.2f \t\n','Breaking depth',db)
