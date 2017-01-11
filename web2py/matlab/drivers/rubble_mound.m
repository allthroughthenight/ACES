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

addpath('../functions'); % Path to functions folder

#{
Hs=5.0;
Ts=10.0;
cotnsl=100.0;
ds=9.0;
cotssl=2.0;
unitwt=165.0;
P=0.1;
S=2.0;
N=7000;
#}

arg_list = argv();

Hs=str2num(arg_list{1});
Ts=str2num(arg_list{2});
cotnsl=str2num(arg_list{3});
ds=str2num(arg_list{4});
cotssl=str2num(arg_list{5});
unitwt=str2num(arg_list{6});
P=str2num(arg_list{7});
S=str2num(arg_list{8});
N=str2num(arg_list{9});

g=32.17;
rho=1.989;
H20weight=g*rho;
H20weight=64;

m=1/cotnsl;

[Hbs]=ERRWAVBRK2(Ts,m,ds);
assert(Hs<Hbs,'Error: Wave broken at structure (Hbs = %6.2f m)',Hbs)

[L,k]=WAVELEN(ds,Ts,50,g);

[steep,maxstp]=ERRSTP(Hs,ds,L);
assert(steep<maxstp,'Error: Wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

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

fprintf('%s %-6.2f \n','Armor layer thickness = ',rarmor)
fprintf('%s \t %s \t %s \n','Percent less than by weight', 'Weight','Dimension')
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',0.0,alw0,ald0);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',15.0,alw15,ald15);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',50.0,alw50,ald50);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',85.0,alw85,ald85);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n\n',100.0,alw100,ald100);
fprintf('%s %-6.2f \n','Filter layer thickness = ',rfilter)
fprintf('%s \t %s \t %s \n','Percent less than by weight', 'Weight','Dimension')
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',0.0,blw0,bld0);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',15.0,blw15,bld15);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',50.0,blw50,bld50);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n',85.0,blw85,bld85);
fprintf('%-3.1f \t\t\t\t\t\t\t %-6.2f \t %-6.2f \n\n',100.0,blw100,bld100);

fprintf('%s \n','Irregular runup')
fprintf('%s %-6.2f \n','Conservative = ',runupr_conserv)
fprintf('%s %-6.2f \n','Expected Maximum = ',runupr_max)


    





