clear all
clc

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

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

fprintf('%s \n\n','Calculation and slope type options: ');
fprintf('%s \n','Monochromatic Waves')
fprintf('%s \n','[1] Rough Slope <------------- Runup -------------> [2] Smooth Slope ')
fprintf('%s \n','[3] Rough Slope <----------- Overtopping ---------> [4] Smooth Slope ')
fprintf('%s \n\n','[5] Rough Slope <---- Runup and Overtopping ----> [6] Smooth Slope ')
fprintf('%s \n','Irregular Waves')
fprintf('%s \n\n','[7] Rough Slope <---- Runup and Overtopping ----> [8] Smooth Slope ')

option=input('Select option: ');

has_rough_slope = option==1 || option==5 || option ==7 || option==8;
has_overtopping = option>2;
has_runup = option ~= 3 && option ~= 4;
% numConsts = 0;
% if has_rough_slope
%     numConsts = numConsts + 2;
% end
% if has_overtopping
%     numConsts = numConsts + 3;
% end
% if ~has_runup
%     numConsts = numConsts + 1;
% end

conversionKnots2mph = 1.15077945; %1 knots = 1.15077945 mph

fprintf('\n');

% Single case input for metric measurments
if single_case
    [H] = USER_INPUT_DATA_VALUE(['Enter H: incident wave height (Hs for irregular waves) (' labelUnitDist '): '], 0.1, 100.0);
    
    [T] = USER_INPUT_DATA_VALUE(['Enter T: wave period (Tp for irregular waves) (' labelUnitDist '): '], 1.0, 1000.0);
    
    [cotphi] = USER_INPUT_DATA_VALUE('Enter cotphi: cotan of nearshore slope: ', 5.0, 10000.0);
    
    [ds] = USER_INPUT_DATA_VALUE(['Enter ds: water depth at structure toe (' labelUnitDist '): '], 0.1, 200.0);
    
    [cottheta] = USER_INPUT_DATA_VALUE('Enter cot \theta: cotan of structure slope (0.0 for vertical walls): ', 0.0, 30.0);
    
    [hs] = USER_INPUT_DATA_VALUE(['Enter hs: structure height above toe (' labelUnitDist '): '], 0.0, 200.0);

    numCases = 1;
    
else
     multiCaseData = {...
         ['H: wave height (' labelUnitDist ')'], 0.1, 100.0;...
          'T: wave period (sec)', 1.0, 1000.0;...
          'cotphi: cotan of nearshore slope', 5.0, 10000.0;...
         ['ds: water depth at structure toe (' labelUnitDist ')'], 0.1, 200.0;...
          'cottheta: cotan of structure slope (0.0 for vertical walls)', 0.0, 30.0;...
         ['hs: structure height above toe (' labelUnitDist ')'], 0.0, 200}; 
    
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HList = varData(1, :);
    TList = varData(2, :);
    cotphiList = varData(3, :);
    dsList = varData(4, :);
    cotthetaList = varData(5, :);
    hsList = varData(6, :);
end

if option == 3
    R_default = 15.0;
elseif option == 4
    R_default = 20.0;
else
    R_default = 0;
end
[roughSlopeCoeffData] = USER_INPUT_ROUGH_SLOPE_COEFFICIENTS(...
    has_rough_slope, has_overtopping, has_runup,...
    struct('numCases', numCases, 'R_default', R_default));

if isfield(roughSlopeCoeffData, 'a')
    a = roughSlopeCoeffData.a;
end
if isfield(roughSlopeCoeffData, 'b')
    b = roughSlopeCoeffData.b;
end
if isfield(roughSlopeCoeffData, 'alpha')
    alpha = roughSlopeCoeffData.alpha;
end
if isfield(roughSlopeCoeffData, 'Qstar0')
    Qstar0 = roughSlopeCoeffData.Qstar0;
end
if isfield(roughSlopeCoeffData, 'U')
    U = roughSlopeCoeffData.U;
end
if isfield(roughSlopeCoeffData, 'R')
    R = roughSlopeCoeffData.R;
end

exporter = EXPORTER('output/exporterRunupOvertopping.txt');

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/runup_overtopping.txt', 'wt');
end

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        cotphi = cotphiList(loopIndex);
        ds = dsList(loopIndex);
        cottheta = cotthetaList(loopIndex);
        hs = hsList(loopIndex);
        
        if isfield(roughSlopeCoeffData, 'aList')
            a = roughSlopeCoeffData.aList(loopIndex);
        end
        
        if isfield(roughSlopeCoeffData, 'bList')
            b = roughSlopeCoeffData.bList(loopIndex);
        end
        
        if isfield(roughSlopeCoeffData, 'alphaList')
            alpha = roughSlopeCoeffData.alphaList(loopIndex);
        end
        
        if isfield(roughSlopeCoeffData, 'Qstar0List')
            Qstar0 = roughSlopeCoeffData.Qstar0List(loopIndex);
        end
        
        if isfield(roughSlopeCoeffData, 'UList')
            U = roughSlopeCoeffData.UList(loopIndex);
        end
        
        if isfield(roughSlopeCoeffData, 'RList')
            R = roughSlopeCoeffData.RList(loopIndex);
        end
    end
    
    errorMsg = '';
    
    m=1/cotphi;

%     assert(ds<hs,'Error: Method does not apply to submerged structures.')
    if not(ds<hs)
        errorMsg = 'Error: Method does not apply to submerged structures.';
        disp(errorMsg);
    else
        [Hbs]=ERRWAVBRK2(T,m,ds);
%         assert(H<Hbs,'Error: Wave broken at structure (Hbs = %6.2f %s)',Hbs,labelUnitDist)
        if not (H<Hbs)
            errorMsg = sprintf('Error: Wave broken at structure (Hbs = %6.2f %s)',Hbs,labelUnitDist);
            disp(errorMsg);
        else
            [c,c0,cg,cg0,k,L,L0,reldep]=LWTGEN(ds,T,g);

            [steep,maxstp]=ERRSTP(H,ds,L);
%             assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
            if not(steep<maxstp)
                errorMsg = sprintf('Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep');
                disp(errorMsg);
            else
                [alpha0,H0]=LWTDWS(0,c,cg,c0,H);

                relht0=ds/H0;
                steep0=H0/(g*T^2);

                if cottheta==0
%                     assert(option~=1 && option~=5 && option~=7,'Error: Vertical wall cannot have rough slope.')
                    if not(option~=1 && option~=5 && option~=7)
                        errorMsg = 'Error: Vertical wall cannot have rough slope.';
                        disp(errorMsg);
                    else
                        theta=0.5*pi;
                        ssp=1000;
                    end
                else
                    theta=atan(1/cottheta);
                    ssp=(1/cottheta)/sqrt(H/L0);
                end

                if length(errorMsg) == 0
                    fprintf('%s \n','Deepwater')
                    fprintf('\t %s \t\t\t\t %-6.3f %s \n','Wave height, Hs0',H0,labelUnitDist)
                    fprintf('\t %s \t\t %-6.3f \n','Relative height, ds/H0',relht0)
                    fprintf('\t %s \t %-6.6f \n\n','Wave steepness, Hs0/(gT^2)',steep0)
                end
            end
        end
    end

    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end
        
        fprintf(fId, 'Input\n');
        fprintf(fId, 'H\t\t%6.2f %s\n', H, labelUnitDist);
        fprintf(fId, 'T\t\t%6.2f s\n', T);
        fprintf(fId, 'cotphi\t\t%6.2f\n', cotphi);
        fprintf(fId, 'ds\t\t%6.2f %s\n', ds, labelUnitDist);
        fprintf(fId, 'cottheta\t%6.2f\n', cottheta);
        fprintf(fId, 'hs\t\t%6.2f %s\n', hs, labelUnitDist);
        
        exportData = {H, T, cotphi, ds, cottheta, hs};
        
        if exist('a') == 1
            fprintf(fId, 'a\t\t%6.4f\n', a);
            exportData = [exportData {a}];
        end
        
        if exist('b') == 1
            fprintf(fId, 'b\t\t%6.4f\n', b);
            exportData = [exportData {b}];
        end
        
        if exist('alpha') == 1
            fprintf(fId, 'alpha\t\t%6.4f\n', alpha);
            exportData = [exportData {alpha}];
        end
        
        if exist('Qstar0') == 1
            fprintf(fId, 'Qstar0\t\t%6.4f\n', Qstar0);
            exportData = [exportData {Qstar0}];
        end
        
        if exist('U') == 1
            fprintf(fId, 'U\t\t%6.4f knots\n', U/conversionKnots2mph);
            exportData = [exportData {U/conversionKnots2mph}];
        end
        
        if exist('R') == 1
            fprintf(fId, 'R\t\t%6.4f %s\n', R, labelUnitDist);
            if ~has_runup
                exportData = [exportData {R}];
            end
        end
        
        if length(errorMsg) > 0
            fprintf(fId, '\n%s\n\n', errorMsg);
            exportData = [exportData {errorMsg}];
        else
            fprintf(fId, '\n%s \n','Deepwater');
            fprintf(fId, '\t %s \t\t %6.3f %s \n','Wave height, Hs0',H0,labelUnitDist);
            fprintf(fId, '\t %s \t %6.3f \n','Relative height, ds/H0',relht0);
            fprintf(fId, '\t %s \t %6.6f \n\n','Wave steepness, Hs0/(gT^2)',steep0);
            
            exportData = [exportData {H0, relht0, steep0}];
        end
    end
    
    if length(errorMsg) == 0
        freeb=hs-ds;

        if option==1
            [R]=RUNUPR(H,ssp,a,b);
            fprintf('%s \t %-6.3f %s \n\n','Runup',R,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s \n\n','Runup',R,labelUnitDist);
                exportData = [exportData {R}];
            end
        elseif option==2
            [R]=RUNUPS(H,L,ds,theta,ssp);
            fprintf('%s \t %-6.3f %s \n\n','Runup',R,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s \n\n','Runup',R,labelUnitDist);
                exportData = [exportData {R}];
            end
        elseif option==3   
            [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
            fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist);
                exportData = [exportData {Q}];
            end
        elseif option==4
            [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
            fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist);
                exportData = [exportData {Q}];
            end
        elseif option==5
            [R]=RUNUPR(H,ssp,a,b);
            [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
            fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
            fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s \n','Runup',R,labelUnitDist);
                fprintf(fId, '%s \t %6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist);
                exportData = [exportData {R, Q}];
            end
        elseif option==6
            [R]=RUNUPS(H,L,ds,theta,ssp);
            [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
            fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
            fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s \n','Runup',R,labelUnitDist);
                fprintf(fId, '%s \t %6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist);
                exportData = [exportData {R, Q}];
            end
        elseif option==7
            [R]=RUNUPR(H,ssp,a,b);
            [Q]=QOVERT_IRR(H0,freeb,R,Qstar0,alpha,theta,U,g);
            fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
            fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s \n','Runup',R,labelUnitDist);
                fprintf(fId, '%s \t %6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist);
                exportData = [exportData {R, Q}];
            end
        elseif option==8
            [R]=RUNUPS(H,L,ds,theta,ssp);
            [Q]=QOVERT_IRR(H0,freeb,R,Qstar0,alpha,theta,U,g);
            fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
            fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)

            if fileOutputData{1}
                fprintf(fId, '%s \t %6.3f %s \n','Runup',R,labelUnitDist);
                fprintf(fId, '%s \t %6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist);
                exportData = [exportData {R, Q}];
            end
        end
    end
    
    if fileOutputData{1}
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
        
        exporter.writeData(exportData);
    end
end

if fileOutputData{1}
    fclose(fId);
end

exporter.close();