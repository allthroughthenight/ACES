clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Linear Wave Theory (page 2-1 in ACES User's Guide)
% Yields first-order approximations for various wave parameters of wave
% motion as predicted by linear wave theory

% Transferred by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: March 17, 2011
% Date Modified: June 26th, 2016 by yaprak

% Requires the following functions:
% ERRWAVBRK1
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   H: wave height (m or ft)
%   T: wave period (sec)
%   d: water depth (m or ft)
%   z: vertical coordinate (m or ft)
%   xL: horizontal coordinate as fraction of wavelength (x/L)

%   OUTPUT
%   L: wavelength (m or ft)
%   C: wave celerity (m/sec or ft/sec)
%   Cg: group celerity (m/sec or ft/sec)
%   E: energy density (N-m/m^2 or ft-lb/ft^2)
%   Ef: energy flux (N-m/sec-m or ft-lb/sec-ft)
%   Ur: Ursell number
%   eta: surface elevation (m or ft)
%   px: horizontal particle displacement (m or ft)
%   LOOK AT PZ AND PY
%   pz: vertical particle displacement (m or ft)
%   u: horizontal particle velocity (m/sec or ft/sec)
%   w: vertical particle velocity (m/sec or ft/sec)
%   dudt: horizontal particle acceleration (m/sec^2 or ft/sec^2)
%   dwdt: vertical particle accleration (m/sec^2 or ft/sec^2)
%   pres: pressure (N/m^2 or lb ft^2 )
%% -------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

% Single case input for metric measurments
if single_case
    [H] = USER_INPUT_DATA_VALUE(['Enter H: wave height (' labelUnitDist '): '], 0.1, 200);

    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (sec): ', 1.0, 1000.0);

    [d] = USER_INPUT_DATA_VALUE(['Enter d: water depth (' labelUnitDist '): '], 0.1, 5000.0);
    
    [z] = USER_INPUT_DATA_VALUE(['Enter z: vertical coordinate (' labelUnitDist '): '], -5100.0, 100.0);
    
    [xL] = USER_INPUT_DATA_VALUE('Enter xL: horizontal coordinate as fraction of wavelength (x/L): ', 0.0, 1.0);
    
    numCases = 1;
else
    multiCaseData = {...
        ['H: wave height (' labelUnitDist ')'], 0.1, 200;...
        'T: wave period (sec)', 1.0, 1000.0;...
        ['d: water depth (' labelUnitDist ')'], 0.1, 5000.0;...
        ['z: vertical coordinate (' labelUnitDist ')'], -5100.0, 100.0;...
        'xL: horizontal coordinate as fraction of wavelength (x/L)', 0.0, 1.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HList = varData(1, :);
    TList = varData(2, :);
    dList = varData(3, :);
    zList = varData(4, :);
    xLList = varData(5, :);
end


%% *********** Don't change anything here ******************

twopi=2*pi;
nIteration = 50;

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        d = dList(loopIndex);
        z = zList(loopIndex);
        xL = xLList(loopIndex);
    end
    
    [L,k]=WAVELEN(d,T,nIteration,g);

    theta=xL*twopi; %theta=(kx-wt) where arbitrarily t=0 and k=2*pi/L

    % Check for monochromatic wave breaking (depth limited - no slope)
    [Hb]=ERRWAVBRK1(d,0.78);
    assert(H<Hb,'Error: Input wave broken (Hb = %6.2f %s)',Hb,labelUnitDist)

    % Check to make sure vertical coordinate is within waveform
    eta=(H/2)*cos(theta);
    assert(z<eta && (z+d)>0,'Error: Point outside waveform.')

    % Main Computations
    arg=(2*k*d/(sinh(2*k*d)));
    tot=d+z;

    C=L/T;
    Cg=0.5*(1+arg)*C;
    E=(1/8)*rho*g*(H^2);
    Ef=E*Cg;
    Ur=L^2*H/(d^3);
    px=(-H/2)*(cosh(k*tot)/sinh(k*d))*sin(theta);
    py=(H/2)*(sinh(k*tot)/sinh(k*d))*cos(theta);
    u=(H*pi/T)*(cosh(k*tot)/sinh(k*d))*cos(theta);
    w=(H*pi/T)*(sinh(k*tot)/sinh(k*d))*sin(theta);
    dudt=(H*2*pi^2/(T^2))*(cosh(k*tot)/sinh(k*d))*sin(theta);
    dwdt=(-H*2*pi^2/(T^2))*(sinh(k*tot)/sinh(k*d))*cos(theta);
    pres=-rho*g*z+rho*g*(H/2)*(cosh(k*tot)/cosh(k*d))*cos(theta);

    fprintf('\t\t\t\t\t\t\t\t %s \n','Units');
    fprintf('%s \t\t\t %-6.2f \t %s \n','Wavelength',L,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f \t %s/s \n','Celerity',C,labelUnitDist);
    fprintf('%s \t\t %-6.2f \t %s/s \n','Group speed',Cg,labelUnitDist);
    fprintf('%s \t\t %-8.2f \t %s-%s/%s^2 \n','Energy density',E,labelUnitWt,labelUnitDist,labelUnitDist);
    fprintf('%s \t\t %-8.2f \t %s-%s/%s-s \n','Energy flux',Ef,labelUnitWt,labelUnitDist,labelUnitDist);
    fprintf('%s \t\t %-6.2f \n','Ursell number',Ur);
    fprintf('%s \t\t\t %-6.2f \t %s \n','Water Surface Elevation',eta,labelUnitDist);
    fprintf('%s \t %-6.2f \t %s \n','Horz. displacement',px,labelUnitDist);
    fprintf('%s \t %-6.2f \t %s \n','Vert. displacement',py,labelUnitDist);
    fprintf('%s \t\t %-6.2f \t %s/s \n','Horz. velocity',u,labelUnitDist);
    fprintf('%s \t\t %-6.2f \t %s/s \n','Vert. velocity',w,labelUnitDist);
    fprintf('%s \t %-6.2f \t %s/s^2 \n','Horz. acceleration',dudt,labelUnitDist);
    fprintf('%s \t %-6.2f \t %s/s^2 \n','Vert. acceleration',dwdt,labelUnitDist);
    fprintf('%s \t\t\t %-8.2f \t %s/%s^2 \n','Pressure',pres,labelUnitWt,labelUnitDist);

    if single_case
        %Plotting waveform
        plotxL=(-1:0.001:1);
        plottheta=plotxL*twopi;

        ploteta=(H/2)*cos(plottheta);
        plotu=(H*pi/T)*(cosh(k*tot)/sinh(k*d))*cos(plottheta);
        plotw=(H*pi/T)*(sinh(k*tot)/sinh(k*d))*sin(plottheta);

        figure(1)
        subplot(3,1,1); plot(plotxL,ploteta); ylim([min(ploteta)-1 max(ploteta)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Elevation [' labelUnitDist ']'])

        subplot(3,1,2); plot(plotxL,plotu); ylim([min(plotu)-1 max(plotu)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Velocity, u [' labelUnitDist '/s]'])

        subplot(3,1,3); plot(plotxL,plotw); ylim([min(plotw)-1 max(plotw)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Velocity, w [' labelUnitDist '/s]'])
        xlabel('x/L')
    end
end

% File Output
if single_case
    fileOutputArgs = {};
    [fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

    if fileOutputData{1}
        fId = fopen('output\linear_wave_theory.txt', 'wt');
        
        fprintf(fId, 'Linear Wave Theory Summary\n\n');
        
        fprintf(fId, 'Item\t\t\tValue\t\t\t %s \n','Units');
        fprintf(fId, '%s \t\t\t %-6.2f \t %s \n','Wavelength',L,labelUnitDist);
        fprintf(fId, '%s \t\t\t %-6.2f \t %s/s \n','Celerity',C,labelUnitDist);
        fprintf(fId, '%s \t\t %-6.2f \t %s/s \n','Group speed',Cg,labelUnitDist);
        fprintf(fId, '%s \t\t %-8.2f \t %s-%s/%s^2 \n','Energy density',E,labelUnitWt,labelUnitDist,labelUnitDist);
        fprintf(fId, '%s \t\t %-8.2f \t %s-%s/%s-s \n','Energy flux',Ef,labelUnitWt,labelUnitDist,labelUnitDist);
        fprintf(fId, '%s \t\t %-6.2f \n','Ursell number',Ur);
        fprintf(fId, '%s \t\t\t %-6.2f \t %s \n','Elevation',eta,labelUnitDist);
        fprintf(fId, '%s \t %-6.2f \t %s \n','Horz. displacement',px,labelUnitDist);
        fprintf(fId, '%s \t %-6.2f \t %s \n','Vert. displacement',py,labelUnitDist);
        fprintf(fId, '%s \t\t %-6.2f \t %s/s \n','Horz. velocity',u,labelUnitDist);
        fprintf(fId, '%s \t\t %-6.2f \t %s/s \n','Vert. velocity',w,labelUnitDist);
        fprintf(fId, '%s \t %-6.2f \t %s/s^2 \n','Horz. acceleration',dudt,labelUnitDist);
        fprintf(fId, '%s \t %-6.2f \t %s/s^2 \n','Vert. acceleration',dwdt,labelUnitDist);
        fprintf(fId, '%s \t\t\t %-8.2f \t %s/%s^2 \n','Pressure',pres,labelUnitWt,labelUnitDist);
        
        fclose(fId);
    end
end