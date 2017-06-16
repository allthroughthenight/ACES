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

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

if metric
    labelSpeed = 'm/s';
    labelUnitDistLrg = 'km';
else
    labelSpeed = 'mph';
    labelUnitDistLrg = 'mi';
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
is_water_open = wgtyp == 1 || wgtyp == 2;
is_water_shallow = wgtyp == 2 || wgtyp == 4;
%is_water_restricted = wgtyp == 3 || wgtyp == 4;

[use_knots] = USER_INPUT_FINITE_CHOICE(...
    ['Speed options:\n[M] ' labelSpeed '\n[K] knots\nSelect option: '],...
    {'M', 'm', 'K', 'k'});
use_knots = strcmp(use_knots, 'K') || strcmp(use_knots, 'k');
if use_knots
    labelSpeedFinal = 'knots';
else
    labelSpeedFinal = labelSpeed;
end

% Single case input
if single_case
    [zobs] = USER_INPUT_DATA_VALUE(['Enter zobs: elevation of observed winds [' labelUnitDist ']: '], 1.0, 5000.0);

    [Uobs] = USER_INPUT_DATA_VALUE(['Enter uobs: observed wind speed [' labelSpeedFinal ']: '], 0.1, 200.0);

    [dtemp] = USER_INPUT_DATA_VALUE('Enter dtemp: air-sea temperature difference [deg C]: ', -100.0, 100.0);
    
    [duro] = USER_INPUT_DATA_VALUE('Enter duro: duration of observed wind [hr]: ', 0.1, 86400.0);
    
    [durf] = USER_INPUT_DATA_VALUE('Enter durf: duration of final wind [hr]: ', 0.1, 86400.0);
    
    [lat] = USER_INPUT_DATA_VALUE('Enter lat: latitude of wind observation [deg]: ', 0.0, 180.0);
    
    if is_water_open
        [F] = USER_INPUT_DATA_VALUE(['Enter F: length of wind fetch [' labelUnitDistLrg ']: '], 0.0, 9999.0);
    end
    
    if is_water_shallow
        [d] = USER_INPUT_DATA_VALUE(['Enter d: average depth of fetch [' labelUnitDist ']: '], 0.1, 10000.0);
    else
        d = 0;
    end
    
    if ~is_water_open
        [wdir] = USER_INPUT_DATA_VALUE('Enter wdir: wind direction [deg]: ', 0.0, 360.0);
    end
    
    numCases = 1;
else
    multiCaseData = {...
        ['zobs: elevation of observed winds [' labelUnitDist ']'], 1.0, 5000.0;...
        ['uobs: observed wind speed [' labelSpeedFinal ']'], 0.1, 200.0;...
        'dtemp: air-sea temperature difference [deg C]', -100.0, 100.0;...
        'duro: duration of observed wind [hr]', 0.1, 86400.0;...
        'durf: duration of final wind [hr]', 0.1, 86400.0;...
        'lat: latitude of wind observation [deg]', 0.0, 180.0};
    
    if is_water_open
        multiCaseData = [multiCaseData; {['F: length of wind fetch [' labelUnitDistLrg ']'], 0.0, 9999.0}];
    end
    
    if is_water_shallow
        multiCaseData = [multiCaseData; {['d: average depth of fetch [' labelUnitDist ']'], 0.1, 10000.0}];
    end
    
    if ~is_water_open
%         multiCaseData = [multiCaseData;...
%             {'wdir: wind direction [deg]', 0.0, 360.0;...
%             'dang: radial angle increment [deg]', 1.0, 180.0;...
%             'ang1: direction of first radial fetch [deg]', 0.0, 360.0;...
%             'Nfet: number of radial fetches', 2, 360;...
%             ['angs: fetch length [' labelUnitDistLrg ']'], 0, 9999}];
        multiCaseData = [multiCaseData;...
            {'wdir: wind direction [deg]', 0.0, 360.0}];
    end
    
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    zobsList = varData(1, :);
    uobsList = varData(2, :);
    dtempList = varData(3, :);
    duroList = varData(4, :);
    durfList = varData(5, :);
    latList = varData(6, :);
    
    optVarNum = 7;
    
    if is_water_open
        FList = varData(optVarNum, :);
        optVarNum = optVarNum + 1;
    end
    
    if is_water_shallow
        dList = varData(optVarNum, :);
        optVarNum = optVarNum + 1;
    end
    
    if ~is_water_open
        wdirList = varData(optVarNum, :);
%         dangList = varData(optVarNum + 1, :);
%         ang1List = varData(optVarNum + 2, :);
%         NfetList = varData(optVarNum + 3, :);
%         angsList = varData(optVarNum + 4, :);
    end
end

if ~is_water_open
    [dang] = USER_INPUT_DATA_VALUE('Enter dang: radial angle increment [deg]: ', 1.0, 180.0);

    [ang1] = USER_INPUT_DATA_VALUE('Enter ang1: direction of first radial fetch [deg]: ', 0.0, 360.0);

    [manualOrFile] = USER_INPUT_FINITE_CHOICE(...
        ['Would you like to enter fetch length data manually or load from a file?\n'...
            '[M] for manual entry or [F] for file loading: '],...
        {'M', 'm', 'F', 'f'});
    data_entry_manual = strcmp(manualOrFile, 'M') || strcmp(manualOrFile, 'm');

    if data_entry_manual
        [Nfet] = USER_INPUT_DATA_VALUE('Enter Nfet: number of radial fetches: ', 2, 360);
        Nfet = floor(Nfet);

        angs = [];
        for angsLoopIndex = 1:Nfet
            angTemp = USER_INPUT_DATA_VALUE(['Enter angs: fetch length [' labelUnitDistLrg '] #' num2str(angsLoopIndex) ': '], 0,9999);

            angs = [angs angTemp];
        end

        clear angsLoopIndex;
        clear angTemp;
    else
        accepted = false;
        while ~accepted
            [filename] = USER_INPUT_FILE_NAME();

            fId = fopen(filename);

            fileData = textscan(fId, '%f');

            fclose(fId);

            if length(fileData{1}) >= 2 && length(fileData{1}) <= 360
                accepted = true;
            else
                fprintf('File must have Nt, K, d, and between 1 and 200 storm heights.\n');
            end
        end

        angs = fileData{1};
        Nfet = length(angs);
    end
end


% Constant for convertions
ft2m=0.3048;
mph2mps=0.44704;
hr2s=3600;
min2s=60;
deg2rad=pi/180;
mi2m=1609.344;
km2m=0.001;
F2C=5/9;
knots2mps=0.5144;

if ~metric
    conversionDist = ft2m;
    conversionDistLrg = mi2m;
else
    conversionDist = 1.0;
    conversionDistLrg = km2m;
end

if use_knots
    conversionSpeed = knots2mps;
elseif ~metric
    conversionSpeed = mph2mps;
else
    conversionSpeed = 1.0;
end

for loopIndex = 1:numCases
    if ~single_case
        zobs = zobsList(loopIndex);
        Uobs = uobsList(loopIndex);
        dtemp = dtempList(loopIndex);
        duro = duroList(loopIndex);
        durf = durfList(loopIndex);
        lat = latList(loopIndex);
        
        if is_water_open
            F = FList(loopIndex);
        end
        
        if is_water_shallow
            d = dList(loopIndex);
        else
            d = 0;
        end
        
        if ~is_water_open
        end
        
        if is_water_open
            phi=0;
        else
            wdir = wdirList(loopIndex);
            [F,phi,theta]=WGFET(ang1,dang,wdir,angs);
        end
    end
    
    assert(lat~=0, 'Error: Latitude must be a non-zero value.')
    
%   Check WDIR vs Fetch data. WDIR must meet this criterion:
%   ang1 -45 degrees <= WDIR <= anglast + 45 degrees
    if ~is_water_open
        assert(ang1 - 45 <= wdir,...
            'Error: wdir must be at least 45 degrees less than the first fetch angle.');
        assert(wdir <= (ang1 + (Nfet - 1)*dang) + 45,...
            'Error: wdir must be at most 45 degrees more than the final fetch angle.');
    end
    
%    [ue]=WADJ(Uobs*mph2mps,zobs*ft2m,dtemp,F*mi2m,duro*hr2s,durf*hr2s,lat*deg2rad,windobs);
    [ue]=WADJ(Uobs*conversionSpeed,...
        zobs*conversionDist,...
        dtemp,...
        F*conversionDistLrg,...
        duro*hr2s,...
        durf*hr2s,...
        lat*deg2rad,...
        windobs);

    [ua,Hmo,Tp,wgmsg]=WGRO(d*conversionDist,F*conversionDistLrg,phi,durf*hr2s,ue,wgtyp);

    if ~is_water_open
        fprintf('%s \t\t\t\t %-6.2f %s\n','Wind fetch',F, labelUnitDistLrg);
        fprintf('%s \t\t\t %-6.2f deg\n', 'Wind Direction', wdir);
    end
    
%    fprintf('%s \t\t %-6.2f %s \n','Equiv. wind speed',ue/mph2mps, labelSpeedFinal);
    fprintf('%s \t\t %-6.2f %s \n','Equiv. wind speed',ue/conversionSpeed, labelSpeedFinal);
%    fprintf('%s \t\t %-6.2f %s \n','Adjus. wind speed',ua/mph2mps, labelSpeedFinal);
    fprintf('%s \t\t %-6.2f %s \n','Adjus. wind speed',ua/conversionSpeed, labelSpeedFinal);
    
    if ~is_water_open
        fprintf('%s \t %-6.2f deg\n','Mean wave direction',theta);
    end

    fprintf('%s \t\t\t %-6.2f %s \n','Wave height ',Hmo/conversionDist,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f s \n','Wave period ',Tp);
    
    fprintf('%s %s \n','Wave growth: ',wgmsg);
end

if single_case
    % File Output
    fileOutputArgs = {};
    [fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

    if fileOutputData{1}
        fId = fopen('output/wind_adj.txt', 'wt');

        fprintf(fId, 'Wind Adj\n\n');
        
        if ~is_water_open
            fprintf(fId, '%s \t\t\t %-6.2f %s\n','Wind fetch',F, labelUnitDistLrg);
            fprintf(fId, '%s \t\t\t %-6.2f deg\n', 'Wind Direction', wdir);
        end

        fprintf(fId, '%s \t\t %-6.2f %s \n','Equiv. wind speed',ue/conversionSpeed, labelSpeedFinal);
        fprintf(fId, '%s \t\t %-6.2f %s \n','Adjus. wind speed',ua/conversionSpeed, labelSpeedFinal);

        if ~is_water_open
            fprintf(fId, '%s \t\t %-6.2f deg\n','Mean wave direction',theta);
        end

        fprintf(fId, '%s \t\t\t %-6.2f %s \n','Wave height ',Hmo/conversionDist,labelUnitDist);
        fprintf(fId, '%s \t\t\t %-6.2f s \n','Wave period ',Tp);

        fprintf(fId, '%s %s \n','Wave growth: ',wgmsg);

        fclose(fId);
    end
end