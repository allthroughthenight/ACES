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

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

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

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
	fId = fopen('output/wave_forces.txt', 'wt');
  
  exporter = EXPORTER('output/exporterWaveForces');
end

for loopIndex = 1:numCases
    if ~single_case
        d = dList(loopIndex);
        Hi = HiList(loopIndex);
        T = TList(loopIndex);
        chi = chiList(loopIndex);
        cotphi = cotphiList(loopIndex);
    end
    
	errorMsg = '';
	
    m=1/cotphi;

    if m==0
        [Hbs]=ERRWAVBRK1(d,0.78);
    else
        [Hbs]=ERRWAVBRK2(T,m,d);
    end

%     assert(Hi<Hbs,'Error: Wave broken at structure (Hbs = %6.2f %s)', Hbs, labelUnitDist);
	if Hi >= Hbs
		errorMsg = sprintf('Error: Wave broken at structure (Hbs = %6.2f %s)',...
			Hbs, labelUnitDist);
		disp(errorMsg);
	else
		[L,k]=WAVELEN(d,T,50,g);

		[steep,maxstp]=ERRSTP(Hi,d,L);
%         assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
		if steep >= maxstp
			errorMsg = sprintf('Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)', maxstp, steep)
			disp(errorMsg)
		else
			[MR,S,MRintc,MRintt,Sintc,Sintt]=WFVW1(d,Hi,chi,L,H20weight);
			
			fprintf('\n\t\t\t\t\t\t %s \t\t\t %s \n','Miche-Rundgren','Sainflou')
			fprintf('%s \t %s \t\t %s \t\t %s \t\t %s \t\t %s \n','Wave Position at Wall','Crest','Trough','Crest','Trough', 'Units')
			fprintf('%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \t\t %s \n','Hgt above bottom',MR(1),MR(4),S(1),S(4), labelUnitDist)
			fprintf('%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \t\t %s/%s \n','Integrated force',MR(2),MR(5),S(2),S(5), labelUnitWt, labelUnitDist)
			fprintf('%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \t\t %s-%s/%s \n','Integrated moment',MR(3),MR(6),S(3),S(6), labelUnitWt, labelUnitDist, labelUnitDist)

			if single_case
				figure(1)
				subplot(2,1,1); plot(MRintc(:,2),MRintc(:,1),'g-',MRintc(:,3),MRintc(:,1),'c-.',MRintc(:,4),MRintc(:,1),'r:')
				hold on
				hline = refline([0 0]);
				set(hline,'LineStyle','--')
				hold off
				legend('Wave Pressure','Hydrostatic Pressure','Wave and Hydrostatic Pressue')
				xlabel(['Pressure [' labelUnitWt '/' labelUnitDist '^2]'])
				ylabel(['Elevation [' labelUnitDist ']'])
				title('Miche-Rundgren Pressure Distribution - Crest at Wall')
				
				subplot(2,1,2); plot(MRintt(:,2),MRintt(:,1),'g-',MRintt(:,3),MRintt(:,1),'c-.',MRintt(:,4),MRintt(:,1),'r:')
				hold on
				hline = refline([0 0]);
				set(hline,'LineStyle','--')
				rectangle('Position',[-50,floor(min(Sintt(:,1))),50,abs(floor(min(Sintt(:,1))))+5],'LineWidth',2)
				hold off
				ylim([floor(min(Sintt(:,1))) abs(floor(min(Sintt(:,1))))-5])
				legend('Wave Pressure','Hydrostatic Pressure','Wave and Hydrostatic Pressure')
				xlabel(['Pressure [' labelUnitWt '/' labelUnitDist '^2]'])
				ylabel(['Elevation [' labelUnitDist ']'])
				title('Miche-Rundgren Pressure Distribution - Trough at Wall')

				
				figure(2)
				subplot(2,1,1); plot(Sintc(:,2),Sintc(:,1),'g-',Sintc(:,3),Sintc(:,1),'c-.',Sintc(:,4),Sintc(:,1),'r:')
				hold on
				hline = refline([0 0]);
				set(hline,'LineStyle','--')
				hold off
				legend('Wave Pressure','Hydrostatic Pressure','Wave and Hydrostatic Pressure')
				xlabel(['Pressure [' labelUnitWt '/' labelUnitDist '^2]'])
				ylabel(['Elevation [' labelUnitDist ']'])
				title('Sainflou Pressure Distribution - Crest at Wall')
			
				subplot(2,1,2); plot(Sintt(:,2),Sintt(:,1),'g-',Sintt(:,3),Sintt(:,1),'c-.',Sintt(:,4),Sintt(:,1),'r:')
				hold on
				hline = refline([0 0]);
				set(hline,'LineStyle','--')
				rectangle('Position',[-50,floor(min(Sintt(:,1))),50,abs(floor(min(Sintt(:,1))))+5],'LineWidth',2)
				hold off
				ylim([floor(min(Sintt(:,1))) abs(floor(min(Sintt(:,1))))-5])
				legend('Wave Pressure','Hydrostatic Pressure','Wave and Hydrostatic Pressue')
				xlabel(['Pressure [' labelUnitWt '/' labelUnitDist '^2]'])
				ylabel(['Elevation [' labelUnitDist ']'])
				title('Sainflou Pressure Distribution - Trough at Wall')
			end
		end
    end
    
    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end
        
        fprintf(fId, 'Input\n');
        fprintf(fId, 'd\t%6.2f %s\n', d, labelUnitDist);
        fprintf(fId, 'Hi\t%6.2f %s\n', Hi, labelUnitDist);
        fprintf(fId, 'T\t%6.2f s\n', T, labelUnitDist);
        fprintf(fId, 'chi\t%6.2f\n', chi);
        fprintf(fId, 'cotphi\t%6.2f\n', cotphi);
        
        if length(errorMsg) > 0
            fprintf(fId, '\n%s\n', errorMsg);
        else
            fprintf(fId, '\n\t\t\t\t\t\t %s \t\t\t %s \n','Miche-Rundgren','Sainflou')
            fprintf(fId, '%s \t %s \t\t %s \t\t %s \t\t %s \t\t %s \n','Wave Position at Wall','Crest','Trough','Crest','Trough', 'Units')
            fprintf(fId, '%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \t\t %s \n','Hgt above bottom',...
                MR(1),MR(4),S(1),S(4), labelUnitDist)
            fprintf(fId, '%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \t\t %s/%s \n','Integrated force',...
                MR(2),MR(5),S(2),S(5), labelUnitWt, labelUnitDist)
            fprintf(fId, '%s \t\t %-6.2f \t %6.2f \t\t %-6.2f \t %6.2f \t\t %s-%s/%s \n','Integrated moment',...
                MR(3),MR(6),S(3),S(6), labelUnitWt, labelUnitDist, labelUnitDist)
        end
        
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
        
        exportData = {d, Hi, T, chi, cotphi};
        if length(errorMsg) > 0
            exportData = [exportData {errorMsg}];
        else
            exportData = [exportData {MR(1),MR(4),S(1),S(4),MR(2),MR(5),...
                S(2),S(5),MR(3),MR(6),S(3),S(6)}];
        end
        exporter.writeData(exportData);
    end
end

if fileOutputData{1}
    fclose(fId);
    exporter.close();
end

if single_case
	if fileOutputData{1}
      	fId = fopen('output/wave_forces_plot.txt', 'wt');
        
        fprintf(fId, 'Partial Listing of Plot Output File \n\n');
        
        fprintf(fId, 'Miche-Rundgren Pressure Distribution\n');
        fprintf(fId, 'Crest at Wall \n\n');
        
        fprintf(fId, '          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n');
        fprintf(fId, '          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n',...
            labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist);
        
        for loopIndex = 1:size(MRintc, 1)
            fprintf(fId, '%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n',...
                loopIndex, MRintc(loopIndex,1), MRintc(loopIndex,2), MRintc(loopIndex,3), MRintc(loopIndex,4));
        end
        
        fprintf(fId, '\n\nMiche-Rundgren Pressure Distribution\n');
        fprintf(fId, 'Trough at Wall \n\n');
        
        fprintf(fId, '          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n');
        fprintf(fId, '          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n',...
            labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist);
        
        for loopIndex = 1:size(MRintt, 1)
            fprintf(fId, '%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n',...
                loopIndex, MRintt(loopIndex,1), MRintt(loopIndex,2), MRintt(loopIndex,3), MRintt(loopIndex,4));
        end
        
        fprintf(fId, '\n\nSainflou Pressure Distribution\n');
        fprintf(fId, 'Crest at Wall \n\n');
        
        fprintf(fId, '          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n');
        fprintf(fId, '          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n',...
            labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist);
        
        for loopIndex = 1:size(Sintc, 1)
            fprintf(fId, '%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n',...
                loopIndex, Sintc(loopIndex,1), Sintc(loopIndex,2), Sintc(loopIndex,3), Sintc(loopIndex,4));
        end
        
        fprintf(fId, '\n\nSainflou Pressure Distribution\n');
        fprintf(fId, 'Trough at Wall \n\n');
        
        fprintf(fId, '          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n');
        fprintf(fId, '          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n',...
            labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist, labelUnitWt, labelUnitDist);
        
        for loopIndex = 1:size(Sintt, 1)
            fprintf(fId, '%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n',...
                loopIndex, Sintt(loopIndex,1), Sintt(loopIndex,2), Sintt(loopIndex,3), Sintt(loopIndex,4));
        end
        
        fclose(fId);
    end
end