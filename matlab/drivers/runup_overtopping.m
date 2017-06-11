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
numConsts = 0;
if has_rough_slope
    numConsts = numConsts + 2;
end
if has_overtopping
    numConsts = numConsts + 3;
end
if ~has_runup
    numConsts = numConsts + 1;
end

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

if numConsts > 0
    fprintf('\nConstant Values:\n');
    
    if has_rough_slope
        %Empirical coefficients for rough slope runup
        a=0.956;
        b=0.398;
        
        fprintf('a = %-6.4f\n', a);
        fprintf('b = %-6.4f\n', b);
    end
    
    if has_overtopping
        %Empirical coefficients and values for overtopping
        alpha=0.076463;
        Qstar0=0.025;
        U=35.0*conversionKnots2mph;
        
        fprintf('alpha = %-6.4f\n', alpha);
        fprintf('Qstar0 = %-6.4f\n', Qstar0);
        fprintf('U = %-6.4f knots\n', U/conversionKnots2mph);
        
        if option==3
            R=15.0;
            fprintf('R = %-6.4f\n', R);
        elseif option==4
            R=20.0;
            fprintf('R = %-6.4f\n', R);
        end
    end
    
    custom_const = USER_INPUT_FINITE_CHOICE(...
        'Use default constant values or load from file? (D or F): ',...
        {'D', 'd', 'F', 'f'});
    custom_const = strcmp(custom_const, 'F') || strcmp(custom_const, 'f');

    if custom_const
        accepted = false;
        while ~accepted

            [fileData] = USER_INPUT_MULTI_FILE();

            optVarNum = 1;
            if size(fileData, 1) == numConsts
                if size(fileData, 2) == 1
                    accepted = true;

                    if has_rough_slope
                        a = fileData(optVarNum);
                        b = fileData(optVarNum + 1);

                        optVarNum = optVarNum + 2;
                    end

                    if has_overtopping
                        alpha = fileData(optVarNum);
                        Qstar0 = fileData(optVarNum + 1);
                        U = fileData(optVarNum + 2)*conversionKnots2mph;
                        R = fileData(optVarNum + 3);
                    end
                elseif size(fileData, 2) == numCases
                    accepted = true;

                    if has_rough_slope
                        aList = fileData(optVarNum, :);
                        bList = fileData(optVarNum + 1, :);

                        optVarNum = optVarNum + 2;
                    end

                    if has_overtopping
                        alphaList = fileData(optVarNum, :);
                        Qstar0List = fileData(optVarNum + 1);
                        UList = fileData(optVarNum + 2, :)*conversionKnots2mph;
                        RList = fileData(optVarNum + 3, :);
                    end
                else
                    fprintf('Wrong number of cases. Expected either 1 or %d, found %d.\n',...
                        numCases, size(fileData, 2));
                end
            else
                fprintf('Wrong number of constants. Expected %d, found %d.\n',...
                    numConsts, size(fileData, 1));
            end
        end
    else

    end
end

for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        cotphi = cotphiList(loopIndex);
        ds = dsList(loopIndex);
        cottheta = cotthetaList(loopIndex);
        hs = hsList(loopIndex);
        
        if exist('aList')
            a = aList(loopIndex);
        end
        
        if exist('bList')
            b = bList(loopIndex);
        end
        
        if exist('alphaList')
            alpha = alphaList(loopIndex);
        end
        
        if exist('Qstar0List')
            Qstar0 = Qstar0List(loopIndex);
        end
        
        if exist('UList')
            U = UList(loopIndex);
        end
        
        if exist('RList')
            R = RList(loopIndex);
        end
    end
    
    m=1/cotphi;

    assert(ds<hs,'Error: Method does not apply to submerged structures.')

    [Hbs]=ERRWAVBRK2(T,m,ds);
    assert(H<Hbs,'Error: Wave broken at structure (Hbs = %6.2f %s)',Hbs,labelUnitDist)

    [c,c0,cg,cg0,k,L,L0,reldep]=LWTGEN(ds,T,g);

    [steep,maxstp]=ERRSTP(H,ds,L);
    assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

    [alpha0,H0]=LWTDWS(0,c,cg,c0,H);

    relht0=ds/H0;
    steep0=H0/(g*T^2);

    if cottheta==0
        assert(option~=1 && option~=5 && option~=7,'Error: Vertical wall cannot have rough slope.')
        theta=0.5*pi;
        ssp=1000;
    else
        theta=atan(1/cottheta);
        ssp=(1/cottheta)/sqrt(H/L0);
    end

    fprintf('%s \n','Deepwater')
    fprintf('\t %s \t\t\t\t %-6.3f %s \n','Wave height, Hs0',H0,labelUnitDist)
    fprintf('\t %s \t\t %-6.3f \n','Relative height, ds/H0',relht0)
    fprintf('\t %s \t %-6.6f \n\n','Wave steepness, Hs0/(gT^2)',steep0)

    freeb=hs-ds;

    if option==1
        [R]=RUNUPR(H,ssp,a,b);
        fprintf('%s \t %-6.3f %s \n\n','Runup',R,labelUnitDist)
    elseif option==2
        [R]=RUNUPS(H,L,ds,theta,ssp);
        fprintf('%s \t %-6.3f %s \n\n','Runup',R,labelUnitDist)
    elseif option==3   
        [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
        fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
    elseif option==4
        [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
        fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
    elseif option==5
        [R]=RUNUPR(H,ssp,a,b);
        [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
        fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
        fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
    elseif option==6
        [R]=RUNUPS(H,L,ds,theta,ssp);
        [Q]=QOVERT(H0,freeb,R,Qstar0,alpha,theta,U,g);
        fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
        fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
    elseif option==7
        [R]=RUNUPR(H,ssp,a,b);
        [Q]=QOVERT_IRR(H0,freeb,R,Qstar0,alpha,theta,U,g);
        fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
        fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
    elseif option==8
        [R]=RUNUPS(H,L,ds,theta,ssp);
        [Q]=QOVERT_IRR(H0,freeb,R,Qstar0,alpha,theta,U,g);
        fprintf('%s \t %-6.3f %s \n','Runup',R,labelUnitDist)
        fprintf('%s \t %-6.3f %s^3/sec-%s \n\n','Overtopping rate per unit width',Q,labelUnitDist,labelUnitDist)
    end
end