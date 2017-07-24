clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Cnoidal Wave Theory (page 2-2 in ACES User's Guide)
% Yields first-order and second-order approximations for various wave
% parameters of wave motion as predicted by cnoidal wave theory

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: March 18, 2011
% Date Modified:7/21/16 -yaprak

% Requires the following functions:
% ERRWAVBRK1

% MAIN VARIABLE LIST:
%   INPUT
%   H: wave height (m)
%   T: wave period (sec)
%   d: water depth (m)
%   z: vertical coordinate (m)
%   xL: horizontal coordinate as fraction of wavelength (x/L)
%   time: time-coordinate (default=0)
%   O: order approximation (1 or 2)

%   OUTPUT
%   L: wavelength (m)
%   C: wave celerity (m/s)
%   E: energy density (N-m/m^2)
%   Ef: energy flux (N-m/m-s)
%   Ur: Ursell number
%   eta: surface elevation (m)
%   u: horizontal particle velocity (m/s)
%   w: vertical particle velocity (m/s)
%   dudt: horizontal particle acceleration (m/s^2)
%   dwdt: vertical particle accleration (m/s^2)
%   pres: pressure (N/m^2)

%   OTHERS
%   K: complete elliptic intergral of the first kind
%   E: complete elliptical intergral of the second kind
%   m: optimized parameter
%   lambda: simplification term ((1-m)/m)
%   mu: simplification term (E/(K*m))git
%   epsi: perturbation parameter (H/d)
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[water, rho] = USER_INPUT_SALT_FRESH_WATER(metric);

if single_case
    [H] = USER_INPUT_DATA_VALUE(['Enter H: wave height (' labelUnitDist '): '], 0.1, 200.0);

    [T] = USER_INPUT_DATA_VALUE('Enter T: wave period (sec): ', 1.0, 1000.0);

    [d] = USER_INPUT_DATA_VALUE(['Enter d: water depth (' labelUnitDist '): '], 0.1, 5000.0);
    
    [z] = USER_INPUT_DATA_VALUE(['Enter z: vertical coordinate (' labelUnitDist '): '], -5100.0, 100.0);
    
    [xL] = USER_INPUT_DATA_VALUE('Enter xL: horizontal coordinate as fraction of wavelength (x/L): ', 0.0, 1.0);
    
    numCases = 1;
else
    multiCaseData = {...
            ['H: wave height (' labelUnitDist ')'], 0.1, 200.0;...
            'T: wave period (sec)', 1.0, 1000.0;...
            ['d: water depth (' labelUnitDist ')'], 0.1, 5000.0;...
            ['z: vertical coordinate (' labelUnitDist ')'], -5100.0, 100.0;...
            'xL: horizontal coordinate as fraction of wavelength (x/L)', 0.0, 1.0};
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HList = varData(1, :);
    TList = varData(2, :);
    dList = varData(3, :);
    zList = varData(4, :);
    xLList = varData(5, :);
end

twopi=2*pi;

O = 0;
while O ~= 1 && O ~= 2
    prompt = 'Enter O: order approximation (1 or 2): ';
    O = input(prompt);
end

prompt = 'Enter time: time-coordinate (default=0): ';
time = input(prompt);


% File Output
fileOutputArgs = {'Enter the filename (no extension): ', 'Enter the description for this file: '};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);
if fileOutputData{1}
    fId = fopen(['output\' fileOutputData{2} '.txt'], 'wt');
    fprintf(fId, '%s\n\n', fileOutputData{3});
end


for loopIndex = 1:numCases
    if ~single_case
        H = HList(loopIndex);
        T = TList(loopIndex);
        d = dList(loopIndex);
        z = zList(loopIndex);
        xL = xLList(loopIndex);
    end
    
    errorMsg = '';
    
    epsi=H/d;

    [Hb]=ERRWAVBRK1(d,0.78);
%     assert(H<Hb,'Error: Input wave broken (Hb = %6.2f %s)',Hb,labelUnitDist)
    if not(H<Hb)
        errorMsg = sprintf('Error: Input wave broken (Hb = %6.2f %s)',Hb,labelUnitDist);
        disp(errorMsg);
    else
        %% First Order Approximation
        if O==1 %determining m using bisection method
            a=1*10^-12;
            b=1-10^-12;
            F=@(m)(16*m*ellipke(m)^2/3)-(g*H*T^2/d^2);
            while (b-a)/2>=0.00001
                xi=(a+b)/2;
                if F(xi)==0
                    break
                else
                    if F(xi)*F(b)<0
                        a=xi;
                    elseif F(xi)*F(a)<0
                        b=xi;
                    end
                end
            end
            m=xi;

            [K,E]=ellipke(m);

            lambda=(1-m)/m;
            mu=E/(m*K);
            theta=2*K*(xL-(time/T));

            C0=1;
            C1=(1+2*lambda-3*mu)/2;
            C=sqrt(g*d)*(C0+epsi*C1); %celerity

            L=C*T; %wave length

            Ur=(H*(L^2))/(d^3);
%             assert(Ur>26,'Error: Ursell parameter test failed.')
            if not(Ur>26)
                errorMsg = 'Error: Ursell parameter test failed.';
                disp(errorMsg);
            else
                [SN,CN,DN] = ellipj(theta,m);
                CSD=CN*SN*DN;

                A0=epsi*(lambda-mu);
                A1=epsi;
                eta=d*(A0+A1*CN^2); %water surface elevation

%                 assert(z<eta && (z+d)>0,'Error: Point outside waveform.')
                if not(z<eta)
                    errorMsg = 'Error: Point outside waveform.';
                    disp(errorMsg);
                else
                    E0=(-lambda+2*mu+4*lambda*mu-lambda^2-3*mu^2)/3;
                    E=rho*g*H^2*E0; %average energy density

                    F0=E0;
                    Ef=rho*g*H^2*sqrt(g*d)*F0; %energy flux

                    B00=epsi*(lambda-mu);
                    B10=epsi;
                    u=sqrt(g*d)*(B00+B10*CN^2); %horizontal velocity

                    w=sqrt(g*d)*(4*K*d*CSD/L)*((z+d)/d)*B10; %vertical velocity

                    dudt=sqrt(g*d)*B10*(4*K/T)*CSD; %horizontal acceleration

                    term=sqrt(g*d)*(4*K*d/L)*((z+d)/d)*B10*(2*K/T);
                    dwdt=term*((SN*DN)^2-(CN*DN)^2+(m*SN*CN)^2); %vertical acceleration

                    P1=(1+2*lambda-3*mu)/2;
                    P0=3/2;
                    Pb=rho*g*d*(P0+epsi*P1);
                    pres=Pb-(rho/2)*((u-C)^2+w^2)-g*rho*(z+d); %pressure

                    disp('First Order Approximations')
                    fprintf('%s \t\t\t %-6.2f %s \t \n','Wavelength',L,labelUnitDist);
                    fprintf('%s \t\t\t %-6.2f %s/sec \t \n','Celerity',C,labelUnitDist);
                    fprintf('%s \t\t %-8.2f %s-%s/%s^2 \t \n','Energy density',E,labelUnitDist,labelUnitWt,labelUnitDist);
                    fprintf('%s \t\t %-8.2f %s-%s/sec-%s \t \n','Energy flux',Ef,labelUnitDist,labelUnitWt,labelUnitDist);
                    fprintf('%s \t\t %-6.2f \n','Ursell number',Ur);
                    fprintf('%s \t\t\t %-6.2f %s \t \n','Elevation',eta,labelUnitDist);
                    fprintf('%s \t\t %-6.2f %s/sec \t \n','Horz. velocity',u,labelUnitDist);
                    fprintf('%s \t\t %-6.2f %s/sec \t \n','Vert. velocity',w,labelUnitDist);
                    fprintf('%s \t %-6.2f %s/sec^2 \t \n','Horz. acceleration',dudt,labelUnitDist);
                    fprintf('%s \t %-6.2f %s/sec^2 \t \n','Vert. acceleration',dwdt,labelUnitDist);
                    fprintf('%s \t\t\t %-8.2f %s/%s^2 \t \n','Pressure',pres,labelUnitWt,labelUnitDist);
                end
            end

        % Second Order Approximations
        elseif O==2 %determining m using bisection method
            a=1*10^-12;
            b=1-10^-12;
            F=@(m)(16*m*ellipke(m)^2/3)-(g*H*T^2/d^2)*(1-epsi*((1+2*((1-m)/m))/4));
            while (b-a)/2>=0.00001
                xi=(a+b)/2;
                if F(xi)==0
                    break
                else
                    if F(xi)*F(b)<0
                        a=xi;
                    elseif F(xi)*F(a)<0
                        b=xi;
                    end
                end
            end
            m=xi;
            [K,E]=ellipke(m);
            lambda=(1-m)/m;
            mu=E/(m*K);

            theta=2*K*(xL-(time/T));
            [SN,CN,DN] = ellipj(theta,m);
            CSD=CN*SN*DN;

            C2=(-6-16*lambda+5*mu-16*lambda^2+10*lambda*mu+15*mu^2)/40;
            C1=(1+2*lambda-3*mu)/2;
            C0=1;
            C=sqrt(g*d)*(C0+epsi*C1+epsi^2*C2); %celerity

            L=C*T; %wave length

            Ur=(H*(L^2))/(d^3);
%             assert(Ur>26,'Error: Ursell parameter test failed.')
            if not(Ur>26)
                errorMsg = 'Error: Ursell parameter test failed.';
                disp(errorMsg);
            else
                A2=(3/4)*epsi^2;
                A1=epsi-A2;
                A0=epsi*(lambda-mu)+epsi^2*((-2*lambda+mu-2*lambda^2+2*lambda*mu)/4);
                eta=d*(A0+A1*CN^2+A2*CN^4); %wave surface elevation

%                 assert(z<eta && (z+d)>0,'Error: Point outside waveform.')
                if not(z<eta)
                    errorMsg = 'Error: Point outside waveform.';
                    disp(errorMsg);
                else
                    E1=(1/30)*(lambda-2*mu-17*lambda*mu+3*lambda^2-17*lambda^2*mu+2*lambda^3+15*mu^3);
                    E0=(-lambda+2*mu+4*lambda*mu-lambda^2-3*mu^2)/3;
                    E=rho*g*H^2*(E0+epsi*E1); %average energy density

                    F1=(1/30)*(-4*lambda+8*mu+53*lambda*mu-12*lambda^2-60*mu^2+53*lambda^2*mu-120*lambda*mu^2 ...
                        -8*lambda^3+75*mu^3);
                    F0=E0;
                    Ef=rho*g*H^2*sqrt(g*d)*(F0+epsi*F1); %energy flux

                    term=(z+d)/d;

                    B21=-(9/2)*epsi^2;
                    B11=3*epsi^2*(1-lambda);
                    B01=((3*lambda)/2)*epsi^2;
                    B20=-(epsi^2);
                    B10=epsi+epsi^2*((1-6*lambda+2*mu)/4);
                    B00=epsi*(lambda-mu)+epsi^2*((lambda-mu-2*lambda^2+2*mu^2)/4);
                    u=sqrt(g*d)*((B00+B10*CN^2+B20*CN^4)-(1/2)*term^2*(B01+B11*CN^2+B21*CN^4)); %horizontal velocity

                    w1=term*(B10+2*B20*CN^2);
                    w2=(1/6)*term^3*(B11+2*B21*CN^2);
                    w=sqrt(g*d)*(4*K*d*CSD/L)*(w1-w2); %vertical velocity

                    u1=(B10-(1/2)*term^2*B11)*(4*K*CSD/T);
                    u2=(B20-(1/2)*term^2*B21)*(8*K*CN^2*CSD/T);
                    dudt=sqrt(g*d)*(u1+u2); %horizontal acceleration

                    w1=(8*K*CSD^2/T)*(term*B20-(1/6)*term^3*B21);
                    w2=term*(B10+2*B20*CN^2)-(1/6)*term^3*(B11+2*B21*CN^2);
                    w3=(2*K/T)*((SN*DN)^2-(CN*DN)^2+(m*SN*CN)^2);
                    dwdt=sqrt(g*d)*(4*K*d/L)*(w1+w2*w3); %vertical acceleration

                    P2=(-1-16*lambda+15*mu-16*lambda^2+30*lambda*mu)/40;
                    P1=(1+2*lambda-3*mu)/2;
                    P0=3/2;
                    Pb=rho*g*d*(P0+epsi*P1+epsi^2*P2);
                    pres=Pb-(rho/2)*((u-C)^2+w^2)-g*rho*(z+d);

                    disp('Second Order Approximations')
                    fprintf('%s \t\t\t %-6.2f %s \t \n','Wavelength',L,labelUnitDist);
                    fprintf('%s \t\t\t %-6.2f %s/sec \t \n','Celerity',C,labelUnitDist);
                    fprintf('%s \t\t %-8.2f %s-%s/%s^2 \t \n','Energy density',E,labelUnitDist,labelUnitWt,labelUnitDist);
                    fprintf('%s \t\t %-8.2f %s-%s/sec-%s \t \n','Energy flux',Ef,labelUnitDist,labelUnitWt,labelUnitDist);
                    fprintf('%s \t\t %-6.2f \n','Ursell number',Ur);
                    fprintf('%s \t\t\t %-6.2f %s \t \n','Elevation',eta,labelUnitDist);
                    fprintf('%s \t\t %-6.2f %s/sec \t \n','Horz. velocity',u,labelUnitDist);
                    fprintf('%s \t\t %-6.2f %s/sec \t \n','Vert. velocity',w,labelUnitDist);
                    fprintf('%s \t %-6.2f %s/sec^2 \t \n','Horz. acceleration',dudt,labelUnitDist);
                    fprintf('%s \t %-6.2f %s/sec^2 \t \n','Vert. acceleration',dwdt,labelUnitDist);
                    fprintf('%s \t\t\t %-8.2f %s/%s^2 \t \n','Pressure',pres,labelUnitWt,labelUnitDist);
                end
            end
        end
    end
    
    if fileOutputData{1}
        if ~single_case
            fprintf(fId, 'Case #%d\n\n', loopIndex);
        end

        fprintf(fId, 'Input\n');
        fprintf(fId, 'Wave height\t\t\t%8.2f %s\n', H, labelUnitDist);
        fprintf(fId, 'Wave period\t\t\t%8.2f s\n', T);
        fprintf(fId, 'Water depth\t\t\t%8.2f %s\n', d, labelUnitDist);
        fprintf(fId, 'Vertical coordinate\t\t%8.2f %s\n', z, labelUnitDist);
        fprintf(fId, 'Horizontal coordinate\t\t%8.2f\n  as fraction of wavelength (x/L)\n', xL);

        if length(errorMsg) > 0
            fprintf(fId, '\n%s\n', errorMsg);
        else
            if O == 1
                fprintf(fId, '\nFirst Order Approximations\n');
            else
                fprintf(fId, '\nSecond Order Approximations\n');
            end

            fprintf(fId, '%s \t\t %8.2f %s\n','Wavelength',L,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f %s/sec\n','Celerity',C,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f %s-%s/%s^2\n','Energy density',E,labelUnitDist,labelUnitWt,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f %s-%s/sec-%s\n','Energy flux',Ef,labelUnitDist,labelUnitWt,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f\n','Ursell number',Ur);
            fprintf(fId, '%s \t\t %8.2f %s\n','Elevation',eta,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f %s/sec\n','Horz. velocity',u,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f %s/sec\n','Vert. velocity',w,labelUnitDist);
            fprintf(fId, '%s \t %8.2f %s/sec^2\n','Horz. acceleration',dudt,labelUnitDist);
            fprintf(fId, '%s \t %8.2f %s/sec^2\n','Vert. acceleration',dwdt,labelUnitDist);
            fprintf(fId, '%s \t\t %8.2f %s/%s^2\n','Pressure',pres,labelUnitWt,labelUnitDist);
        end

        if loopIndex < numCases
            fprintf(fId, '\n--------------------------------------\n\n');
        end
    end
end

if fileOutputData{1}
    fclose(fId);
end

if single_case && length(errorMsg) == 0
    if O == 1
        %Plotting waveform
        plotxL=(-1:0.001:1);
        plottheta=2*K*(plotxL-(time/T));
        [pSN,pCN,pDN] = ellipj(plottheta,m);
        pCSD=pSN.*pCN.*pDN;

        ploteta=d*(A0+A1*pCN.^2);
        plotu=sqrt(g*d)*(B00+B10*pCN.^2);
        plotw=sqrt(g*d)*(4*K*d*pCSD/L)*((z+d)/d)*B10;

        subplot(3,1,1); plot(plotxL,ploteta); ylim([min(ploteta)-1 max(ploteta)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Elevation [' labelUnitDist ']'])

        subplot(3,1,2); plot(plotxL,plotu); ylim([min(plotu)-1 max(plotu)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Velocity, u [' labelUnitDist '/s]'])

        subplot(3,1,3); plot(plotxL,plotw); ylim([min(plotw)-1 max(plotw)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Velocity, w [' labelUnitDist '/s]'])
        xlabel('x/L')
    elseif O == 2
        %Plotting waveform
        plotxL=(-1:0.001:1);
        plottheta=2*K*(plotxL-(time/T));
        [pSN,pCN,pDN] = ellipj(plottheta,m);
        pCSD=pSN.*pCN.*pDN;

        ploteta=d*(A0+A1*pCN.^2+A2*pCN.^4);
        plotu=sqrt(g*d)*((B00+B10*pCN.^2+B20*pCN.^4)-(1/2)*((z+d)/d)^2*(B01+B11*pCN.^2+B21*pCN.^4));

        pw1=((z+d)/d)*(B10+2*B20*pCN.^2);
        pw2=(1/6)*(((z+d)/d)^3)*(B11+2*B21*pCN.^2);
        plotw=sqrt(g*d)*(4*K*d*pCSD/L).*(pw1-pw2);

        subplot(3,1,1); plot(plotxL,ploteta); ylim([min(ploteta)-1 max(ploteta)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Elevation [' labelUnitDist ']'])

        subplot(3,1,2); plot(plotxL,plotu); ylim([min(plotu)-1 max(plotu)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Velocity, u [' labelUnitDist '/s]'])

        subplot(3,1,3); plot(plotxL,plotw); ylim([min(plotw)-1 max(plotw)+1])
        hline = refline_v2([0 0]);
        set(hline,'Color','r','LineStyle','--')
        ylabel(['Velocity, w [' labelUnitDist '/s]'])
        xlabel('x/L')
    end
    
    if fileOutputData{1}
        fId = fopen(['output\' fileOutputData{2} '_plot.txt'], 'wt');

        fprintf(fId, 'Partial Listing of Plot Output File 1 for %s\n\n', fileOutputData{3});

        fprintf(fId, 'X/L\tETA (%s)\tU (%s/sec)\tW (%s/sec)\n', labelUnitDist,labelUnitDist,labelUnitDist);

        for loopIndex = 1:length(plotxL)
            fprintf(fId, '%-6.3f\t%-6.3f\t\t%-6.3f\t\t%-6.3f\n',...
                plotxL(loopIndex),...
                ploteta(loopIndex),...
                plotu(loopIndex),...
                plotw(loopIndex));
        end
        
        fclose(fId);
    end
end