clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Beta-Rayleigh Distribution (page 1-2 of ACES User's Guide).
% Provides a statistical representation for a shallow-water wave height
% distribution.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 28, 2011
% Date Verified: June 27, 2012

% Requires the following functions:
% ERRWAVBRK1
% WAVELEN
% ERRSTP

% MAIN VARIABLE LIST:
%   INPUT
%   Hmo: zero-moment wave height [m]
%   Tp: peak wave period [s]
%   d: water depth [m]

%   OUTPUT
%   Hrms: root-mean-square wave height [m]
%   Hmed: median wave height [m]
%   H13: significant wave height (average of the 1/3 highest waves) [m]
%   H110: average of the 1/10 highest waves [m]
%   H1100: average of the 1/100 highest waves [m]

%   OTHER:
%------------------------------------------------------------
addpath('../functions'); % Path to functions folder

#{
Hmo=10.0;
Tp=11.5;
d=25.00;
#}

arg_list = argv();

Hmo=str2num(arg_list{1});
Tp=str2num(arg_list{2});
d=str2num(arg_list{3});

ft2m=0.3048;
g=32.17;

Htype(1)=0.50; %Hmed;
Htype(2)=0.66; %H1/3 (1-1/3);
Htype(3)=0.90; %H1/10 (1-1/10);
Htype(4)=0.99; %H1/100 (1-1/100);

[Hb]=ERRWAVBRK1(d,0.9);
assert(Hmo<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)

[L,k]=WAVELEN(d,Tp,50,g);
[steep,maxstp]=ERRSTP(Hmo,d,L);
assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

dterm=d/(g*Tp^2);
k=1;
sum1=0;

if dterm>0.01
    disp('Input conditions indicate Rayleigh distribution');
    Hb=sqrt(5)*Hmo;
    Hinc=Hb/10000;
    sigma=Hmo/4;
    Hrms=2*sqrt(2)*sigma;
    
    for i=2:10001
        %Rayleigh distribution
        H(i)=Hinc*(i-1);
        term1=exp(-(H(i)/Hrms)^2);
        term2=(2*H(i))/Hrms^2;
        p(i)=term1*term2;
        
        sum1=sum1+(p(i)*Hinc);
        if k<5 && sum1>Htype(k)
            index(k)=i;
            k=k+1;
        end
    end
    
    for k=2:4
        sum2=0;
        Hstart=H(index(k));
        Hinc=(Hb-Hstart)/10000;
        pprv=p(index(k));
        Hprv=Hstart;
        for i=2:10000
            Hnxt=Hstart+Hinc*(i-1);
            term1=exp(-(Hnxt/Hrms)^2);
            term2=(2*Hnxt)/Hrms^2;
            pnxt=term1*term2;
            darea=0.5*(pprv+pnxt)*Hinc; %area of a trapezoid
            sum2=sum2+(Hinc/2.0+Hprv)*darea;
            pprv=pnxt;
            Hprv=Hnxt;
        end
        Hout(k)=sum2/(1-Htype(k)); %computing centroid (areasum = 1-Htype)
    end
else
    Hb=d;
    Hinc=Hb/100;
    disp('Input conditions indicate Beta-Rayleigh distribution')
    a1=0.00089;
    b1=0.834;
    a2=0.000098;
    b2=1.208;
    
    d1=a1*dterm^(-b1);
    assert(d1<35.0,'Error: d/gT^2 approaching infinity')
    Hrms=(1/sqrt(2))*exp(d1)*Hmo; %root-mean-square wave height
    
    d2=a2*dterm^(-b2);
    assert(d2<35.0,'Error: d/gT^2 approaching infinity')
    
    Hrmsq=(1/sqrt(2))*exp(d2)*Hmo^2; %root-mean-quad wave heigth
    
    %Computing alpha and beta
    K1=(Hrms/Hb)^2;
    K2=(Hrmsq^2)/(Hb^4);
    
    alpha=(K1*(K2-K1))/(K1^2-K2);
    beta=((1-K1)*(K2-K1))/(K1^2-K2);
    
    term1=(2*gamma(alpha+beta))/(gamma(alpha)*gamma(beta));
    
    for i=1:101
        %Beta-Rayleigh distribution
        H(i)=Hinc*(i-1);
        term2=(H(i)^(2*alpha-1))/(Hb^(2*alpha));
        term3=(1-(H(i)/Hb)^2)^(beta-1);
        p(i)=term1*term2*term3;
        
        sum1=sum1+(p(i)*Hinc);
        if k<5 && sum1>Htype(k)
            index(k)=i;
            k=k+1;
        end
    end
    
    for k=2:4
        sum2=0;
        Hstart=H(index(k));
        Hinc=(Hb-Hstart)/20;
        pprv=p(index(k));
        Hprv=Hstart;
        for i=2:20
            Hnxt=Hstart+Hinc*(i-1);
            term2=(Hnxt^(2*alpha-1))/(Hb^(2*alpha));
            term3=(1-(Hnxt/Hb)^2)^(beta-1);
            pnxt=term1*term2*term3;
            darea=0.5*(pprv+pnxt)*Hinc; %area of a trapezoid
            sum2=sum2+(Hinc/2.0+Hprv)*darea;
            pprv=pnxt;
            Hprv=Hnxt;
        end
        Hout(k)=sum2/(1-Htype(k)); %computing centroid (areasum = 1-Htype)
    end
end
Hmed=H(index(1));

table=cat(2,H',p');

#{
plot(Hout(2),0,'ks',Hout(3),0,'ro',Hout(4),0,'bd',Hrms,0,'g*',Hmed,0,'m^',table(:,1),table(:,2));
legend('H_{1/3}','H_{1/10}','H_{1/100}','H_{rms}','H_{med}')
xlabel('H [m]')
ylabel('Probability density p(H)')
#}

fprintf('\n %s \n','Wave heights')
fprintf('\t %s \t\t %-6.2f \n','Hrms',Hrms)
fprintf('\t %s \t\t %-6.2f \n','Hmed',Hmed)
fprintf('\t %s \t %-6.2f \n','H(1/3)',Hout(2))
fprintf('\t %s \t %-6.2f \n','H(1/10)',Hout(3))
fprintf('\t %s \t %-6.2f \n','H(1/100)',Hout(4))

