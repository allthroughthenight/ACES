clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Breakwater Design Using Hudson and Related Equations
% (page 4-1 in ACES User's Guide). Estimates armor weight, minimum crest,
% width, armor thickness, and the number of armor units per unit area of
% a breakwater using Hudson and related equations.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 13, 2011
% Date Modified:

% Requires the following functions:
% no functions required

% MAIN VARIABLE LIST:
%   INPUT
%   unitwt: armor specific unit weight (N/m^3) - 1 N/m^3 = 157 ft/lb^3
%   H: wave height (m)
%   Kd: stability coefficient
%   kdelt: layer coefficient
%   P: average porosity of armor layer
%   cotssl: cotangent of structure slope
%   n: number of armor units comprising the thickness of the armor layer

%   OUTPUT
%   w: weight of individual armor unit (N)
%   b: crest width of breakwater (m)
%   r: average cover layer thickness (m)
%   Nr: number of single armor units per unit surface area

%   OTHERS
%   rho: density of water (kg/m^3)
%   H20weight: specific weight of water
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g] = USER_INPUT_METRIC_IMPERIAL();

if single_case
    if metric
        [unitwt] = USER_INPUT_DATA_VALUE('Enter unitwt: armor specific unit weight (N/m^3): ', 1.0, 99999.0);
        [H] = USER_INPUT_DATA_VALUE('Enter H: wave height (m): ', 0.1, 100.0);
    else
        [unitwt] = USER_INPUT_DATA_VALUE('Enter unitwt: armor specific unit weight (lb/ft^3): ', 1.0, 99999.0);
        [H] = USER_INPUT_DATA_VALUE('Enter H: wave height (ft): ', 0.1, 100.0);
    end
    
    [Kd] = USER_INPUT_DATA_VALUE('Enter Kd: stability coefficient: ', 0, 10);
    
    [kdelt] = USER_INPUT_DATA_VALUE('Enter kdelt: layer coefficient: ', 0, 2);
    
    [P] = USER_INPUT_DATA_VALUE('Enter P: average porosity of armor layer: ', 0, 54);
    
    [cotssl] = USER_INPUT_DATA_VALUE('Enter cotssl: cotangent of structure slope: ', 1.0, 6.0);
    
    [n] = USER_INPUT_DATA_VALUE('Enter n: number of armor units comprising the thickness of the armor layer: ', 1.0, 3.0);
else
    unitwt=165;
    H=11.50;
    Kd=10.0;
    kdelt=1.02;
    P=54.0;
    cotssl=2.00;
    n=2;
end

rho=1.989;
H20weight=rho*g; %64 lb/ft^3 for seawater, 62.4 for fresh

specgrav=unitwt/H20weight;

w=(unitwt*H^3)/(Kd*(specgrav-1.0)^3*cotssl);
r=n*kdelt*(w/unitwt)^(1/3);
Nr=1000*n*kdelt*(1-P/100)*(unitwt/w)^(2/3);
b=3*kdelt*(w/unitwt)^(1/3);

if metric
    if w>8000
        w=w/8896.4; %1 ton=8896.4 N
        units='tons';
    else
        units='N';
    end
else
    if w>2000
        w=w/2000;
        units='tons';
    else
        units='lbs';
    end
end

fprintf('%s \t\t %-6.2f %s \t \n','Weight of individual unit',w,units)
fprintf('%s \t\t\t\t\t %-6.2f \t \n','Crest width',b)
fprintf('%s \t %-6.2f \t \n','Average cover layer thickness',r)
fprintf('%s \t %-6.2f \t \n','Number of single armor unit',Nr)
