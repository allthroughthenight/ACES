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
    
    [ds] = USER_INPUT_DATA_VALUE(['Enter ds: water depth at structure toe (' labelUnitDist '): '], 0.1, 200.0);
    
    [NM] = USER_INPUT_DATA_VALUE('Enter NM: number of materials comprising the breakwater: ', 1, 4);
    
    d50 = [];
    por = [];
    for matIndex = 1:NM
        [d50Input] = USER_INPUT_DATA_VALUE(['Enter d50: mean diameter of material #' num2str(matIndex) ' (' labelUnitDist '): '], 0.05, 99.0);

        [porInput] = USER_INPUT_DATA_VALUE(['Enter p: porosity of material #' num2str(matIndex) ' (%): '], 0.0, 100.0);
        
        d50 = [d50 d50Input];
        por = [por porInput];
    end
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
    numCases =1;
else
    multiCaseData = {...
            ['H: wave height (' labelUnitDist ')'], 0.1, 200.0;...
            'T: wave period (sec)', 1.0, 1000.0;...
            ['ds: water depth (' labelUnitDist ')'], 0.1, 5000.0;...
            'NM: number of materials comprising the breakwater', 1, 4};
    d50 = [];
    por = [];
    for matIndex = 1:NM
            multiCaseData = [ multiCaseData; {['d50: mean diameter of material #' num2str(matIndex) ' (' labelUnitDist '): '], 0.05, 99.0;...
                ['p: porosity of material #' num2str(matIndex) ' (%): '], 0.0, 100.0}];
      
            d50 = [d50 d50Input];
            por = [por porInput];
    end
    multiCaseData = [ multiCaseData; {['hs: structure height above toe (' labelUnitDist '): '], 0.1, 200.0;...
                     'cottheta: cotangent of structure slope: ', 1.0, 5.0;...
                     ['b: structure crest width (' labelUnitDist '): '], 0.1, 200.0;...
                     'NL: number of horizontal layers in the breakwater: ', 1, 4}];
                 
    th = [];
    hlen = [];
    for matIndex = 1:NL
        multiCaseData = [ multiCaseData; {['th: thickness of horizontal layer #' num2str(layIndex) ' (' labelUnitDist '): '], 0.1, 200.0}];
        for layerindex=1:NL
            multiCaseData = [ multiCaseData; {['hlen: horizontal length of matertial # ' num2str(matIndex) ' in layer #' num2str(layIndex) ' (' labelUnitDist '): '], 0.0, 200.0}];   
        end
    end
               
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HList = varData(1, :);
    TList = varData(2, :);
    dsList = varData(3, :);
    NMList = varData(4, :);
    d50List = varData(5, :);
    porList = varData(6, :);
    hsList = varData(7, :);
    cotthetaList = varData(8, :);
    BList = varData(9, :);
    NLList = varData(10, :);
    thList = varData(11, :);
    hlenList = varData(12, :);
end

if ~metric
    if strcmp(water,'S')
        nu=14.643223710^(-06); %salt water
    else
        nu=0.0000141; %ft^2/s KINEMATIC VISCOSITY OF THE WATER AT 50 DEGREES FAHRENHEIT
 
    end
else 
    if strcmp(water,'S')
       nu = 1.3604*10^(-06); % salt water
    else
       nu = 1.307*10^(-6); % m^2/s %fresh
    end
end

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        ds = dsList(loopIndex);
        NM = NMList(loopIndex);
        d50 = d50List(loopIndex);
        por = porList(loopIndex);
        hs = hsList(loopIndex);
        cottheta = cotthetaList(loopIndex);
        B = BList(loopIndex);
        NL = NLList(loopIndex);
        th = thList(loopIndex);
        hlen = hlenList(loopIndex);
    end
    

    [Hb]=ERRWAVBRK1(ds,0.78);
    assert(H<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)
    
    [Hbs]=ERRWAVBRK2(T,1/cottheta,ds); 
    assert(H<Hbs,'Error: Input wave braking at toe of the structure (Hbs = %6.2f m)',Hbs)
    
    [L,k]=WAVELEN(ds,T,50,g);

    [steep,maxstp]=ERRSTP(H,ds,L);
    assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

    assert(ds<hs,'Error: Method does not apply to submerged structures.')

    assert(sum(th)==ds,'Error: Water depth must equal sum of all layer thicknesses.')

    [KTt,Kto,KT,Kr,Ht,L]=MADSEELG(H,T,ds,hs,b,NL,th,hlen,NM,d50,por,cottheta,nu,g);

    fprintf('%s \t\t\t %-6.3f \n','Reflection coefficient, Kr', Kr)
    fprintf('%s \n','Wave transmission coefficient')
    fprintf('%s \t %-6.3f \n','Wave Transmission (Through), KTt', KTt)
    fprintf('%s  %-6.3f \n','Wave Transmission (Overtopping), KTo', Kto)
    fprintf('%s \t\t %-6.3f \n','Wave Transmission (Total), KT', KT)
    fprintf('%s \t\t %-6.2f \n','Transmitted wave height, Ht', Ht)


end