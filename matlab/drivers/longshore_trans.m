clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Longshore Sediment Transport (page 6-1 in ACES User's Guide).
% Provides estimates of the potential longshore transport rate under the
% action of waves

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 21, 2011
% Date Modified: 

% Requires the following functions:
% DEEP_TRANS
% BREAK_TRANS

% MAIN VARIABLE LIST:
%   INPUT
%   H: Wave height (either deepwater or breaking) [ft]
%   alpha: wave angle (either deepwater angle of wave crest or crest angle
%          with shoreline) [deg]
%   K: dimensionless coefficient [default value 0.39]

%   OUTPUT
%   Q: sediment transport rate [yd^3/year]

%   OTHERS
%   g: gravity [32.17 ft/s^2]
%   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs/ft^3]
%   rhos: density of sediment [5.14 slugs/ft^3 in FORTRAN source code]
%-------------------------------------------------------------

addpath('../functions'); % Path to functions folder

H=3.75;
alpha=12.00;
K=0.39; 
g=32.17;

rho=1.989; %(64 lb/ft^3)/g = 1.989 slugs/ft^3
rhos=165.508/g; %bulk density of quartz is 165.508 lb/ft^3 - 165.508/g=5.14

fprintf('%s \n\n','Calculation options: ');
fprintf('%s \n','[1] Transport using deepwater wave conditions')
fprintf('%s \n\n','[2] Transport using breaking wave conditions')

option=input('Select option: ');
fprintf('\n')

if option==1
    [Q]=DEEP_TRANS(H,alpha,K,rho,g,rhos);
else
    [Q]=BREAK_TRANS(H,alpha,K,rho,g,rhos);
end

%Q=Q*1168800; %ACES conversion
Q=Q*1168775.04; %convert from ft^3/s to yd^3/yr

fprintf('%s \t %13.0f \n','Sediment transport rate', Q)
