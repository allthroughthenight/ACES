clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Irregular Wave Runup on Beaches (page 5-1 in ACES % User's Guide). 
% Provides an approach to calculate runup statistical parameters for wave
% runup on smooth slope linear beaches.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 18, 2011
% Date Verified: June 6, 2012

% Requires the following functions:
% no functions required

% MAIN VARIABLE LIST:
%   INPUT
%   Hs0: deepwater significant wave height
%   Tp: peak energy wave period (sec)
%   cottheta: cotangent of foreshore slope

%   OUTPUT
%   Rmax: maximum runup
%   R2: runup exceeded by 2 percent of the runups
%   R110: Average of the highest one-tenth of the runups
%   R13: Average of highest one-third of the runups
%   Ravg: average run

%   OTHERS
%   I: Irribarren number
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

if single_case
    if metric
        [Hs0] = USER_INPUT_DATA_VALUE('Enter Hs0: deepwater significant wave height (m): ', 0.1, 100.0);
    else
        [Hs0] = USER_INPUT_DATA_VALUE('Enter Hs0: deepwater significant wave height (ft): ', 0.1, 100.0);
    end
    
    [Tp] = USER_INPUT_DATA_VALUE('Enter Tp: peak energy wave period (sec): ', 0.1, 100.0);
    
    [cottheta] = USER_INPUT_DATA_VALUE('Enter cottheta: cotangent of foreshore slope: ', 0.1, 100.0);
else
    Hs0=4.6;
    Tp=9.50;
    cottheta=13.0;
end

%Coefficients provided by Mase (1989)
amax=2.32;
bmax=0.77;
a2=1.86;
b2=0.71;
a110=1.70;
b110=0.71;
a13=1.38;
b13=0.70;
aavg=0.88;
bavg=0.69;

L0=g*(Tp^2)/(2*pi);
steep=Hs0/L0;
assert(steep<0.142,'Error: Input wave unstable (Max: 0.142, [H/L] = %0.4f)',steep')

tantheta=1/cottheta;
I=tantheta/sqrt(Hs0/L0);

Rmax=Hs0*amax*(I^bmax);
R2=Hs0*a2*(I^b2);
R110=Hs0*a110*(I^b110);
R13=Hs0*a13*(I^b13);
Ravg=Hs0*aavg*(I^bavg);

fprintf('%s \t\t\t\t\t %-6.2f %s \n','Maximum runup',Rmax,labelUnitDist)
fprintf('%s \t %-6.2f %s \n','Runup exceeded by 2% of runup',R2,labelUnitDist)
fprintf('%s \t %-6.2f %s \n','Avg. of highest 1/10 runups',R110,labelUnitDist)
fprintf('%s \t\t %-6.2f %s \n','Avg. of highest 1/3 runups',R13,labelUnitDist)
fprintf('%s \t\t\t\t\t %-6.2f %s \n','Maximum runup',Ravg,labelUnitDist)
