clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Extremal Significant Wave Height Analysis (page 1-3 of ACES
% User's Guide). Provide significant wave height estimates for various
% return periods.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: May 13, 2011
% Date Verified: June 18, 2012

% Requires the following functions:
% ERRWAVBRK1

% MAIN VARIABLE LIST:
%   INPUT
%   Nt: estimated total number of events from the population during the
%       length of the record
%   K: length of the record in years
%   d: water depth
%   Hs: significant wave heights from long-term data source

%   OUTPUT
%   Hsr: significant wave height with return period Tr
%   sigr: standard deviation of significant wave height
%   pe: probability that a height with given return period will be equaled
%       or exceeded during some time period

%   OTHERS
%   yact: probability as estimated by the plotting forumula
%   yest: probability as estimated by the distribution
%   signr: normalized standard deviation of significant wave height with
%       return period Tr
%-------------------------------------------------------------

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

if single_case
% 	prompt = 'Enter Nt: estimated total number of events: ';
% 	Nt=input(prompt);
    [Nt] = USER_INPUT_DATA_VALUE('Enter Nt: estimated total number of events: ', 0.0, 10000.0);

% 	prompt = 'Enter K: length of the record in years: ';
% 	K=input(prompt);
    [K] = USER_INPUT_DATA_VALUE('Enter K: length of the record in years: ', 0.0, 999.9);

% 	prompt = 'Enter d: water depth: ';
% 	d=input(prompt);
    [d] = USER_INPUT_DATA_VALUE('Enter d: water depth: ', 0.0, 1000.0);

	fprintf('Hs: significant wave heights from long-term data source already entered');
	Hs=[9.32;8.11;7.19;7.06;6.37;6.15;6.03;5.72;4.92;4.90;4.78;4.67;4.64;4.19;3.06];
    % TODO
    % Set single case for each 'Hs' entry?
else
    % TODO 
    % Default multi-case block. Eventually to be repalced with csv/tsv file
    % reader
	Nt=20;
	K=20;
	d=500;
	Hs=[9.32;8.11;7.19;7.06;6.37;6.15;6.03;5.72;4.92;4.90;4.78;4.67;4.64;4.19;3.06];
end

N=length(Hs);
lambda=Nt/K;
nu=N/Nt;

Hs=Hs/0.3048;
d=d/0.3048;

[Hb]=ERRWAVBRK1(d,0.78);
for j=1:length(Hs)
    assert(Hs(j)<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)
end

ret=[1.0;1.1;1.2;1.3;1.4;1.5;1.6;1.7;1.8;1.9;2.0;5.0;10.0;25.0;50.0;100.0];

%Coefficients
k_W=[0.75,1.00,1.40,2.00];
a1=[0.64;1.65;1.92;2.05;2.24];
a2=[9.0;11.4;11.4;11.4;11.4];
kappa=[0.93;-0.63;0.00;0.69;1.34];
c=[0.0;0.0;0.3;0.4;0.5];
epsi=[1.33;1.15;0.90;0.72;0.54];

fprintf('%s \n\n','Confidence intervals: ');
fprintf('%s \n','[1] 80%')
fprintf('%s \n','[2] 85%')
fprintf('%s \n','[3] 90%')
fprintf('%s \n','[4] 95%')
fprintf('%s \n\n','[5] 99%')

option=input('Select option: ');
fprintf('\n')

pret=[1.0,2.0,5.0,10.0,25.0,50.0,100.0];
plen=pret;

Hs=sort(Hs,'descend');

for j=1:N
    yact(j,1)=1-(j-0.44)/(Nt+0.12); %FT-I
    ym(j,1)=-log(-log(yact(j,1)));
    for m=2:5
        k=k_W(m-1); %Weibull
        yact(j,m)=1.0-(j-0.20-0.27/sqrt(k))/(Nt+0.20+0.23/sqrt(k));
        ym(j,m)=(-log(1-yact(j,m)))^(1/k);
    end
end

Sx=sum(Hs);
Sy=sum(yact);
Sxx=sum(Hs.^2);
Slly=sum(ym);
Syy=sum(ym.^2);

for j=1:N
    for m=1:5
        Sxy(j,m)=(Hs(j).*ym(j,m));
    end
end
Sxy=sum(Sxy);

for m=1:5
    alpha(m)=(N*Sxy(m)-Sx*Slly(m))/(N*Syy(m)-Slly(m)^2);
    beta(m)=(1/N)*(Sx-alpha(m)*Slly(m));
end

for j=1:N
    yest(j,1)=exp(-exp(-(Hs(j)-beta(1))/alpha(1))); %FT-I
    for m=2:5
        k=k_W(m-1); %Weibull
        if (Hs(j)-beta(m))/alpha(m)>=0
            yest(j,m)=1.0-exp(-((Hs(j)-beta(m))/alpha(m))^k);
        else
            yest(j,m)=0;
        end
    end
end

for m=1:5
    for j=1:N
        st(j,m)=(yact(j,m)-yest(j,m))^2;
    end
end

sumresid=sum(st)/0.3048; %sum square of residuals

for m=1:5
    numer=N*Sxy(m)-Sx*Slly(m);
    term1d=N*Sxx-Sx^2;
    term2d=N*Syy(m)-Slly(m).^2;
    rxy(m)=numer/(sqrt(term1d*term2d)); %correlation coefficient
end

for j=1:length(ret)
    prob1=1-1/(lambda*ret(j));
    if prob1<=0
        prob1=1*10^(-7);
    end
    yr(j,1)=-log(-log(prob1)); %FT-I
    Hsr(j,1)=alpha(1)*yr(j,1)+beta(1);
    for m=2:5
        prob2=lambda*ret(j);
            if prob2<=0
                prob2=1*10^(-7);
            end
        k=k_W(m-1); %Weibull
        yr(j,m)=log(prob2)^(1/k);
        Hsr(j,m)=alpha(m)*yr(j,m)+beta(m);
    end
end

for j=1:N
    rtp(j,1)=1.0/((1-exp(-exp(-ym(j,1))))*lambda); %FT-I
    for m=2:5
        k=k_W(m-1); %Weibull
        rtp(j,m)=exp(ym(j,m)^k)/lambda;
    end
end

standev=std(Hs); %standard deviation
%Calculate confidence intervals
for m=1:5
    coeff=a1(m)*exp(a2(m)*N^(-1.3)+kappa(m)*sqrt(-log(nu)));
    for j=1:length(ret)
        signr=(1/sqrt(N))*(1.0+coeff*(yr(j,m)-c(m)+epsi(m)*log(nu))^2)^(1/2);
        sigr(j,m)=signr*standev;
    end
end

if option==1 %80%
    bounds=sigr.*1.28;
    conf=80;
elseif option==2 %85%
    bounds=sigr.*1.44;
    conf=85;
elseif option==3 %90%
    bounds=sigr.*1.65;
    conf=90;
elseif option==4 %95%
    bounds=sigr.*1.96;
    conf=95;
elseif option==5 %99%
    bounds=sigr.*2.58;
    conf=99;
end

for j=1:length(Hsr)
    for m=1:5
    lowbound(j,m)=Hsr(j,m)-bounds(j,m);
    highbound(j,m)=Hsr(j,m)+bounds(j,m);
    end
end

%Calculated percent chance for significant wave height equaling or
%exceeding the return period

for i=1:7
    for j=1:7
        pe(j,i)=100*(1-(1-1/pret(j))^plen(i));
    end
end

for i=1:N
    for m=1:5
        xxr(i,m)=ym(i,m)*alpha(m)+beta(m);
    end
end



peprint=pe(2:end,2:end);
printside=[999,2,5,10,25,50,100];
printside2=[2;5;10;25;50;100];
temp=cat(2,printside2,peprint);
printpe=cat(1,printside,temp);

index(1)=find(ret==2);
index(2)=find(ret==5);
index(3)=find(ret==10);
index(4)=find(ret==25);
index(5)=find(ret==50);
index(6)=find(ret==100);

fprintf('%s %-i %s %-3.2f %s %-i %s %-3.2f %s %-3.2f \n\n','N =',N,', NU =',nu,', NT =',Nt,', K =',K,', lambda =',lambda)
fprintf('\t\t\t\t %s \t\t\t %s \t %s \t %s \t %s \n','FT-I','W (k=0.75)','W (k=1.00)','W (k=1.40)','W (k=2.00)')
fprintf('%s \t %-6.4f \t\t %-6.4f \t\t %-6.4f \t\t %-6.4f \t\t %-6.4f \n', 'Corr. coeff.',rxy(1),rxy(2),rxy(3),rxy(4),rxy(5))
fprintf('%s \t %-6.4f \t\t %-6.4f \t\t %-6.4f \t\t %-6.4f \t\t %-6.4f \n\n', 'Sq. of Resid.',sumresid(1),sumresid(2),sumresid(3),sumresid(4),sumresid(5))

fprintf('%s \t %s \t\t %s \t\t %s \t\t %s \t\t %s \n','Return period','Hs [m]','Hs [m]','Hs [m]','Hs [m]','Hs [m]')
for m=1:6
    if m<6
        fprintf('%-i \t\t\t\t %-6.2f \t\t %-6.2f \t\t %-6.2f \t\t %-6.2f \t\t %-6.2f \n',ret(index(m)),Hsr(index(m),1),Hsr(index(m),2),Hsr(index(m),3),...
            Hsr(index(m),4),Hsr(index(m),5))
    else
        fprintf('%-i \t\t\t %-6.2f \t\t %-6.2f \t\t %-6.2f \t\t %-6.2f \t\t %-6.2f \n\n',ret(index(m)),Hsr(index(m),1),Hsr(index(m),2),Hsr(index(m),3),...
            Hsr(index(m),4),Hsr(index(m),5))
    end
end

[val,C]=max(rxy);
if C==1
    fprintf('%s \n\n','Best fit distribution function: Fisher-Tippett Type I')
elseif C==2
    fprintf('%s \n\n','Best fit distribution function: Weibull Distribution (k=0.75)')
elseif C==3
    fprintf('%s \n\n','Best fit distribution function: Weibull Distribution (k=1.00)')
elseif C==4
    fprintf('%s \n\n','Best fit distribution function: Weibull Distribution (k=1.40)')
elseif C==5
    fprintf('%s \n\n','Best fit distribution function: Weibull Distribution (k=2.00)')
end

fprintf('%i %s %s \n',conf,'% ','Confidence Interval, (Lower Bound - Upper Bound)')
fprintf('%s \n','Return period')

for m=1:6
    if m<6
        fprintf('%-i \t\t\t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t \n',ret(index(m)),lowbound(index(m),1),'-',highbound(index(m),1),...
            lowbound(index(m),2),'-',highbound(index(m),2),lowbound(index(m),3),'-',highbound(index(m),3),lowbound(index(m),4),'-',highbound(index(m),4),lowbound(index(m),5),'-',highbound(index(m),5))
    else
        fprintf('%-i \t\t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t %-3.1f %c %-3.1f \t \n\n',ret(index(m)),lowbound(index(m),1),'-',highbound(index(m),1),...
            lowbound(index(m),2),'-',highbound(index(m),2),lowbound(index(m),3),'-',highbound(index(m),3),lowbound(index(m),4),'-',highbound(index(m),4),lowbound(index(m),5),'-',highbound(index(m),5))
    end
end

fprintf('%s \n','Percent Chance for Significant Height Equaling or Exceeding Return Period Hs')
disp(round(printpe))

for m=1:5
    figure(m)
    semilogx(ret,Hsr(:,m),':',rtp(:,m),Hs,ret,highbound(:,m),'r--',ret,lowbound(:,m),'r--')
    if m==1
        title('FT-I')
        ylabel('H_s')
        xlabel('Return period [yr]')
        legend('FT-I Distribution','Data','Confidence Bounds','Location','SouthEast')
    elseif m==2
        title('Weibull (k=0.75)')
        ylabel('H_s')
        xlabel('Return period [yr]')
        legend('Weibull (k=0.75)','Data','Confidence Bounds','Location','SouthEast')
    elseif m==3
        title('Weibull (k=1.00)')
        ylabel('H_s')
        xlabel('Return period [yr]')
        legend('Weibull (k=1.00)','Data','Confidence Bounds','Location','SouthEast')
    elseif m==4
        title('Weibull (k=1.40)')
        ylabel('H_s')
        xlabel('Return period [yr]')
        legend('Weibull (k=1.40)','Data','Confidence Bounds','Location','SouthEast')
    elseif m==5
        ylabel('H_s')
        title('Weibull (k=2.00)')
        xlabel('Return period [yr]')
        legend('Weibull (k=2.00)','Data','Confidence Bounds','Location','SouthEast')
    end
end
