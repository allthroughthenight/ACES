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

addpath('../functions'); % Path to functions folder

H=2.0;
T=10.0;
ds=9.6;
nummat=1; 
d50=[1.46];
por=[0.37];
hs=10.5;
cotssl=1.0;
b=8.5;
numlay=1;
th=[9.60];
hlen=[25.60];

g=32.17;
nu=0.0000141; %ft^2/s

[Hb]=ERRWAVBRK1(ds,0.78);
assert(H<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)

[L,k]=WAVELEN(ds,T,50,g);

[steep,maxstp]=ERRSTP(H,ds,L);
assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

assert(ds<hs,'Error: Method does not apply to submerged structures.')

assert(sum(th)==ds,'Error: Water depth must equal sum of all layer thicknesses.')

[KTt,Kto,KT,Kr,Ht,L]=MADSEELG(H,T,ds,hs,b,numlay,th,hlen,nummat,d50,por,cotssl,nu,g);

fprintf('%s \t\t\t %-6.3f \n','Reflection coefficient', Kr)
fprintf('%s \n','Wave transmission coefficient')
fprintf('%s \t %-6.3f \n','Wave Transmission (Through)', KTt)
fprintf('%s  %-6.3f \n','Wave Transmission (Overtopping)', Kto)
fprintf('%s \t\t %-6.3f \n','Wave Transmission (Total)', KT)
fprintf('%s \t\t %-6.2f \n','Transmitted wave height', Ht)


