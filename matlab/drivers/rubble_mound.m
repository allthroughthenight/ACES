clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Rubble-Mound Revetment Design (page 4-4 in ACES % User's Guide). 
% Provides estimates for revetment armor and bedding layer stone sizes,
% thicknesses, and gradation characteristics. Also calculated are two 
% values of runup on the revetment, an expected extreme and a conservative
% run-up value.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 15, 2011
% Date Verified: June 7, 2012 

% Requires the following functions:
% ERRSTP
% ERRWAVBRK2
% RUNUPR
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   Hs: significant wave height (m)
%   Ts: signficiant wave period (sec)
%   cotnsl: cotangent of nearshore slope
%   ds: water depth at toe of revetment (m)
%   cotssl: cotangent of structure slope
%   unitwt: unit weight of rock (N/m^3)
%   P: permeability coefficient
%   S: damage level

%   OUTPUT
%   w: weight of individual armor and filter stone (N)
%   at: armor/filter layer thickness (m)
%   R: runup (m)
%   ssp: surf-similarity parameter
%   ssz: surf parameter

%   OTHERS
%   ssp: surf-similarity parameter at the transition from plunging to
%   surging waves
%   ssz: surf parameter for given input date
%   rho: density of water (kg/m^3)
%   H20weight: specific weight of water
%   ztp: surf simularity parametet at transition from plunging to surging
%   waves
%   N: number of waves the structure is exposed to (conservative values)
%   CERC_NS: stability number
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

if single_case
    [Hs] = USER_INPUT_DATA_VALUE(['Enter Hs: significant wave height (' labelUnitDist '): '], 0.1, 100.0);
    
    [Ts] = USER_INPUT_DATA_VALUE('Enter Ts: signficiant wave period (sec): ', 1.0, 1000.0);
    
    [cotnsl] = USER_INPUT_DATA_VALUE('Enter cotnsl: cotangent of nearshore slope: ', 5.0, 10000.0);
    
    [ds] = USER_INPUT_DATA_VALUE(['Enter ds: water depth at toe of revetment (' labelUnitDist '): '], 0.1, 200.0);
    
    [cotssl] = USER_INPUT_DATA_VALUE('Enter cotssl: cotangent of structure slope: ', 2.0, 6.0);
    
    [unitwt] = USER_INPUT_DATA_VALUE(['Enter unitwt: unit weight of rock (' labelUnitWt '/' labelUnitDist '^3): '], 1.0, 99999.0);
    
    [P] = USER_INPUT_DATA_VALUE('Enter P: permeability coefficient: ', 0.05, 0.6);
    
    [S] = USER_INPUT_DATA_VALUE('Enter S: damage level: ', 2.0, 17.0);
    
    numCases = 1;
else
    multiCaseData = {...
        ['Hs: significant wave height (' labelUnitDist ')'], 0.1, 100.0;...
        'Ts: signficiant wave period (sec)', 1.0, 1000.0;...
        'cotnsl: cotangent of nearshore slope', 5.0, 10000.0;...
        ['ds: water depth at toe of revetment (' labelUnitDist ')'], 0.1, 200.0;...
        'cotssl: cotangent of structure slope', 2.0, 6.0;...
        ['unitwt: unit weight of rock (' labelUnitWt '/' labelUnitDist '^3)'], 1.0, 99999.0;...
        'P: permeability coefficient', 0.05, 0.6;...
        'S: damage level', 2.0, 17.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HsList = varData(1, :);
    TsList = varData(2, :);
    cotnslList = varData(3, :);
    dsList = varData(4, :);
    cotsslList = varData(5, :);
    unitwtList = varData(6, :);
    PList = varData(7, :);
    SList = varData(8, :);
end

N=7000;

H20weight=g*rho;

exporter = EXPORTER('output/exporterRubbleMound.txt');

% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/rubble_mound.txt', 'wt');
end


for loopIndex = 1:numCases
    if ~single_case
        Hs = HsList(loopIndex);
        Ts = TsList(loopIndex);
        cotnsl = cotnslList(loopIndex);
        ds = dsList(loopIndex);
        cotssl = cotsslList(loopIndex);
        unitwt = unitwtList(loopIndex);
        P = PList(loopIndex);
        S = SList(loopIndex);
    end
    
    errorMsg = '';
    
    m=1/cotnsl;

    [Hbs]=ERRWAVBRK2(Ts,m,ds);
%     assert(Hs<Hbs,'Error: Wave broken at structure (Hbs = %6.2f m)',Hbs)
    if not(Hs<Hbs)
        errorMsg = sprintf('Error: Wave broken at structure (Hbs = %6.2f m)',Hbs);
        disp(errorMsg);
    else
        [L,k]=WAVELEN(ds,Ts,50,g);

        [steep,maxstp]=ERRSTP(Hs,ds,L);
%         assert(steep<maxstp,'Error: Wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
        if not(steep<maxstp)
            errorMsg = sprintf('Error: Wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep');
            disp(errorMsg);
        else
            tanssl=1/cotssl;
            Tz=Ts*(0.67/0.80);
            ssz=tanssl/sqrt(2*pi*Hs/(g*Tz^2)); 

            arg1=1/(P+0.5);
            ssp=(6.2*(P^0.31)*sqrt(tanssl))^arg1;

            CERC_NS=(1.45/1.27)*(cotssl^(1/6)); %if change to 1.14, same answer as ACES

            arg2=(S/sqrt(N))^0.2;
            plunge_NS=6.2*(P^0.18)*arg2*(ssz^-0.5);
            surging_NS=1.0*(P^-0.13)*arg2*sqrt(cotssl)*(ssz^P);

            if ssz<=ssp
                Dutch_NS=plunge_NS;
            else
                Dutch_NS=surging_NS;
            end

            Dutch_NS=1.20*Dutch_NS;

            %Stability number used to calculated the mean weight of armor units is the 
            %larger of the CERC vs Dutch stability numb
            NS=max(CERC_NS,Dutch_NS);

            w50=unitwt*(Hs/(NS*((unitwt/H20weight)-1.0)))^3;

            %Minimum thickness of armor layer
            rarmor=2*((w50/unitwt)^(1/3)); 

            %Determine bedding/filter layer thickness where%maximum of either rarmor/4 
            %or 1
            rfilter=max(rarmor/4,1.0); 

            %Calculate the total horizontal layer thickness (l) of the armor layer and
            %first underlayer
            rt=rarmor+rfilter; 
            l=rt*sqrt(1+(cotssl^2));

            %Compaer l to 2*Hs. If l<2*Hs then set L=2*Hs and solve for a new RT. Then
            %calculate a new rarmor and a new rbed.
            if l<(2*Hs)
                l=2*Hs;
                rt=l/sqrt(1+(cotssl^2));
                rarmor=rt-rfilter;
                rfilter=max(rarmor/4,1.0);
            end

            %Armor layer weight
            alw0=(1/8)*w50;
            alw15=0.4*w50;
            alw50=w50;
            alw85=1.96*w50;
            alw100=4*w50;

            %Armor layer dimension
            ald0=(alw0/unitwt)^(1/3);
            ald15=(alw15/unitwt)^(1/3);
            ald50=(alw50/unitwt)^(1/3);
            ald85=(alw85/unitwt)^(1/3);
            ald100=(alw100/unitwt)^(1/3);

            %Bedding/filter layer dimensions
            bld85=ald15/4.0;

            temp1=exp(0.01157*85.0-0.5785);
            bld50=bld85/temp1;

            temp1=exp(0.01157*0.0-0.5785);
            bld0=bld50*temp1;
            temp1=exp(0.01157*15.0-0.5785);
            bld15=bld50*temp1;
            temp1=exp(0.01157*100.0-0.5785);
            bld100=bld50*temp1;

            %Filter layer weight
            blw0=unitwt*(bld0^3);
            blw15=unitwt*(bld15^3);
            blw50=unitwt*(bld50^3);
            blw85=unitwt*(bld85^3);
            blw100=unitwt*(bld100^3);

            Tp=Ts/0.80;

            [Lp,k]=WAVELEN(ds,Tp,50,g);

            Hm01=0.10*Lp*tanh(2*pi*ds/Lp);
            Hm02=Hs/exp(0.00089*((ds/(g*(Tp^2)))^(-0.834)));

            Hm0=min(Hm01,Hm02);

            esp=tanssl/((2*pi*Hm0/(g*(Tp^2)))^(1/2));

            [runupr_max]=RUNUPR(Hm0,esp,1.022,0.247);
            [runupr_conserv]=RUNUPR(Hm0,esp,1.286,0.247);

            fprintf('%s %-6.2f %s\n','Armor layer thickness = ',rarmor, labelUnitDist )
            fprintf('%s \t %s (%s) \t %s (%s) \n','Percent less than by weight', 'Weight', labelUnitWt,'Dimension', labelUnitDist)
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',0.0,alw0,ald0);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',15.0,alw15,ald15);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',50.0,alw50,ald50);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',85.0,alw85,ald85);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n\n',100.0,alw100,ald100);
            fprintf('%s %-6.2f %s\n','Filter layer thickness = ',rfilter, labelUnitDist)
            fprintf('%s \t %s (%s) \t %s (%s) \n','Percent less than by weight', 'Weight', labelUnitWt,'Dimension', labelUnitDist)
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',0.0,blw0,bld0);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',15.0,blw15,bld15);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',50.0,blw50,bld50);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',85.0,blw85,bld85);
            fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n\n',100.0,blw100,bld100);

            fprintf('%s \n','Irregular runup')
            fprintf('%s %-6.2f %s \n','Conservative = ',runupr_conserv, labelUnitDist )
            fprintf('%s %-6.2f %s \n','Expected Maximum = ',runupr_max, labelUnitDist)
        end
    end
    
    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end
        
        fprintf(fId, 'Input\n');
        fprintf(fId, 'Hs\t%6.2f %s\n', Hs, labelUnitDist);
        fprintf(fId, 'Ts\t%6.2f s\n', Ts);
        fprintf(fId, 'cotnsl\t%6.2f\n', cotnsl);
        fprintf(fId, 'ds\t%6.2f %s\n', ds, labelUnitDist);
        fprintf(fId, 'cotssl\t%6.2f\n', cotssl);
        fprintf(fId, 'unitwt\t%6.2f %s/%s^3\n', unitwt, labelUnitWt, labelUnitDist);
        fprintf(fId, 'P\t%6.2f\n', P);
        fprintf(fId, 'S\t%6.2f\n\n', S);
        
        if length(errorMsg) > 0
            fprintf(fId, '%s\n', errorMsg);
        else
            fprintf(fId, '%s %6.2f %s\n','Armor layer thickness = ',rarmor, labelUnitDist );
            fprintf(fId, '%s \t %s (%s) \t %s (%s) \n','Percent less than by weight', 'Weight', labelUnitWt,'Dimension', labelUnitDist);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',0.0,alw0,ald0);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',15.0,alw15,ald15);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',50.0,alw50,ald50);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',85.0,alw85,ald85);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n\n',100.0,alw100,ald100);
            fprintf(fId, '%s %6.2f %s\n','Filter layer thickness = ',rfilter, labelUnitDist);
            fprintf(fId, '%s \t %s (%s) \t %s (%s) \n','Percent less than by weight', 'Weight', labelUnitWt,'Dimension', labelUnitDist);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',0.0,blw0,bld0);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',15.0,blw15,bld15);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',50.0,blw50,bld50);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n',85.0,blw85,bld85);
            fprintf(fId, '%3.1f \t\t\t\t %6.2f \t %6.2f \n\n',100.0,blw100,bld100);

            fprintf(fId, '%s \n','Irregular runup');
            fprintf(fId, '%s %6.2f %s \n','Conservative = ',runupr_conserv, labelUnitDist);
            fprintf(fId, '%s %6.2f %s \n','Expected Maximum = ',runupr_max, labelUnitDist);
        end
        
        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
        
        exportData = {Hs, Ts, cotnsl, ds, cotssl, unitwt, P, S};
        if length(errorMsg) > 0
            exportData = [exportData {errorMsg}];
        else
            exportData = [exportData {rarmor, alw0, ald0, alw15, ald15,...
                alw50, ald50, alw85, ald85, alw100, ald100, rfilter,...
                blw0, bld0, blw15, bld15, blw50, bld50, blw85, bld85,...
                blw100, bld100, runupr_conserv, runupr_max}];
        end
        exporter.writeData(exportData);
    end
end

if fileOutputData{1}
    fclose(fId);
end

exporter.close();