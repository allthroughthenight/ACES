clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Wave Transmission on Permeable Structures (page 5-4 in ACES
% User's Guide). Determines wave transmission coefficients and transmitted
% wave heights for permeable breakwaters with crest elevations at or
% above the still-water level.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 19, 2011
% Date Verified: June 7, 2012 

%Requires English units

% Requires the following functions:
% ERRSTP
% ERRWAVBRK1
% EQBWLE
% EQBWTRCO
% MADSEELG
% MADSN1
% MADSN2
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   H: incident wave height
%   T: wave period
%   ds: water depth at structure toe
%   nummat: number of materials comprising the breakwater
%   d50: mean diameter of each material
%   p: porosity of each material
%   hs: structure height above toe
%   cotnssl: cotan of nearshore slope
%   b: structure crest width
%   cottheta: cotangent of structure slope
%   numlay: number of horizontal layers in the breakwater
%   th: thickness of each horizontal layer
%   hlen: horizontal length of each matertial in each layer

%   OUTPUT
%   Kr: wave reflection coefficient
%   KTt: wave transmission coefficient - through
%   KTo: wave transmission coefficient - overtopping
%   KT: wave transmission coefficient - total
%   Ht: transmitted wave height

%   OTHERS
%   freeb: freeboard
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

if single_case
    [H] = USER_INPUT_DATA_VALUE(['Enter H: incident wave height (' labelUnitDist '): '], 0.1, 100.0);
    
    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (s): ', 1.0, 1000.0);
    
    numCases = 1;
else
    multiCaseData = {...
            ['H: wave height (' labelUnitDist ')'], 0.1, 200.0;...
            'T: wave period (sec)', 1.0, 1000.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HList = varData(1, :);
    TList = varData(2, :);
end

[ds] = USER_INPUT_DATA_VALUE(['Enter ds: water depth at structure toe (' labelUnitDist '): '], 0.1, 200.0);

[NM] = USER_INPUT_DATA_VALUE('Enter NM: number of materials comprising the breakwater: ', 1, 4);

d50 = [];
por = [];
for matIndex = 1:NM
    [d50Input] = USER_INPUT_DATA_VALUE(['Enter d50: mean diameter of material #' num2str(matIndex) ' (' labelUnitDist '): '], 0.05, 99.0);
    d50 = [d50 d50Input];
end
for matIndex = 1:NM
    [porInput] = USER_INPUT_DATA_VALUE(['Enter p: porosity of material #' num2str(matIndex) ' (%): '], 0.0, 100.0);
    por = [por porInput];
end
por = por/100;
fprintf('%s \n\n','Breakwater geometry input: ');
[hs] = USER_INPUT_DATA_VALUE(['Enter hs: structure height above toe (' labelUnitDist '): '], 0.1, 200.0);

[cottheta] = USER_INPUT_DATA_VALUE('Enter cottheta: cotangent of structure slope: ', 1.0, 5.0);

[b] = USER_INPUT_DATA_VALUE(['Enter b: structure crest width (' labelUnitDist '): '], 0.1, 200.0);

[NL] = USER_INPUT_DATA_VALUE('Enter NL: number of horizontal layers in the breakwater: ', 1, 4);

th = [];
for layIndex = 1:NL
    [thInput] = USER_INPUT_DATA_VALUE(['Enter th: thickness of horizontal layer #' num2str(layIndex) ' (' labelUnitDist '): '], 0.1, 200.0);

    th = [th thInput];
end

hlen = [];
for matIndex = 1:NM
    hlenTemp = [];

    for layIndex = 1:NL
        [hlenInput] = USER_INPUT_DATA_VALUE(['Enter hlen: horizontal length of matertial # ' num2str(matIndex) ' in layer #' num2str(layIndex) ' (' labelUnitDist '): '], 0.0, 200.0);

        hlenTemp = [hlenTemp hlenInput];
    end

    if matIndex == 1
        hlen = hlenTemp;
    else
        hlen = [hlen; hlenTemp];
    end
end


if ~metric
    if strcmp(water,'S') || strcmp(water,'s')
        nu=14.643223710^(-06); %salt water
    else
        nu=0.0000141; %ft^2/s KINEMATIC VISCOSITY OF THE WATER AT 50 DEGREES FAHRENHEIT
 
    end
else 
    if strcmp(water,'S') || strcmp(water,'s')
       nu = 1.3604*10^(-06); % salt water
    else
       nu = 1.307*10^(-6); % m^2/s %fresh
    end
end

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/wavetrans_perm.txt', 'wt');
    exporter = EXPORTER('output/exporterWavetransPerm');
end

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
    end
    
    errorMsg = '';

    [Hb]=ERRWAVBRK1(ds,0.78);
%     assert(H<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)
    if not(H<Hb)
        errorMsg = sprintf('Error: Input wave broken (Hb = %6.2f m)',Hb);
        disp(errorMsg);
    else
        [Hbs]=ERRWAVBRK2(T,1/cottheta,ds); 
%         assert(H<Hbs,'Error: Input wave breaking at toe of the structure (Hbs = %6.2f m)',Hbs)
        if not(H<Hbs)
            errorMsg = sprintf('Error: Input wave breaking at toe of the structure (Hbs = %6.2f m)',Hbs);
            disp(errorMsg);
        else
            [L,k]=WAVELEN(ds,T,50,g);

            [steep,maxstp]=ERRSTP(H,ds,L);
%             assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
            if not(steep<maxstp)
                errorMsg = sprintf('Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep');
                disp(errorMsg);
            else
    %             assert(ds<hs,'Error: Method does not apply to submerged structures.')
                if not(ds<hs)
                    errorMsg = 'Error: Method does not apply to submerged structures.';
                    disp(errorMsg);
                else
    %             assert(sum(th)==ds,'Error: Water depth must equal sum of all layer thicknesses.')
                    if not(sum(th)==ds)
                        errorMsg = 'Error: Water depth must equal sum of all layer thicknesses.';
                        disp(errorMsg);
                    else
                        [KTt,Kto,KT,Kr,Ht,L]=MADSEELG(H,T,ds,hs,b,NL,th,hlen,NM,d50,por,cottheta,nu,g);

                        fprintf('%s \t\t\t %-6.3f \n','Reflection coefficient, Kr', Kr)
                        fprintf('%s \n','Wave transmission coefficient')
                        fprintf('%s \t %-6.3f \n','Wave Transmission (Through), KTt', KTt)
                        fprintf('%s  %-6.3f \n','Wave Transmission (Overtopping), KTo', Kto)
                        fprintf('%s \t\t %-6.3f \n','Wave Transmission (Total), KT', KT)
                        fprintf('%s \t\t %-6.2f \n','Transmitted wave height, Ht', Ht)
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
        fprintf(fId, 'H\t\t%6.2f %s\n', H, labelUnitDist);
        fprintf(fId, 'T\t\t%6.2f s\n', T);
        fprintf(fId, 'ds\t\t%6.2f %s\n', ds, labelUnitDist);
        for d50Index = 1:length(d50)
            fprintf(fId, 'd50 #%d\t\t%6.2f %s\n', d50Index, d50(d50Index), labelUnitDist);
        end
        for porIndex = 1:length(por)
            fprintf(fId, 'por #%i\t\t%6.2f%%\n', porIndex, por(porIndex)*100);
        end
        fprintf(fId, 'hs\t\t%6.2f %s\n', hs, labelUnitDist);
        fprintf(fId, 'cottheta\t%6.2f\n', cottheta);
        fprintf(fId, 'b\t\t%6.2f %s\n', b, labelUnitDist);
        for thIndex = 1:length(th)
            fprintf(fId, 'th #%d\t\t%6.2f %s\n', thIndex, th(thIndex), labelUnitDist);
        end
        for hlenIndex1 = 1:size(hlen, 1)
            for hlenIndex2 = 1:size(hlen, 2)
                fprintf(fId, 'Len mat %d,\t%6.2f %s\n  layer %d\n',...
                    hlenIndex1, hlen(hlenIndex1, hlenIndex2),...
                    labelUnitDist, hlenIndex2);
            end
        end
        
        if length(errorMsg)
            fprintf(fId, '\n%s\n', errorMsg);
        else
            fprintf(fId, '\nReflection coefficient, Kr\t\t%-6.3f\n', Kr);
            fprintf(fId, 'Wave transmission coefficient\n');
            fprintf(fId, 'Wave Transmission (Through), KTt\t%-6.3f\n', KTt);
            fprintf(fId, 'Wave Transmission (Overtopping), KTo\t%-6.3f\n', Kto);
            fprintf(fId, 'Wave Transmission (Total), KT\t\t%-6.3f\n', KT);
            fprintf(fId, 'Transmitted wave height, Ht\t\t%-6.2f %s\n', Ht, labelUnitDist);
        end
        
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
        
        exportData = {H, T, ds};
        for exportDataVal = d50
            exportData = [exportData {exportDataVal}];
        end
        for exportDataVal = por
            exportData = [exportData {exportDataVal*100}];
        end
        exportData = [exportData {hs, cottheta, b}];
        for exportDataVal = th
            exportData = [exportData {exportDataVal}];
        end
        for hlenIndex1 = 1:size(hlen, 1)
            for hlenIndex2 = 1:size(hlen, 2)
                exportData = [exportData {hlen(hlenIndex1, hlenIndex2)}];
            end
        end
        if length(errorMsg) > 0
            exportData = [exportData {errorMsg}];
        else
            exportData = [exportData {Kr, KTt, Kto, KT, Ht}];
        end
        exporter.writeData(exportData);
    end
end

if fileOutputData{1}
    fclose(fId);
    exporter.close();
end