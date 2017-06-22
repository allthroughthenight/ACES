clear all
clc

%% ACES Update to MATLAB BEACH NOURISMENT and OVERFILL RATIO
%-------------------------------------------------------------
% Evaluates the suitable of borrow material as beach fill and give overfill
% nourishment ratios. (Aces Tech Manual Chapter 6-4-1)

% Updated by: Yaprak Onat
% Date Created: June 21, 2016
% Date Modified:

% Requires the following functions:


% MAIN VARIABLE LIST:
%   INPUT
%  Vol_i = initial volume (yd^3 or m^3) Range 1 to 10^8
%   M_R = Native mean (phi, mm) Range -5 to 5
%   ro_n = native standard deviation (phi) Range 0.01 to 5
%   M_b = borrow mean (phi, mm) Range -5 to 5
%   ro_b = borrow standard deviation (phi) Range 0.01 to 5
%
%   OUTPUT
%   R_A = Overfill Ratio
%   Rj = Renourishment factor
%   Vol_D = Design Volume (yd^3 or m^3)

%   OTHERS
%   g: gravity [32.17 ft/s^2]
%   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs/ft^3]
%   rhos: density of sediment [5.14 slugs/ft^3 in FORTRAN source code]
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

if metric
     labelUnitVolumeRate = 'm^3';
     labelUnitGrain = 'mm';
else
     labelUnitVolumeRate = 'yd^3';
     labelUnitGrain = 'phi';
end

if single_case
       [Vol_i] = USER_INPUT_DATA_VALUE(['Enter Vol_i: initial volume (' labelUnitVolumeRate '): '], 1, 10^8);
       [M_R] = USER_INPUT_DATA_VALUE(['Enter M_R: Native mean (' labelUnitGrain '): '], -5.0, 5.0);
       [ro_n] = USER_INPUT_DATA_VALUE('Enter ro_n: Native standard deviation (phi): ', 0.01, 5.0);
       [M_b] = USER_INPUT_DATA_VALUE(['Enter M_b: Borrow mean (' labelUnitGrain '): '], -5.0, 5.0);
       [ro_b] = USER_INPUT_DATA_VALUE('Enter ro_b: Borrow standard deviation (phi): ', 0.01, 5.0);
       numCases = 1;
else
    multiCaseData = {...
            ['Vol_i: initial volume (' labelUnitVolumeRate ')'], 1, 10^8;...
            ['M_R: Native mean (' labelUnitGrain ')'], -5.0, 5.0;...
            'ro_n: Native standard deviation (phi)', 0.01, 5.0;...
            ['M_b: Borrow mean (' labelUnitGrain ')'], -5.0, 5.0;...
            'ro_b: Borrow standard deviation (phi)', 0.01, 5.0;};

    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);

    Vol_iList = varData(1, :);
    M_RList = varData(2, :);
    ro_nList = varData(3, :);
    M_bList = varData(4, :);
    ro_bLList = varData(5, :);
end

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/beach_nourishment.txt', 'wt');
end

for loopIndex = 1:numCases
    if ~single_case
        Vol_i = Vol_iList(loopIndex);
        M_R = M_RList(loopIndex);
        ro_n = ro_nList(loopIndex);
        M_b = M_bList(loopIndex);
        ro_b = ro_bLList(loopIndex);
    end

    catg= zeros; % category of the material according to table 6-4-1 in Aces manual

    if metric    % If Means are entered in mm, convert to phi units for computations.
        M_R = - ( log(M_R) / log(2.) );
        M_b = - ( log(M_b) / log(2.) );
    end

    % Relationships of phi means and pho standard deviations
    if ro_b>ro_n
        disp ('Borrow material is more poorly sorted than native material')
        if M_b>M_R
            disp('Borrow material is finer than native material')
            catg=1;
        else
            disp ('Borrow material is coarser than native material')
            catg=2;
        end
    else
        if M_b<M_R
           disp('Borrow material is coarser than native material')
           catg=3;
        else
           disp('Borrow material is finer than native material')
           catg=4;
        end
    end

    delta = (M_b-M_R)/ro_n; % phi mean difference
    sigma = ro_b/ro_n; % phi sorting ratio
    if sigma == 1
            theta_1=0;
            theta_2=inf;
    else
        % defining theta_1 and theta_2
        if catg == 1 || catg == 2
            theta_1 = max(-1, (-delta/(sigma^2-1)));
            theta_2 = inf;
        else
            theta_1 = -1;
            theta_2 = max(-1, (1+(2*delta/(1-sigma^2))));
        end
    end

    % calculate overfill ratio
    bk1 = (theta_1-delta)/sigma;
    fn1 = BOVERF(bk1);
    ft1 = BOVERF(theta_1);

    if theta_2 == inf
       fn3 = ((1.0-ft1)/sigma)*exp(0.5*(theta_1^2-bk1^2));
       R_A = 1.0/(fn1+fn3);
    else
        bk2 = (theta_2-delta)/sigma;
        fn2 = BOVERF(bk2);
        ft2 = BOVERF(theta_2);
        fn3 = ((ft2-ft1)/sigma)*exp(0.5*(theta_1^2-bk1^2));
        R_A  = 1.0/(1-fn2+fn1+fn3);
    end

    assert(R_A>=1.0,'Error: Overfill ratio (R_A) < 1.0 Respecify data',R_A)

    R_j = exp((delta-0.5*((ro_b^2/ro_n^2)-1)));

    Vol_D = R_A * Vol_i;

    fprintf('%s \t\t\t %-6.2f \t \n','Overfill Ratio, R_A',R_A);
    fprintf('%s \t\t %-6.2f \t \n','Renourishment factor, R_j',R_j);
    fprintf('%s \t\t\t %-6.2f %s \t \n','Design Volume, Vol_D',Vol_D,labelUnitVolumeRate);

    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end

        fprintf(fId, 'Input\n');
        fprintf(fId, 'Vol_i\t%6.2f %s\n', Vol_i, labelUnitVolumeRate);
        fprintf(fId, 'M_R\t%6.2f %s\n', M_R, labelUnitGrain);
        fprintf(fId, 'ro_n\t%6.2f\n', ro_n);
        fprintf(fId, 'M_b\t%6.2f %s\n', M_b, labelUnitGrain);
        fprintf(fId, 'ro_b\t%6.2f\n\n', ro_b);

        fprintf(fId, '%s \t\t %6.2f \t \n','Overfill Ratio, R_A',R_A);
        fprintf(fId, '%s \t %6.2f \t \n','Renourishment factor, R_j',R_j);
        fprintf(fId, '%s \t\t %6.2f %s \t \n','Design Volume, Vol_D',Vol_D,labelUnitVolumeRate);

        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
    end
end

if fileOutputData{1}
    fclose(fId);
end
