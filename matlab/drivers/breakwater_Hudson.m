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

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

if single_case
    [unitwt] = USER_INPUT_DATA_VALUE(['Enter unitwt: armor specific unit weight (' labelUnitWt '/' labelUnitDist '^3): '], 1.0, 99999.0);
    
    [H] = USER_INPUT_DATA_VALUE(['Enter H: wave height (' labelUnitDist '): '], 0.1, 100.0);
    
    [Kd] = USER_INPUT_DATA_VALUE('Enter Kd: stability coefficient: ', 0, 10);
    
    [kdelt] = USER_INPUT_DATA_VALUE('Enter kdelt: layer coefficient: ', 0, 2);
    
    [P] = USER_INPUT_DATA_VALUE('Enter P: average porosity of armor layer: ', 0, 54);
    
    [cotssl] = USER_INPUT_DATA_VALUE('Enter cotssl: cotangent of structure slope: ', 1.0, 6.0);
    
    [n] = USER_INPUT_DATA_VALUE('Enter n: number of armor units comprising the thickness of the armor layer: ', 1.0, 3.0);
    
    numCases = 1;
else
    multiCaseData = {...
        ['unitwt: armor specific unit weight (' labelUnitWt '/' labelUnitDist '^3)'], 1.0, 99999.0;...
        ['H: wave height (' labelUnitDist ')'], 0.1, 100.0;...
        'Kd: stability coefficient', 0, 10;...
        'kdelt: layer coefficient', 0, 2;...
        'P: average porosity of armor layer', 0, 54;...
        'cotssl: cotangent of structure slope', 1.0, 6.0;...
        'n: number of armor units comprising the thickness of the armor layer', 1.0, 3.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    unitwtList = varData(1, :);
    HList = varData(2, :);
    KdList = varData(3, :);
    kdeltList = varData(4, :);
    PList = varData(5, :);
    cotsslList = varData(6, :);
    nList = varData(7, :);
end

H20weight=rho*g; %64 lb/ft^3 for seawater, 62.4 for fresh

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/breakwater_Hudson.txt', 'wt');

    fprintf(fId, 'Breakwater Hudson Output\n\n');
end

for loopIndex = 1:numCases
    if ~single_case
        unitwt = unitwtList(loopIndex);
        H = HList(loopIndex);
        Kd = KdList(loopIndex);
        kdelt = kdeltList(loopIndex);
        P = PList(loopIndex);
        cotssl = cotsslList(loopIndex);
        n = nList(loopIndex);
    end
    
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
    fprintf('%s \t\t\t\t\t %-6.2f %s \t \n','Crest width',b,labelUnitDist)
    fprintf('%s \t %-6.2f %s \t \n','Average cover layer thickness',r,labelUnitDist)
    fprintf('%s \t %-6.2f \t \n','Number of single armor unit',Nr)
    
    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end
        
        fprintf(fId, 'unitwt                             %6.2f %s/%s^3\n', unitwt, labelUnitWt, labelUnitDist);
        fprintf(fId, 'H                                  %6.2f %s\n', H, labelUnitDist);
        fprintf(fId, 'Kd                                 %6.2f\n', Kd);
        fprintf(fId, 'kdelt                              %6.2f\n', kdelt);
        fprintf(fId, 'P                                  %6.2f %%\n', P);
        fprintf(fId, 'cotssl                             %6.2f\n', cotssl);
        fprintf(fId, 'n                                  %6.2f\n\n', n);
        
        fprintf(fId, '%s          %6.2f %s\n','Weight of individual unit',w,units);
        fprintf(fId, '%s                        %6.2f %s\n','Crest width',b,labelUnitDist);
        fprintf(fId, '%s      %6.2f %s\n','Average cover layer thickness',r,labelUnitDist);
        fprintf(fId, '%s        %6.2f\n','Number of single armor unit',Nr);
        
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
    end
end

if fileOutputData{1}
    fclose(fId);
end