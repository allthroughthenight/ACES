clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Lineat Wave Theory with Snell's Law (page 3-1 in ACES User's Guide)
% Provides a simple estimate for wave shoaling and refraction using Snell's
% Law with wave properties predicted by linear wave theory

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 11, 2011
% Date Verified: June 6, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK1
% ERRWAVBRK3
% LWTDWS
% LWTGEN
% LWTTWM
% LWTTWS
% ERRWAVBRK3
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   H1: wave height at known location (m)
%   T: wave period at known location (sec)
%   d1: water depth at known location (m)
%   alpha1: wave crest angle (deg)
%   cotphi: cotan of nearshore slope
%   d2: water depth at desired location (m)

%   OUTPUT
%   H0: deepwater wave height (m)
%   H2: wave height at subject location (m)
%   alpha0: deepwater wave crest angle (deg)
%   alpha2: wave crest angle at subject location (deg)
%   L0: deepwater wavelength (m)
%   L1: wavelength at known location (m)
%   L2: wavelength at subject location (m)
%   c1: wave celerity at known location (m/s)
%   c0: deepwater wave celerity (m/s)
%   c2: wave celerity at subject location (m/s)
%   cg1: group speed at known location (m/s)
%   cg0: deepwater group speed (m/s)
%   cg2: group speef at subject location (m/s)
%   E1: energy density at known location (N-m/m^2)
%   E0: deepwater energy density (N-m/m^2)
%   E2: enery density at subject location (N-m/m^2)
%   P1: energy flux at known location (N-m/m-s)
%   P0: deepwater wave flux (N-m/m-s)
%   P2: wave flux at subject location (N-m/m-s)
%   HL: deepwater wave steepness
%   Ur1: Ursell number at known location
%   Ur2: Ursell number at desired location
%   Hb: breaking wave height (m)
%   db: breaking wave depth (m)
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

% Single case input
if single_case
    [H1] = USER_INPUT_DATA_VALUE(['Enter H1: wave height at known location (' labelUnitDist '): '], 0.1, 200.0);
    
    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period at known location (sec): ', 1.0, 1000.0);

    [d1] = USER_INPUT_DATA_VALUE(['Enter d1: water depth at known location (' labelUnitDist '): '], 0.1, 5000.0);
    
    [alpha1] = USER_INPUT_DATA_VALUE('Enter alpha1: wave crest angle (deg): ', 0.0, 90.0);
    
    [cotphi] = USER_INPUT_DATA_VALUE('Enter cotphi: cotan of nearshore slope: ', 5.0, 1000.0);
    
    [d2] = USER_INPUT_DATA_VALUE(['Enter d2: water depth at desired location (' labelUnitDist '): '], 0.1, 5000.0);
    
    numCases = 1;
else
    multiCaseData = {...
        ['H1: wave height at known location (' labelUnitDist ')'], 0.1, 200.0;...
        'T: wave period at known location (sec)', 1.0, 1000.0;...
        ['d1: water depth at known location (' labelUnitDist ')'], 0.1, 5000.0;...
        'alpha1: wave crest angle (deg)', 0.0, 90.0;...
        'cotphi: cotan of nearshore slope', 5.0, 1000.0;...
        ['d2: water depth at desired location (' labelUnitDist ')'], 0.1, 5000.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    H1List = varData(1, :);
    TList = varData(2, :);
    d1List = varData(3, :);
    alpha1List = varData(4, :);
    cotphiList = varData(5, :);
    d2List = varData(6, :);
end

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output\snells_law.txt', 'wt');
    exporter = EXPORTER('output/exporterSnellsLaw');
end

for loopIndex = 1:numCases
    if ~single_case
        H1 = H1List(loopIndex);
        T = TList(loopIndex);
        d1 = d1List(loopIndex);
        alpha1 = alpha1List(loopIndex);
        cotphi = cotphiList(loopIndex);
        d2 = d2List(loopIndex);
    end
    
    errorMsg = '';
    
    %rho=1.989;
    m=1/cotphi;

    [Hb]=ERRWAVBRK1(d1,0.78);
%     assert(H1<Hb,'Error: Known wave broken (Hb = %6.2f %s)',Hb,labelUnitDist)
    if not(H1<Hb)
        errorMsg = sprintf('Error: Known wave broken (Hb = %6.2f %s)',Hb,labelUnitDist);
        disp(errorMsg);
    else
        %determine known wave properties
        [c1,c0,cg1,cg0,k1,L1,L0,reldep1]=LWTGEN(d1,T,g);
        [E1,P1,Ur1,setdown1]=LWTTWM(cg1,d1,H1,L1,reldep1,rho,g,k1);

        [steep,maxstp]=ERRSTP(H1,d1,L1);
%         assert(steep<maxstp,'Error: Known wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
        if not(steep<maxstp)
            errorMsg = sprintf('Error: Known wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep');
            disp(errorMsg);
        else
            %determine deepwater wave properties
            [alpha0,H0,errorMsg]=LWTDWS(alpha1,c1,cg1,c0,H1);
            if length(errorMsg) > 0
                disp(errorMsg);
            else
                E0=(1/8)*rho*g*(H0^2);
                P0=E0*cg0;
                HL=H0/L0;

    %             assert(HL<(1/7),'Error: Deepwater wave unstable, [H0/L0] > (1/7)')
                if not(HL<(1/7))
                    errorMsg = 'Error: Deepwater wave unstable, [H0/L0] > (1/7)';
                    disp(errorMsg);
                else
                    %determine subject wave properties
                    [c2,c0,cg2,cg0,k2,L2,L0,reldep2]=LWTGEN(d2,T,g);
                    [alpha2,H2,kr,ks]=LWTTWS(alpha0,c2,cg2,c0,H0);
                    [E2,P2,Ur2,setdown2]=LWTTWM(cg2,d2,H2,L2,reldep2,rho,g,k2);

                    [Hb,db]=ERRWAVBRK3(H0,L0,T,m);
    %                 assert(H2<Hb,'Error: Subject wave broken (Hb = %6.2f m, hb = %6.2f %s)',Hb,db,labelUnitDist)
                    if not(H2<Hb)
                        errorMsg = sprintf('Error: Subject wave broken (Hb = %6.2f %s, hb = %6.2f %s)',Hb,labelUnitDist,db,labelUnitDist);
                        disp(errorMsg);
                    else
                        [steep,maxstp]=ERRSTP(H2,d2,L2);
        %                 assert(steep<maxstp,'Error: Subject wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
                        if not(steep<maxstp)
                            errorMsg = sprintf('Error: Subject wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep');
                            disp(errorMsg);
                        else
                            fprintf('\t\t\t\t\t %s \t\t %s \t\t %s \t\t %s\n','Known','Deepwater','Subject','Units');
                            fprintf('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t %s \n','Wave height',H1,H0,H2,labelUnitDist)
                            fprintf('%s \t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t deg \n','Wave crest angle',alpha1,alpha0,alpha2)
                            fprintf('%s \t\t\t %-5.2f \t %-5.2f \t\t %-5.2f \t\t %s \n','Wavelength',L1,L0,L2,labelUnitDist)
                            fprintf('%s \t\t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t %s/s \n','Celerity',c1,c0,c2,labelUnitDist)
                            fprintf('%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t %s/s \n','Group speed',cg1,cg0,cg2,labelUnitDist)
                            fprintf('%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t %s-%s/%s^2 \n','Energy density',E1,E0,E2,labelUnitDist,labelUnitWt,labelUnitDist)
                            fprintf('%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t %s-%s/sec-%s \n','Energy flux',P1,P0,P2,labelUnitDist,labelUnitWt,labelUnitDist)
                            fprintf('%s \t\t %-5.2f \t\t\t\t\t\t %-5.2f \n','Ursell number',Ur1,Ur2)
                            fprintf('%s \t\t\t\t\t %-5.2f \n','Wave steepness',HL)
                            fprintf('\n')
                            fprintf('%s \t\t\t\n','Breaking parameters')
                            fprintf('%s \t\t %-5.2f %s \t\n','Breaking height',Hb,labelUnitDist)
                            fprintf('%s \t\t\t %-5.2f %s \t\n','Breaking depth',db,labelUnitDist)
                        end
                    end
                end
            end
        end
    end
    
    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end
        
        fprintf(fId, 'Input\n');
        fprintf(fId, 'H1\t%6.2f %s\n', H1, labelUnitDist);
        fprintf(fId, 'T\t%6.2f s\n', T);
        fprintf(fId, 'd1\t%6.2f %s\n', d1, labelUnitDist);
        fprintf(fId, 'alpha1\t%6.2f deg\n', alpha1);
        fprintf(fId, 'cotphi\t%6.2f\n', cotphi);
        fprintf(fId, 'd2\t%6.2f %s\n\n', d2, labelUnitDist);
        
        if length(errorMsg) > 0
            fprintf(fId, '%s\n', errorMsg);
        else
            fprintf(fId, '\t\t\t %s \t\t %s \t\t %s \t\t %s\n','Known','Deepwater','Subject','Units');
            fprintf(fId, '%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t %s \n','Wave height',H1,H0,H2,labelUnitDist);
            fprintf(fId, '%s \t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t deg \n','Wave crest angle',alpha1,alpha0,alpha2);
            fprintf(fId, '%s \t\t %-5.2f \t %-5.2f \t\t %-5.2f \t\t %s \n','Wavelength',L1,L0,L2,labelUnitDist);
            fprintf(fId, '%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t %s/s \n','Celerity',c1,c0,c2,labelUnitDist);
            fprintf(fId, '%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \t\t\t %s/s \n','Group speed',cg1,cg0,cg2,labelUnitDist);
            fprintf(fId, '%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t %s-%s/%s^2 \n','Energy density',E1,E0,E2,labelUnitDist,labelUnitWt,labelUnitDist);
            fprintf(fId, '%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \t\t %s-%s/sec-%s \n','Energy flux',P1,P0,P2,labelUnitDist,labelUnitWt,labelUnitDist);
            fprintf(fId, '%s \t\t %-5.2f \t\t\t\t\t %-5.2f \n','Ursell number',Ur1,Ur2);
            fprintf(fId, '%s \t\t %-5.2f \n','Wave steepness',HL);
            fprintf(fId, '\n');
            fprintf(fId, '%s \t\t\t\n','Breaking parameters');
            fprintf(fId, '%s \t %-5.2f %s \t\n','Breaking height',Hb,labelUnitDist);
            fprintf(fId, '%s \t\t %-5.2f %s \t\n','Breaking depth',db,labelUnitDist);
        end
        
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
        
        exportData = {H1, T, d1, alpha1, cotphi, d2};
        if length(errorMsg) > 0
            exportData = [exportData {errorMsg}];
        else
            exportData = [exportData {H1,H0,H2,alpha1,alpha0,alpha2,...
                L1,L0,L2,c1,c0,c2,cg1,cg0,cg2,E1,E0,E2,P1,P0,P2,...
                Ur1,Ur2,HL,Hb,db}];
        end
        exporter.writeData(exportData);
    end
end

if fileOutputData{1}
    fclose(fId);
    exporter.close();
end