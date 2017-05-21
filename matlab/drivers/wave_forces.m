clc
clear all
set(0,'ShowHiddenHandles','on')
delete(get(0,'Children'))

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Nonbreaking Wave Forces at Vertical Walls (page 4-3 of ACES 
% User's Guide). Provides pressure distribution and resultant force and
% moment loading on a vertical wall caused by normally incident, nonbreaking,
% regular waves as proposed by Sainflou (1928), Miche (1944), and Rundgren
% (1958). 

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: May 17, 2011
% Date Verified: June 1, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK1
% ERRWAVBRK2
% WAVELEN
% WFVW1
% WFVW2
% WFVW3
% WFVW4

% MAIN VARIABLE LIST:
%   INPUT
%   d: depth for sea water level
%   Hi: incident wave height
%   T: wave period
%   chi: wave reflection coefficient
%   cotphi: cotangent of nearshore slope

%   OUTPUT
%   MR: array containing Miche-Rundgren integrated values
%       (1) particle height above bottom at crest
%       (2) integrated force at crest
%       (3) integrated moment about base at crest
%       (4) particle height above bottom at trough
%       (5) integrate force at trough
%       (6) integrated moment about bottom at trough
%   S: array containing Sainflou integrated values
%   MRintc: array containing Miche-Rundgren incremental values at crest
%       (1) particle height
%       (2) wave pressure
%       (3) hydrostatic pressure
%       (4) wave and hydrostatic pressure
%       (5) moment
%   MRintt: array containing Miche-Rundgren incremental values at trough
%   Sintc: array containing Sainflou incremental values at crest
%   Sintt: array containing Sainflou incremental values at trough
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

%rho=1.989; %slugs/ft^3 (sea water)
H20weight=rho*g;

if single_case
    [d] = USER_INPUT_DATA_VALUE(['Enter d: depth for sea water level (' labelUnitDist '): '], 0.1, 200.0);
    
    [Hi] = USER_INPUT_DATA_VALUE(['Enter Hi: incident wave height (' labelUnitDist '): '], 0.1, 100.0);
    
    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (s): ', 1.0, 100.0);
    
    [chi] = USER_INPUT_DATA_VALUE('Enter chi: wave reflection coefficient: ', 0.9, 1.0);
    
    [cotphi] = USER_INPUT_DATA_VALUE('Enter cotphi: cotangent of nearshore slope: ', 5.0, 10000.0);
    
    numCases = 1;
else
    multiCaseData = {...
        ['d: depth for sea water level (' labelUnitDist ')'], 0.1, 200.0;...
        ['Hi: incident wave height (' labelUnitDist ')'], 0.1, 100.0;...
        'T: wave period (s)', 1.0, 100.0;...
        'chi: wave reflection coefficient', 0.9, 1.0;...
        'cotphi: cotangent of nearshore slope', 5.0, 10000.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    dList = varData(1, :);
    HiList = varData(2, :);
    TList = varData(3, :);
    chiList = varData(4, :);
    cotphiList = varData(5, :);
end

for loopIndex = 1:numCases
    if ~single_case
        d = dList(loopIndex);
        Hi = HiList(loopIndex);
        T = TList(loopIndex);
        chi = chiList(loopIndex);
        cotphi = cotphiList(loopIndex);
    end
    
    m=1/cotphi;

    if m==0
        [Hbs]=ERRWAVBRK1(d,0.78);
    else
        [Hbs]=ERRWAVBRK2(T,m,d);
    end

    assert(Hi<Hbs,'Error: Wave broken at structure (Hbs = %6.2f m)',Hbs)

    [L,k]=WAVELEN(d,T,50,g);

    [steep,maxstp]=ERRSTP(Hi,d,L);
    assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

    [MR,S,MRintc,MRintt,Sintc,Sintt]=WFVW1(d,Hi,chi,L,H20weight);
    fprintf('\n\t\t\t\t\t\t %s \t\t\t %s \n','Miche-Rundgren','Sainflou')
    fprintf('%s \t %s \t\t %s \t\t %s \t\t %s \n','Wave Position at Wall','Crest','Trough','Crest','Trough')
    fprintf('%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \n','Hgt above bottom',MR(1),MR(4),S(1),S(4))
    fprintf('%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \n','Integrated force',MR(2),MR(5),S(2),S(5))
    fprintf('%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \n','Integrated moment',MR(3),MR(6),S(3),S(6))

    if single_case
        figure(1)
        subplot(2,1,1); plot(MRintc(:,2),MRintc(:,1),'k-',MRintc(:,3),MRintc(:,1),'k--',MRintc(:,4),MRintc(:,1),'k:')
        legend('Wave Pressure','Hyrdostatic Pressure','Wave and Hydrostatic Pressue')
        xlabel('Pressure [lb/ft^2]')
        ylabel('Elevation [ft]')
        title('Miche-Rundgren Pressure Distribution - Crest at Wall')
        hold on
        hline = refline([0 0]);
        set(hline,'LineStyle','--')
        hold off

        subplot(2,1,2); plot(MRintt(:,2),MRintt(:,1),'k-',MRintt(:,3),MRintt(:,1),'k--',MRintt(:,4),MRintt(:,1),'k:')
        legend('Wave Pressure','Hydrostatic Pressure','Wave and Hydrostatic Pressue')
        xlabel('Pressure [lb/ft^2]')
        ylabel('Elevation [ft]')
        title('Miche-Rundgren Pressure Distribution - Trough at Wall')
        hold on
        hline = refline([0 0]);
        set(hline,'LineStyle','--')
        rectangle('Position',[-50,floor(min(Sintt(:,1))),50,abs(floor(min(Sintt(:,1))))+5],'LineWidth',2)
        hold off
        ylim([floor(min(Sintt(:,1))) abs(floor(min(Sintt(:,1))))-5])

        figure(2)
        subplot(2,1,1); plot(Sintc(:,2),Sintc(:,1),'k-',Sintc(:,3),Sintc(:,1),'k--',Sintc(:,4),Sintc(:,1),'k:')
        legend('Wave Pressure','Hyrdostatic Pressure','Wave and Hydrostatic Pressue')
        xlabel('Pressure [lb/ft^2]')
        ylabel('Elevation [ft]')
        title('Sainflou Pressure Distribution - Crest at Wall')
        hold on
        hline = refline([0 0]);
        set(hline,'LineStyle','--')
        hold off

        subplot(2,1,2); plot(Sintt(:,2),Sintt(:,1),'k-',Sintt(:,3),Sintt(:,1),'k--',Sintt(:,4),Sintt(:,1),'k:')
        legend('Wave Pressure','Hydrostatic Pressure','Wave and Hydrostatic Pressue')
        xlabel('Pressure [lb/ft^2]')
        ylabel('Elevation [ft]')
        title('Sainflou Pressure Distribution - Trough at Wall')
        hold on
        hline = refline([0 0]);
        set(hline,'LineStyle','--')
        rectangle('Position',[-50,floor(min(Sintt(:,1))),50,abs(floor(min(Sintt(:,1))))+5],'LineWidth',2)
        hold off
        ylim([floor(min(Sintt(:,1))) abs(floor(min(Sintt(:,1))))-5])
    end
end