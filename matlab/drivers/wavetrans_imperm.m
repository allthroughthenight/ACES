clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Wave Transmission on Impermeable Structures (page 5-3 in ACES
% User's Guide). Provides estimates of wave runup and transmission on rough
% and smooth slope structures. It also addresses wave transmission over
% impermeable vertical walls and composite structures.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 19, 2011
% Date Verified: June 6, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK2
% HTP
% LWTGEN
% RUNUPR
% RUNUPS
% VERTKT
% WAVELEN

% MAIN VARIABLE LIST:
%   MANDATORY INPUT
%   H: incident wave height (Hs for irregular waves)
%   T: wave period (Tp for irregular waves)
%   cotphi: cotan of nearshore slope
%   ds: water depth at structure toe
%   hs: structure height above toe 
%   wth: structure crest width
%   cottheta: cotan of structure slope (0.0 for vertical wall)

%   OPTIONAL INPUT
%   a: empirical coefficient for rough slope runup
%   b: empirical coefficeint for rough slope runup
%   R: wave runup (if known)
%   hB: toe protection or composite breakwater berm height above structure
%   toe

%   MANDATORY OUTPUT
%   Ht: transmitted wave height

%   OPTIONAL OUTPUT
%   R: wave runup

%   OTHERS
%   freeb: freeboard
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

fprintf('%s \n\n','Calculation and slope type options: ');
fprintf('%s \n','[1] Wave transmission only for smooth slope')
fprintf('%s \n','[2] Wave transmission only for vertical wall')
fprintf('%s \n','[3] Wave runup and transmission for rough slope')
fprintf('%s \n\n','[4] Wave runup and transmission for smooth slope')

option=input('Select option: ');
fprintf('\n')

if single_case
    [H] = USER_INPUT_DATA_VALUE(['Enter H: incident wave height (Hs for irregular waves) (' labelUnitDist '): '], 0.1, 100.0);
    
    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (Tp for irregular waves) (s): ', 1.0, 1000.0);
    
    [cotphi] = USER_INPUT_DATA_VALUE('Enter cotphi: cotan of nearshore slope: ', 5.0, 10000.0);
    
    [ds] = USER_INPUT_DATA_VALUE(['Enter ds: water depth at structure toe (' labelUnitDist '): '], 0.1, 200.0);
    
    if option~=2
        [cottheta] = USER_INPUT_DATA_VALUE('Enter cottheta: cotan of structure slope (0.0 for vertical wall): ', 0.0, 30.0);
    else
        cottheta = 0;
    end
    
    [hs] = USER_INPUT_DATA_VALUE(['Enter hs: structure height above toe (' labelUnitDist '): '], 0.0, 200.0);
    
    [B] = USER_INPUT_DATA_VALUE(['Enter B: structure crest width (' labelUnitDist '): '], 0.0, 200.0);
 
    if option==1
        [R] = USER_INPUT_DATA_VALUE(['Enter R: wave runup (if known) (' labelUnitDist '): '], 0.0, 100.0);
    end

    if option==2
       [hB] = USER_INPUT_DATA_VALUE(['Enter hB: structure berm height above toe (' labelUnitDist '): '], 0.0, 200.0);
    end
    
    numCases=1;
else
     multiCaseData = {...
         ['H: wave height (' labelUnitDist ')'], 0.1, 100.0;...
          'T: wave period (sec)', 1.0, 1000.0;...
          'cotphi: cotan of nearshore slope', 5.0, 10000.0;...
         ['ds: water depth at structure toe (' labelUnitDist ')'], 0.1, 200.0};
     
     if option~=2
        multiCaseData = [ multiCaseData; {'cottheta: cotan of structure slope (0.0 for vertical walls)', 0.0, 30.0}];
     end

     multiCaseData = [ multiCaseData;...
        {['hs: structure height above toe (' labelUnitDist ')'], 0.0, 200;...
        ['B: structure crest width (' labelUnitDist ')'], 0.0, 200.0}];

     if option==1
        multiCaseData = [ multiCaseData; {['R: wave runup (if known) (' labelUnitDist ')'], 0.0, 100.0}];
     end

     if option==2
        multiCaseData = [ multiCaseData; {['hB: structure berm height above toe (' labelUnitDist ')'], 0.0, 200.0}];
     end       

    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HList = varData(1, :);
    TList = varData(2, :);
    cotphiList = varData(3, :);
    dsList = varData(4, :);
    
    optVarNum = 5;
    
    if option ~= 2
        cotthetaList = varData(optVarNum, :);
        
        optVarNum = optVarNum + 1;
    end
    
    hsList = varData(optVarNum, :);
    BList = varData(optVarNum + 1, :);
    
    optVarNum = optVarNum + 2;
    
    if option == 1
        RList = varData(optVarNum, :);
        
        optVarNum = optVarNum + 1;
    end
    
    if option == 2
        hBList = varData(optVarNum, :);
    end
end

if option==3
    runupCoeffData = {...
        'Riprap', 0.956, 0.398;...
        'Quarrystone (Impermeable Base)', 0.692, 0.504;...
        'Quarrystone (Permeable Base)', 0.775, 0.361;...
        'Modified Cubes', 0.95, 0.69;...
        'Tetrapods', 1.01, 0.91;...
        'Quadrapods', 0.59, 0.35;...
        'Hexapods', 0.82, 0.63;...
        'Tribars', 1.81, 1.57;...
        'Dolosse', 0.988, 0.703};
    sizeCoeffData = size(runupCoeffData, 1);

    fprintf('Suggested Empirical Rough Slope Runup Coeff Listing\n');
    for loopIndex = 1:sizeCoeffData
        fprintf('[%d] %s \t %-6.3f \t %-6.3f\n', loopIndex,...
            runupCoeffData{loopIndex, 1},...
            runupCoeffData{loopIndex, 2},...
            runupCoeffData{loopIndex, 3});
    end
    fprintf('[%d] Enter custom values\n', (sizeCoeffData + 1));

    [coeffChoice] = USER_INPUT_DATA_VALUE(...
        'Select option: ', 1, (sizeCoeffData + 1));
    coeffChoice = floor(coeffChoice);

    if coeffChoice == sizeCoeffData + 1
        a = USER_INPUT_DATA_VALUE('Enter coefficient a: ', 0.0, 20.0);
        b = USER_INPUT_DATA_VALUE('Enter coefficient b: ', 0.0, 20.0);
    else
        a = runupCoeffData{coeffChoice, 2};
        b = runupCoeffData{coeffChoice, 3};
    end
end

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        cotphi = cotphiList(loopIndex);
        ds = dsList(loopIndex);
        
        if option ~= 2
            cottheta = cotthetaList(loopIndex);
        else
            cottheta = 0;
        end

        hs = hsList(loopIndex);
        B = BList(loopIndex);

        if option == 1
            R = RList(loopIndex);
        end

        if option == 2
            hB = hBList(loopIndex);
        end
    end
    
    m=1/cotphi;

    if option~=2
        assert(ds<hs,'Error: Method does not apply to submerged structures.')
    end

    [c,c0,cg,cg0,k,L,L0,reldep]=LWTGEN(ds,T,g);

    [Hbs]=ERRWAVBRK2(T,m,ds);
    assert(H<Hbs,'Error: Wave broken at structure (Hbs = %6.2f m)',Hbs)

    [steep,maxstp]=ERRSTP(H,ds,L);
    assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

    if cottheta==0
        assert(option==2,'Error: A cotangent of zero indicates a vertical wall.')

        reldep=ds/L;

        assert(reldep>0.14 && reldep<0.5, 'Error: d/L conditions exceeded - 0.14<=(d/L)<=0.5')
    else
        theta=atan(1/cottheta);
        ssp=(1/cottheta)/sqrt(H/L0);
    end

    if option==3
%         a=0.956;
%         b=0.398;
        [R]=RUNUPR(H,ssp,a,b);
        fprintf('%s \t\t\t\t\t\t %-6.3f \n','Runup',R)
    elseif option==4
        [R]=RUNUPS(H,L,ds,theta,ssp);
        fprintf('%s \t\t\t\t\t\t %-6.3f \n','Runup',R)
    end

    freeb=hs-ds;

    if option~=2
        [Ht]=HTP(B,hs,R,H,freeb);
        fprintf('%s \t %-6.3f \n','Transmitted wave height',Ht)
    else
        dl=ds-hB;
        [Ht]=VERTKT(H,freeb,B,ds,dl);
        fprintf('%s \t %-6.3f \n','Transmitted wave height',Ht)
    end
end

if single_case
    % File Output
    fileOutputArgs = {};
    [fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

    if fileOutputData{1}
        fId = fopen('output/wavetrans_imperm.txt', 'wt');
        
        if option==3
            fprintf(fId, '%s \t\t\t\t\t\t %-6.3f \n','Runup',R);
        elseif option==4
            fprintf(fId, '%s \t\t\t\t\t\t %-6.3f \n','Runup',R);
        end

        if option~=2
            fprintf(fId, '%s \t %-6.3f \n','Transmitted wave height',Ht);
        else
            fprintf(fId, '%s \t %-6.3f \n','Transmitted wave height',Ht);
        end
        
        fclose(fId);
    end
end