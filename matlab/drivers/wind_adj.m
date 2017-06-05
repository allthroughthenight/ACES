clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Windspeed Adjustment and Wave Growth (page 1-1 of ACES User's
% Guide). Provide estimates for wave growth over open-water and restricted
% fetches in deep and shallow water.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 28, 2011
% Date Modified:

% Requires the following functions:
% ERRWAVBRK1
% WADJ
% WAGEOS
% WAPBL
% WAPSI
% WASBL
% WASHR
% WGDL
% WGFD
% WGFET
% WGFL
% WGRO

% MAIN VARIABLE LIST:
%   INPUT
%   zobs: elevation of observed winds [m]
%   uobs: observed wind speed [m/s]
%   dtemp: air-sea temperature difference [deg C]
%   duro: duration of observed wind [hr]
%   durf: duration of final wind [hr]
%   lat: latitude of wind observation [deg]
%   windobs: wind observation type
%   fetchopt: wind fetch options
%   wgtyp: open water wave growth equation options

%   OPEN-WATER VARIABLES
%   F: length of wind fetch [m]
%   d: average depth of fetch (only for shallow water equations) [m]

%   RESTRICTED VARIABLES
%   wdir: wind direction [deg]
%   dang: radial angle increment [deg]
%   ang1: direction of first radial fetch [deg]
%   angs: fetch length [m]

%   OUTPUT
%   ue: equivalent neutral wind speed [m/s]
%   ua: adjusted wind speed [m/s]
%   Hmo: wave height [m]
%   Tp: peak wave period [s]
%   wg: type of wave-growth
%   theta: wave direction with respect to N [deg]

%   OTHERS
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

if metric
    labelSpeed = 'km/h';
else
    labelSpeed = 'mph';
end

% fprintf('%s \n','Wind observation types: ');
% fprintf('%s \n','[1] Overwater (shipboard)')
% fprintf('%s \n','[2] Overwater (not shipboard)')
% fprintf('%s \n','[3] Shore (windward - offshore to onshore)')
% fprintf('%s \n','[4] Shore (leeward - onshore to offshore)')
% fprintf('%s \n','[5] Over land')
% fprintf('%s \n\n','[6] Geostrophic wind')
% 
% windobs=input('Select option: ');
% fprintf('\n')
[windobs] = USER_INPUT_FINITE_CHOICE(...
    ['Wind observation types: \n'...
        '[1] Overwater (shipboard)\n'...
        '[2] Overwater (not shipboard)\n'...
        '[3] Shore (windward - offshore to onshore)\n'...
        '[4] Shore (leeward - onshore to offshore)\n'...
        '[5] Over land\n'...
        '[6] Geostrophic wind\n'...
        'Select option: '],...
    {'1', '2', '3', '4', '5', '6'});
windobs = str2num(windobs);

% fprintf('%s \n','Wind fetch and wave growth options: ');
% fprintf('%s \n','[1] Open Water - Deep')
% fprintf('%s \n','[2] Open Water - Shallow')
% fprintf('%s \n','[3] Restricted - Deep')
% fprintf('%s \n\n','[4] Restricted - Shallow')
% 
% wgtyp=input('Select option: ');
% fprintf('\n')
[wgtyp] = USER_INPUT_FINITE_CHOICE(...
    ['Wind fetch and wave growth options: \n'...
        '[1] Open Water - Deep\n'...
        '[2] Open Water - Shallow\n'...
        '[3] Restricted - Deep\n'...
        '[4] Restricted - Shallow\n'...
        'Select option: '],...
    {'1', '2', '3', '4'});
wgtyp = str2num(wgtyp);
use_value_F = wgtyp == 1 || wgtyp == 2;
use_value_d = wgtyp == 2 || wgtyp == 4;
use_values_restricted = wgtyp == 3 || wgtyp == 4;

% Single case input
if single_case
    [zobs] = USER_INPUT_DATA_VALUE(['Enter zobs: elevation of observed winds [' labelUnitDist ']: '], 1.0, 5000.0);

    [uobs] = USER_INPUT_DATA_VALUE(['Enter uobs: observed wind speed [' labelSpeed ']: '], 0.1, 200.0);

    [dtemp] = USER_INPUT_DATA_VALUE('Enter dtemp: air-sea temperature difference [deg C]: ', -100.0, 100.0);
    
    [duro] = USER_INPUT_DATA_VALUE('Enter duro: duration of observed wind [hr]: ', 0.1, 86400.0);
    
    [durf] = USER_INPUT_DATA_VALUE('Enter durf: duration of final wind [hr]: ', 0.1, 86400.0);
    
    [lat] = USER_INPUT_DATA_VALUE('Enter lat: latitude of wind observation [deg]: ', 0.0, 180.0);
    
    if use_value_F
        [F] = USER_INPUT_DATA_VALUE(['Enter F: length of wind fetch [' labelUnitDist ']: '], 0.0, 9999.0);
    end
    
    if use_value_d
        [d] = USER_INPUT_DATA_VALUE(['Enter d: average depth of fetch [' labelUnitDist ']: '], 0.1, 10000.0);
    else
        d = 0;
    end
    
    if use_values_restricted
        [wdir] = USER_INPUT_DATA_VALUE('Enter wdir: wind direction [deg]: ', 0.0, 360.0);
        
        [dang] = USER_INPUT_DATA_VALUE('Enter dang: radial angle increment [deg]: ', 1.0, 180.0);
        
        [ang1] = USER_INPUT_DATA_VALUE('Enter ang1: direction of first radial fetch [deg]: ', 0.0, 360.0);
        
        [] = USER_INPUT_DATA_VALUE('Enter angs: fetch length [m]: ', );
    end
    
    numCases = 1;
else
    multiCaseData = {...
        ['zobs: elevation of observed winds [' labelUnitDist ']'], 1.0, 5000.0;...
        ['uobs: observed wind speed [' labelSpeed ']'], 0.1, 200.0;...
        'dtemp: air-sea temperature difference [deg C]', -100.0, 100.0;...
        'duro: duration of observed wind [hr]', 0.1, 86400.0;...
        'durf: duration of final wind [hr]', 0.1, 86400.0;...
        'lat: latitude of wind observation [deg]', 0.0, 180.0};
    
    if use_value_F
        multiCaseData = [multiCaseData; {['F: length of wind fetch [' labelUnitDist ']: '], 0.0, 9999.0}];
    end
    
    if use_value_d
        multiCaseData = [multiCaseData; {['d: average depth of fetch [' labelUnitDist ']: '], 0.1, 10000.0}];
    end
    
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    zobsList = varData(1, :);
    uobsList = varData(2, :);
    dtempList = varData(3, :);
    duroList = varData(4, :);
    durfList = varData(5, :);
    latList = varData(6, :);
    
    optVarNum = 7;
    
    if use_value_F
        FList = varData(optVarNum, :);
        optVarNum = optVarNum + 1;
    end
    
    if use_value_d
        dList = varData(optVarNum, :);
        optVarNum = optVarNum + 1;
    end
end

% Constant for convertions
ft2m=0.3048;
mph2mps=0.44704;
hr2s=3600;
min2s=60;
deg2rad=pi/180;
mi2m=1609.344;
F2C=5/9;
knots2mps=0.5144;

if wgtyp==1 %Open Water - Deep
%    F=27;
%    d=0;
    phi=0;
elseif wgtyp==2 %Open Water - Shallow
%    F=27;
%    d=13;
    phi=0;
elseif wgtyp==3 %Restricted - Deep
%    d=0;
    wdir=120;
    dang=12;
    ang1=0;
    angs=[3.7;12.3;13.4;12.2;13.2;36.0;35.6;28.7;26.8;13.0;10.4;10.1;6.4;5.7];
    [F,phi,theta]=WGFET(ang1,dang,wdir,angs);
else %Restricted - Shallow
%    d=13;
    wdir=120;
    dang=12;
    ang1=0;
    angs=[3.7;12.3;13.4;12.2;13.2;36.0;35.6;28.7;26.8;13.0;10.4;10.1;6.4;5.7];
    %angs=[3.7;12.3;13.4;12.2;13.2;36.0;35.6;28.7;10.4;5.7];
    [F,phi,theta]=WGFET(ang1,dang,wdir,angs);
end

for loopIndex = 1:numCases
    if ~single_case
        zobs = zobsList(loopIndex);
        uobs = uobsList(loopIndex);
        dtemp = dtempList(loopIndex);
        duro = duroList(loopIndex);
        durf = durfList(loopIndex);
        
        if use_value_F
            F = FList(loopIndex);
        end
        
        if use_value_d
            d = dList(loopIndex);
        end
    end
    
    assert(lat~=0, 'Error: Latitude must be a non-zero value.')
    
    [ue]=WADJ(uobs*mph2mps,zobs*ft2m,dtemp,F*mi2m,duro*hr2s,durf*hr2s,lat*deg2rad,windobs);

    [ua,Hmo,Tp,wgmsg]=WGRO(d*ft2m,F*mi2m,phi,durf*hr2s,ue,wgtyp);

    fprintf('%s %s \n','Wave growth: ',wgmsg)
    if wgtyp==3 || wgtyp==4
        fprintf('%s \t %-6.2f \n','Mean wave direction',theta)
        fprintf('%s \t\t\t\t %-6.2f \n','Wind fetch',F)
    end
    % TODO: Add metric speed
    fprintf('%s \t\t %-6.2f %s \n','Equiv. wind speed',ue/mph2mps, labelSpeed)
    fprintf('%s \t\t %-6.2f %s \n','Adjus. wind speed',ua/mph2mps, labelSpeed)

    fprintf('%s \t\t\t %-6.2f %s \n','Wave height ',Hmo/ft2m,labelUnitDist)
    fprintf('%s \t\t\t %-6.2f s \n','Wave period ',Tp)
end

if single_case
    % File Output
    fileOutputArgs = {};
    [fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

    if fileOutputData{1}
        fId = fopen('output/wind_adj.txt', 'wt');

        fprintf(fId, 'Partial Listing of Plot Output File 1\n\n');

        fprintf(fId, 'Section 1 of the plot output file 1\n\n');

        fprintf(fId, 'Section 2 of the plot output file 2\n\n');

        fclose(fId);
    end
end