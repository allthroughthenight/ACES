clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Longshore Sediment Transport (page 6-1 in ACES User's Guide).
% Provides estimates of the potential longshore transport rate under the
% action of waves

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 21, 2011
% Date Modified:

% Requires the following functions:
% DEEP_TRANS
% BREAK_TRANS

% MAIN VARIABLE LIST:
%   INPUT
%   H: Wave height (either deepwater or breaking) [ft]
%   alpha: wave angle (either deepwater angle of wave crest or crest angle
%          with shoreline) [deg]
%   K: dimensionless coefficient [default value 0.39]

%   OUTPUT
%   Q: sediment transport rate [yd^3/year]

%   OTHERS
%   g: gravity [32.17 ft/s^2]
%   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs/ft^3]
%   rhos: density of sediment [5.14 slugs/ft^3 in FORTRAN source code]
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

fprintf('%s \n\n','Chose Longshore Sediment Transport Method: ');
fprintf('%s \n','[1] Transport using deep water wave conditions')
fprintf('%s \n','[2] Transport using breaking water wave conditions')
% fprintf('%s \n','[3] Transport using CEDRS statistical data:Percent Occurence of wave height & period by direction')

option=input('Select option: ');
fprintf('\n')

if single_case
    if option==1
       [Ho] = USER_INPUT_DATA_VALUE(['Enter Ho: deep water wave height (' labelUnitDist '): '], 0.1, 100.0);
    elseif option==2
       [Hb] = USER_INPUT_DATA_VALUE(['Enter Hb: breaking wave height (' labelUnitDist '): '], 0.1, 100.0);
    end

    [alpha] = USER_INPUT_DATA_VALUE('Enter alpha: wave crest angle with shoreline (deg): ', 0, 90.0);

    [K] = USER_INPUT_DATA_VALUE('Enter K: emprical coefficient: ', 0.0, 1.0);

    numCases=1;
else
     if option==1
        multiCaseData = [ multiCaseData; {'Enter Ho: deep water wave height (' labelUnitDist '): ', 0.1, 100.0}];
     elseif option==2
        multiCaseData = [ multiCaseData; {'Enter Hb: breaking water wave height (' labelUnitDist '): ', 0.1, 100.0}];
     end

     multiCaseData = [ multiCaseData;...
        {'Enter alpha: wave crest angle with shoreline (deg): ', 0, 90.0;...
        'Enter K: emprical coefficient: ', 0.0, 1.0}];

    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);

    optVarNum = 2;
    if option==1
        HoList = varData(1, :);
        optVarNum = optVarNum + 1;
    else
        HbList = varData(1, :);
    end

        alphaList = varData(2, :);
        KList = varData(3, :);
end

for loopIndex = 1:numCases
    if ~single_case
        if option==1
           Ho = HoList(loopIndex);
        else
           Hb = HbList(loopIndex);
        end

        alpha = alphaList(loopIndex);
        K = KList(loopIndex);

    end

    if metric
         labelUnitDistTransportRate = 'm';
         rhos = 2648; %kg/m^3 density of quartz
    else
         labelUnitDistTransportRate = 'yd';
         rhos=165.508/g; %bulk density of quartz is 165.508 lb/ft^3 - 165.508/g=5.14
    end

    if option==1
        [Q]=DEEP_TRANS(Ho,alpha,K,rho,g,rhos);
    else
        [Q]=BREAK_TRANS(Hb,alpha,K,rho,g,rhos);
    end

    if ~metric
        %Q=Q*1168800; %ACES conversion
        Q=Q*1168775.04; %convert from ft^3/s to yd^3/yr
    else
        Q = Q* 3.154*10^7;%m^3/s to m^3/yr
    end

    fprintf('%s \t %13.0f \n',['Sediment transport rate(' labelUnitDistTransportRate '^3/yr):'], Q)

end
