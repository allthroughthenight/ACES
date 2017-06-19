clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Fourier Series Wave Theory (page 2-3 of ACES User's
% Guide). Yields various parameters for progressive waves of permanent
% form as predicted by Fourier series approximation. Provies estimates
% for common engineering parameters such as water surface elevation,
% integral wave properties, and kinematics as functions of wave height,
% period, water depth, and position in the wave form which is assumed to
% exist on a uniform co-flowing current.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: July 1, 2011
% Date Modified:

% Requires the following functions:
% ERRWAVBRK
% FWTPRE

% MAIN VARIABLE LIST:
%   INPUT
%   H: wave height
%   d: water depth
%   T: wave period
%   celdef: celerity defintion
%   u: mean velocity
%   nofour: number of terms in Fourier series
%   nosteps: number of steps in wave height ramping

%   OUTPUT
%   c: celerity
%   L: wavelength
%   eul: mean Eulerian fluid velocity
%   mass: mean mass transport velocity
%   rel2wave: mean velocity relative to wave
%   flux: volume flux
%   B: Bernoulli constant
%   I: impulse
%   Ek: kinetic energy
%   Ep: potential energy
%   Etot: energy density
%   ub: mean square of bed velocity
%   Sxx: radiation stress
%   F: wave power (energy flux)
%   Q: volume flux

%   OTHERS
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

% if single_case
%     [H] = USER_INPUT_DATA_VALUE(['Enter H: wave height (' labelUnitDist '): '], 0.1, 200.0);
% 
%     [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (s): ', 1.0, 1000.0);
% 
%     [d] = USER_INPUT_DATA_VALUE(['Enter d: water depth (' labelUnitDist '): '], 0.1, 5000.0);
% 
%     [celdef] = USER_INPUT_FINITE_CHOICE('Enter celdef: celerity definition (1 for Euler, 2 for Stokes): ', {'1', '2'});
% 
%     [u] = USER_INPUT_DATA_VALUE(['Enter u: mean velocity (' labelUnitDist 'ps): '], 0.0, 10.0);
% 
%     [nofour] = USER_INPUT_DATA_VALUE('Enter nofour: the number of terms in Fourier Series: ', 1, 25);
% 
%     [nstep] = USER_INPUT_DATA_VALUE('Enter nsteps: the number of steps in Wave Height ramping: ', 1, 10);
% 
%      numCases = 1;
%      
% else % multicase 
%     multiCaseData = {...
%             ['H: wave height (' labelUnitDist ')'], 0.1, 200.0;...
%             'T: wave period (sec)', 1.0, 1000.0;...
%             ['d: water depth (' labelUnitDist ')'], 0.1, 5000.0;...
%             'celdef: celerity definition (1 for Euler, 2 for Stokes)', 1,2;...
%             ['u: mean velocity (' labelUnitDist 'ps)'], 1.0, 10.0;...
%             'nofour: the number of terms in Fourier Series: ', 1, 25;...
%             'nsteps: the number of steps in Wave Height ramping: ', 1, 10};
% 
%     [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
%     
%     HList = varData(1, :);
%     TList = varData(2, :);
%     dList = varData(3, :);
%     celdefList = varData(4, :);
%     uList = varData(5, :);
%     nofourList = varData(6, :);
%     nstepsList = varData(7, :);
% end

H = 6;
T = 10;
d = 20;
celdef = 2;
u = 0;
nofour = 18;
nstep = 4;
numCases = 1;

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        d = dList(loopIndex);
        celdef = celdefList(loopIndex);
        uL = uLList(loopIndex);
        nofour = nofourList(loopIndex);
        nstep = nostepsList(loopIndex);
    end
      
    [Hnon,L,Hoverd,unon, deptyp]=FWTPRE(g,T,H,d,u); %Convert dimensional input data to nondimensional data.
    [Hbs]=ERRWAVBRK1(d,0.75); 
    assert(H<Hbs,'Error: Input wave broken (Hb = %6.2f %s)',Hbs,labelUnitDist)
    [ dpi, dhe, dho, sol, z, rhs1, rhs2, b, cosa ] =...
        FWTCALC( Hnon,Hoverd,unon, nstep, nofour, d, L, deptyp, celdef );
    
    % determine overall wave results
    [k, C, L, u_e, u_mt, u_m, q, r, I, Ek, Ep, E, Ub2, Sxx, Ef, Q, R, ft ] = FWTRSLT( z, nofour, H, g, rho, cosa, deptyp, d );
    
    %* if you find hlimit function 
    %* assert(H<=Hmax, 'ERROR: Limit wave exceeded')
    
    fprintf('%s \t\t\t %-6.2f %s/sec \t \n','Celerity',C,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s \t \n','Wavelength',L,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s/sec \t \n','Mean Eularian fluid velocity',u_e,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s/sec \t \n','Mean mass transport velocity',u_mt,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s/sec \t \n','Mean velocity relative to wave',u_m,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s^2/sec \t \n','Volume flux due to wave',q,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s^2/sec^2 \t \n','Bernoulli constant',r,labelUnitDist);
    fprintf('----Integral Parameters ----- \n')
    fprintf('%s \t\t\t %-6.2f %s-sec/%s^2 \t \n','Impulse',I,labelUnitWt, labelUnitDist);
    fprintf('%s \t\t %-8.2f %s-%s/%s^2 \t \n','Kinetic energy',Ek,labelUnitDist,labelUnitWt,labelUnitDist);
    fprintf('%s \t\t %-8.2f %s-%s/%s^2 \t \n','Potential energy',Ep,labelUnitDist,labelUnitWt,labelUnitDist);
    fprintf('%s \t\t %-8.2f %s-%s/%s^2 \t \n','Energy density',E,labelUnitDist,labelUnitWt,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s^2/sec^2 \t \n','Mean square of bed velocity',Ub2,labelUnitDist);
    fprintf('%s \t\t %-8.2f %s-%s/%s^2 \t \n','Radiation stress',Sxx,labelUnitDist,labelUnitWt,labelUnitDist);
    fprintf('%s \t\t %-8.2f %s-%s/sec-%s \t \n','Energy flux (wave power)',Ef,labelUnitDist,labelUnitWt,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s^2/sec \t \n','Volume flux',Q,labelUnitDist);
    fprintf('%s \t\t\t %-6.2f %s^2/sec^2 \t \n','Bernoulli constant',R,labelUnitDist);   
    
    fprintf('-------------')
    fprintf('Solution surface elevations %s %-6.2f \t %-6.2f', labelUnitDist,(z(10)/k), (z(nofour+10)/k) );
    fprintf('Fourier series coefficients b(i) i=1... %-6.2f', nofour )
        for i= 1:nofour
            fprintf('%-6.8f\n',z(i+nofour+10) )
        end 
    
    
    
    [kinematics] = USER_INPUT_FINITE_CHOICE(...
        'Do you want to display kinematics at point of interest ((Y)es or (N)o): ',...
        {'Y', 'y', 'N', 'n'});
    
    while strcmp(kinematics, 'Y') || strcmp(kinematics, 'y')
        [xL] = USER_INPUT_DATA_VALUE('Enter xL: horizontal coordinate as fraction of wavelength (x/L): ', 0.0, 1.0);
        [y] = USER_INPUT_DATA_VALUE(['Enter z: vertical coordinate (' labelUnitDist '): '], -5100.0, 100.0);

        [ ubig, wbig, ax, ay, pbig, eta ] = FWTKIN( xL, y, dpi, nofour, k, d,  z, ft, deptyp, g, rho );

        fprintf('%s \t\t %-6.2f %s/sec \t \n','Horz. velocity',ubig,labelUnitDist);
        fprintf('%s \t\t %-6.2f %s/sec \t \n','Vert. velocity',wbig,labelUnitDist);
        fprintf('%s \t %-6.2f %s/sec^2 \t \n','Horz. acceleration',ax,labelUnitDist);
        fprintf('%s \t %-6.2f %s/sec^2 \t \n','Vert. acceleration',ay,labelUnitDist);
        fprintf('%s \t\t\t %-8.2f %s/%s^2 \t \n','Pressure',pbig,labelUnitWt,labelUnitDist);
        fprintf('%s \t\t\t %-6.2f %s \t \n','Elevation',eta,labelUnitDist);
        
        [kinematics] = USER_INPUT_FINITE_CHOICE(...
            'Do you want to display kinematics at point of interest ((Y)es or (N)o): ',...
            {'Y', 'y', 'N', 'n'});
    end
      


%             if single_case
%             %Plotting waveform
%             CALL FWTPLD 
%             Use graphics routine to display plot data.
%             CALL FWTPLT (-D*LENFAC)


end

    if single_case
        fileOutputArgs = {'Enter the filename (no extension): ', 'Enter the description for this file: '};
        [fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

        if fileOutputData{1}
            fId = fopen(['output\' fileOutputData{2} '.txt'], 'wt');

            fprintf(fId, 'Kinematics at z for %s\n\n', fileOutputData{3});
            fprintf(fId, 'X/L \tETA (%s) \tU (%s/sec) \tW (%s/sec) \tPressure (%s/%s^2) \ta_x (%s/sec^2) \ta_z (%s/sec) \n',labelUnitDist,labelUnitDist,labelUnitDist,labelUnitWt,labelUnitDist, labelUnitDist,labelUnitDist);

            for loopIndex = 1:length(plotxL)
                fprintf(fId, '%-6.3f\t%-6.3f\t\t%-6.3f\t\t%-6.3f\n',...
                    plotxL(loopIndex),...
                    ploteta(loopIndex),...
                    plotu(loopIndex),...
                    plotw(loopIndex)), ...
                    plotpress(loopIndex),...
                    plotax(loopIndex),...
                    plotay(loopIndex)
            end
        end
    end

  
