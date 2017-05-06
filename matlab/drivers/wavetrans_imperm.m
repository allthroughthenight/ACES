clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Wave Transmission on Impermeable Structures (page 5-3 in ACES
% User's Guide). Provides estimates of wave runup and transmission on rough
% and smooth slope structures. It also addresses wave transmission over
% impermeable vertical walls and composite structures.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 19, 2011
% Date Verified: June 6, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK2
% HTP
% LWTGEN
% RUNUPR
% RUNUPS
% VERTKT
% WAVELEN

% MAIN VARIABLE LIST:
%   MANDATORY INPUT
%   H: incident wave height (Hs for irregular waves)
%   T: wave period (Tp for irregular waves)
%   cotphi: cotan of nearshore slope
%   ds: water depth at structure toe
%   hs: structure height above toe 
%   wth: structure crest width
%   cottheta: cotan of structure slope (0.0 for vertical wall)

%   OPTIONAL INPUT
%   a: empirical coefficient for rough slope runup
%   b: empirical coefficeint for rough slope runup
%   R: wave runup (if known)
%   hb: toe protection or composite breakwater berm height above structure
%   toe

%   MANDATORY OUTPUT
%   Ht: transmitted wave height

%   OPTIONAL OUTPUT
%   R: wave runup

%   OTHERS
%   freeb: freeboard
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g] = USER_INPUT_METRIC_IMPERIAL();

if single_case
    [H] = USER_INPUT_DATA_VALUE('Enter H: incident wave height (Hs for irregular waves) (m): ', 0.1, 100.0);
    
    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (Tp for irregular waves) (s): ', 1.0, 1000.0);
    
    [cotphi] = USER_INPUT_DATA_VALUE('Enter cotphi: cotan of nearshore slope: ', 5.0, 10000.0);
    
    [ds] = USER_INPUT_DATA_VALUE('Enter ds: water depth at structure toe (m): ', 0.1, 200.0);
    
    [hs] = USER_INPUT_DATA_VALUE('Enter hs: structure height above toe (m): ', 0.0, 200.0);
    
    [wth] = USER_INPUT_DATA_VALUE('Enter wth: structure crest width (m): ', 0.0, 200.0);
    
    [cottheta] = USER_INPUT_DATA_VALUE('Enter cottheta: cotan of structure slope (0.0 for vertical wall): ', 0.0, 30.0);
    
    [R] = USER_INPUT_DATA_VALUE('Enter R: wave runup (if known) (m): ', 0.0, 100.0);
else
    H=7.50;
    T=10.00;
    cotphi=100.0;
    ds=10.0;
    cottheta=3.0;
    hs=15.0;
    wth=7.50;
    R=15.0;
end

a=0.956;
b=0.398;
hb=6.00;

m=1/cotphi;

fprintf('%s \n\n','Calculation and slope type options: ');
fprintf('%s \n','[1] Wave transmission only for smooth slope')
fprintf('%s \n','[2] Wave transmission only for vertical wall')
fprintf('%s \n','[3] Wave runup and transmission for rough slope')
fprintf('%s \n\n','[4] Wave runup and transmission for smooth slope')

option=input('Select option: ');
fprintf('\n')

if option~=2
    assert(ds<hs,'Error: Method does not apply to submerged structures.')
end

[c,c0,cg,cg0,k,L,L0,reldep]=LWTGEN(ds,T,g);

[Hbs]=ERRWAVBRK2(T,m,ds);
assert(H<Hbs,'Error: Wave broken at structure (Hbs = %6.2f m)',Hbs)

[steep,maxstp]=ERRSTP(H,ds,L);
assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

if cottheta==0
    assert(option==2,'Error: A cotangent of zero indicates a vertical wall.')

    reldep=ds/L;
    
    assert(reldep>0.14 && reldep<0.5, 'Error: d/L conditions exceeded - 0.14<=(d/L)<=0.5')
else
    theta=atan(1/cottheta);
    ssp=(1/cottheta)/sqrt(H/L0);
end

if option==3
    a=0.956;
    b=0.398;
    [R]=RUNUPR(H,ssp,a,b);
    fprintf('%s \t\t\t\t\t\t %-6.3f \n','Runup',R)
elseif option==4
    [R]=RUNUPS(H,L,ds,theta,ssp);
    fprintf('%s \t\t\t\t\t\t %-6.3f \n','Runup',R)
end

freeb=hs-ds;

if option~=2
    [Ht]=HTP(wth,hs,R,H,freeb);
    fprintf('%s \t %-6.3f \n','Transmitted wave height',Ht)
else
    dl=ds-hb;
    [Ht]=VERTKT(H,freeb,wth,ds,dl);
    fprintf('%s \t %-6.3f \n','Transmitted wave height',Ht)
end





