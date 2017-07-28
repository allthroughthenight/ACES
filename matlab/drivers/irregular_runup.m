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

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

if single_case
    [Hs0] = USER_INPUT_DATA_VALUE(['Enter Hs0: deepwater significant wave height (' labelUnitDist '): '], 0.1, 100.0);
    
    [Tp] = USER_INPUT_DATA_VALUE('Enter Tp: peak energy wave period (sec): ', 0.1, 100.0);
    
    [cottheta] = USER_INPUT_DATA_VALUE('Enter cottheta: cotangent of foreshore slope: ', 0.1, 100.0);
    
    numCases = 1;
else
    multiCaseData = {...
        ['Hs0: deepwater significant wave height (' labelUnitDist ')'], 0.1, 100.0;...
        'Tp: peak energy wave period (sec)', 0.1, 100.0;...
        'cottheta: cotangent of foreshore slope', 0.1, 100.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    Hs0List = varData(1, :);
    TpList = varData(2, :);
    cotthetaList = varData(3, :);
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

exporter = EXPORTER('output/exporterIrregularRunup.txt');

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/irregular_runup.txt', 'wt');
end

for loopIndex = 1:numCases
    if ~single_case
        Hs0 = Hs0List(loopIndex);
        Tp = TpList(loopIndex);
        cottheta = cotthetaList(loopIndex);
    end
    
    errorMsg = '';
    
    L0=g*(Tp^2)/(2*pi);
    steep=Hs0/L0;
%     assert(steep<0.142,'Error: Input wave unstable (Max: 0.142, [H/L] = %0.4f)',steep')
    if not(steep<0.142)
        errorMsg = sprintf('Error: Input wave unstable (Max: 0.142, [H/L] = %0.4f)',steep');
        disp(errorMsg);
    else
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
        fprintf('%s \t\t\t\t\t %-6.2f %s \n','Average runup',Ravg,labelUnitDist)
    end

    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end
        
        fprintf(fId, 'Input\n');
        fprintf(fId, 'Hs0\t\t%6.2f %s\n', Hs0, labelUnitDist);
        fprintf(fId, 'Tp\t\t%6.2f s\n', Tp);
        fprintf(fId, 'cottheta\t%6.2f\n\n', cottheta);
        
        if length(errorMsg) > 0
            fprintf(fId, '%s', errorMsg);
        else
            fprintf(fId, '%s \t\t\t %6.2f %s \n','Maximum runup',Rmax,labelUnitDist);
            fprintf(fId, '%s \t %6.2f %s \n','Runup exceeded by 2% of runup',R2,labelUnitDist);
            fprintf(fId, '%s \t %6.2f %s \n','Avg. of highest 1/10 runups',R110,labelUnitDist);
            fprintf(fId, '%s \t %6.2f %s \n','Avg. of highest 1/3 runups',R13,labelUnitDist);
            fprintf(fId, '%s \t\t\t %6.2f %s \n','Average runup',Ravg,labelUnitDist);
        end
        
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
        
        exportData = {Hs0, Tp, cottheta};
        if length(errorMsg) > 0
            exportData = [exportData {errorMsg}];
        else
            exportData = [exportData {Rmax, R2, R110, R13, Ravg}];
        end
        exporter.writeData(exportData);
    end
end

if fileOutputData{1}
    fclose(fId);
end

exporter.close();