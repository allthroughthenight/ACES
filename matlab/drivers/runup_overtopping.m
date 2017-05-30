clear all
clc

%check for option 3, vert wall
%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Wave Runup and Overtopping on Impermeable Structures (page 5-2
% in ACES User's Guide). Provides estimates of wave runup and overtopping
% on rough and smooth slope structures that are assumed to be impermeable

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 18, 2011
% Date Verified: June 6, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK2
% LWTDWS
% LWTGEN
% QOVERT
% QOVERT_IRR
% RUNUPR
% RUNUPS
% WAVELEN

% MAIN VARIABLE LIST:
%   MANDATORY INPUT
%   H: incident wave height (Hs for irregular waves)
%   T: wave period (Tp for irregular waves)
%   cotphi: cotan of nearshore slope
%   ds: water depth at structure toe
%   cottheta: cotan of structure slope (0.0 for vertical walls)
%   hs: structure height above toe 

%   OPTIONAL INPUT
%   a: empirical coefficient for rough slope runup
%   b: empirical coefficeint for rough slope runup
%   alpha: empirical coefficient for overtopping
%   Qstar0: empiricial coefficient for overtopping
%   U: onshore wind velocity for overtoppping
%   R: wave runup (if known)

%   MANDATORY OUTPUT
%   H0: deepwater wave height
%   relht0: deepwater realtive height (d/H)
%   steep0: deepwater wave steepness

%   OPTIONAL OUTPUT
%   R: wave runup
%   Q: overtopping

%   OTHERS
%   freeb: freeboard
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

if single_case
    [H] = USER_INPUT_DATA_VALUE(['Enter H: incident wave height (Hs for irregular waves) (' labelUnitDist '): '], 0.1, 100.0);
    
    [T] = USER_INPUT_DATA_VALUE(['Enter T: wave period (Tp for irregular waves) (' labelUnitDist '): '], 1.0, 1000.0);
    
    [cotphi] = USER_INPUT_DATA_VALUE('Enter cotphi: cotan of nearshore slope: ', 5.0, 10000.0);
    
    [ds] = USER_INPUT_DATA_VALUE(['Enter ds: water depth at structure toe (' labelUnitDist '): '], 0.1, 200.0);
    
    [cottheta] = USER_INPUT_DATA_VALUE('Enter cottheta: cotan of structure slope (0.0 for vertical walls): ', 0.0, 30.0);
    
    [hs] = USER_INPUT_DATA_VALUE(['Enter hs: structure height above toe (' labelUnitDist '): '], 0.0, 200.0);
else
    H=7.5;
    T=10.0;
    cotphi=100.0;
    ds=12.50;
    cottheta=3.0;
    hs=20.00;
end

m=1/cotphi;

fprintf('%s \n\n','Calculation and slope type options: ');
fprintf('%s \n','Monochromatic Waves')
fprintf('%s \n','[1] Rough <------------- Runup -------------> [2] Smooth')
fprintf('%s \n','[3] Rough <----------- Overtopping ---------> [4] Smooth')
fprintf('%s \n\n','[5] Rough <----- Runup and Overtopping -----> [6] Smooth')
fprintf('%s \n','Irregular Waves')
fprintf('%s \n\n','[7] Rough <----- Runup and Overtopping -----> [8] Smooth')

option=input('Select option: ');
fprintf('\n')

assert(ds<hs,'Error: Method does not apply to submerged structures.')

[Hbs]=ERRWAVBRK2(T,m,ds);
assert(H<Hbs,'Error: Wave broken at structure (Hbs = %6.2f %s)',Hbs,labelUnitDist)

[c,c0,cg,cg0,k,L,L0,reldep]=LWTGEN(ds,T,g);

[steep,maxstp]=ERRSTP(H,ds,L);
assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

[alpha0,H0]=LWTDWS(0,c,cg,c0,H);

relht0=ds/H0;
steep0=H0/(g*T^2);

if cottheta==0
    assert(option~=1 && option~=5 && option~=7,'Error: Vertical wall cannot have rough slope.')
    theta=0.5*pi;
    ssp=1000;
else
    theta=atan(1/cottheta);
    ssp=(1/cottheta)/sqrt(H/L0);
end

fprintf('%s \n','Deepwater')
fprintf('\t %s \t\t %-6.3f %s \n','Wave height',H0,labelUnitDist)
fprintf('\t %s \t %-6.3f \n','Relative height',relht0)
fprintf('\t %s \t %-6.6f \n\n','Wave steepness',steep0)

freeb=hs-ds;

if option==1 || option==5 || option ==7 || option==8
    %Empirical coefficients for rough slope runup
    a=0.956;
    b=0.398;
end

if option>2
    %Empirical coefficients and values for overtopping
    alpha=0.076463;
    Qstar0=0.025;
    U=35.0*1.15077945; %1 knots = 1.15077945 mph
    if option==3
        R=15.0;
    elseif option==4
        R=20.0;
    end
end

if option==1
    [R]=RUNUPR(H,ssp,a,b);
    fprintf('%s \t\t\t\t\t %-6.3f %s \n','Runup',R,labelUnitDist)
elseif option==2
    [R]=RUNUPS(H,L,ds,theta,ssp);
    fprintf('%s \t\t\t\t\t %-6.3f %s \n','Runup',R,labelUnitDist)
elseif option==3   
    [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
    fprintf('%s \t %-6.3f %s^3/sec-%s \n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
elseif option==4
    [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
    fprintf('%s \t %-6.3f %s^3/sec-%s \n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
elseif option==5
    [R]=RUNUPR(H,ssp,a,b);
    [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
    fprintf('%s \t\t\t\t\t %-6.3f %s \n','Runup',R,labelUnitDist)
    fprintf('%s \t %-6.3f %s^3/sec-%s \n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
elseif option==6
    [R]=RUNUPS(H,L,ds,theta,ssp);
    [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
    fprintf('%s \t\t\t\t\t %-6.3f %s \n','Runup',R,labelUnitDist)
    fprintf('%s \t %-6.3f %s^3/sec-%s \n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
elseif option==7
    [R]=RUNUPR(H,ssp,a,b);
    [Q]=QOVERT_IRR(H0,freeb,R,Qstar0,alpha,theta,U,g);
    fprintf('%s \t\t\t\t\t %-6.3f %s \n','Runup',R,labelUnitDist)
    fprintf('%s \t %-6.3f %s^3/sec-%s \n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
elseif option==8
    [R]=RUNUPS(H,L,ds,theta,ssp);
    [Q]=QOVERT_IRR(H0,freeb,R,Qstar0,alpha,theta,U,g);
    fprintf('%s \t\t\t\t\t %-6.3f %s \n','Runup',R,labelUnitDist)
    fprintf('%s \t %-6.3f %s^3/sec-%s \n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
end
    



