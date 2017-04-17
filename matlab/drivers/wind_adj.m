clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Windspeed Adjustment and Wave Growth (page 1-1 of ACES User's
% Guide). Provide estimates for wave growth over open-water and restricted
% fetches in deep and shallow water.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 28, 2011
% Date Modified:

% Requires the following functions:
% ERRWAVBRK1
% WADJ
% WAGEOS
% WAPBL
% WAPSI
% WASBL
% WASHR
% WGDL
% WGFD
% WGFET
% WGFL
% WGRO

% MAIN VARIABLE LIST:
%   INPUT
%   zobs: elevation of observed winds [m]
%   uobs: observed wind speed [m/s]
%   dtemp: air-sea temperature difference [deg C]
%   duro: duration of observed wind [hr]
%   durf: duration of final wind [hr]
%   lat: latitude of wind observation [deg]
%   windobs: wind observation type
%   fetchopt: wind fetch options
%   wgtyp: open water wave growth equation options

%   OPEN-WATER VARIABLES
%   F: length of wind fetch [m]
%   d: average depth of fetch (only for shallow water equations) [m]

%   RESTRICTED VARIABLES
%   wdir: wind direction [deg]
%   dang: radial angle increment [deg]
%   ang1: direction of first radial fetch [deg]
%   angs: fetch length [m]

%   OUTPUT
%   ue: equivalent neutral wind speed [m/s]
%   ua: adjusted wind speed [m/s]
%   Hmo: wave height [m]
%   Tp: peak wave period [s]
%   wg: type of wave-growth
%   theta: wave direction with respect to N [deg]

%   OTHERS
%-------------------------------------------------------------

addpath('../functions'); % Path to functions folder

single_case=true;
zobs=12;
uobs=17;
dtemp=2;
duro=1;
durf=4;
lat=28;

assert(lat~=0, 'Error: Latitude must be a non-zero value.')

fprintf('%s \n','Wind observation types: ');
fprintf('%s \n','[1] Overwater (shipboard)')
fprintf('%s \n','[2] Overwater (not shipboard)')
fprintf('%s \n','[3] Shore (windward - offshore to onshore)')
fprintf('%s \n','[4] Shore (leeward - onshore to offshore)')
fprintf('%s \n','[5] Over land')
fprintf('%s \n\n','[6] Geostrophic wind')

windobs=input('Select option: ');
fprintf('\n')

fprintf('%s \n','Wind fetch and wave growth options: ');
fprintf('%s \n','[1] Open Water - Deep')
fprintf('%s \n','[2] Open Water - Shallow')
fprintf('%s \n','[3] Restricted - Deep')
fprintf('%s \n\n','[4] Restricted - Shallow')

wgtyp=input('Select option: ');
fprintf('\n')

if wgtyp==1 %Open Water - Deep
    F=27;
    d=0;
    phi=0;
elseif wgtyp==2 %Open Water - Shallow
    F=27;
    d=13;
    phi=0;
elseif wgtyp==3 %Restricted - Deep
    d=0;
    wdir=120;
    dang=12;
    ang1=0;
    angs=[3.7;12.3;13.4;12.2;13.2;36.0;35.6;28.7;26.8;13.0;10.4;10.1;6.4;5.7];
    [F,phi,theta]=WGFET(ang1,dang,wdir,angs);
else %Restricted - Shallow
    d=13;
    wdir=120;
    dang=12;
    ang1=0;
    angs=[3.7;12.3;13.4;12.2;13.2;36.0;35.6;28.7;26.8;13.0;10.4;10.1;6.4;5.7];
    %angs=[3.7;12.3;13.4;12.2;13.2;36.0;35.6;28.7;10.4;5.7];
    [F,phi,theta]=WGFET(ang1,dang,wdir,angs);
end

%Conversion to metric units
ft2m=0.3048;
mph2mps=0.44704;
hr2s=3600;
min2s=60;
deg2rad=pi/180;
mi2m=1609.344;
F2C=5/9;
knots2mps=0.5144;

[ue]=WADJ(uobs*mph2mps,zobs*ft2m,dtemp,F*mi2m,duro*hr2s,durf*hr2s,lat*deg2rad,windobs);

[ua,Hmo,Tp,wgmsg]=WGRO(d*ft2m,F*mi2m,phi,durf*hr2s,ue,wgtyp);

fprintf('%s %s \n','Wave growth: ',wgmsg)
if wgtyp==3 || wgtyp==4
    fprintf('%s \t %-6.2f \n','Mean wave direction',theta)
    fprintf('%s \t\t\t\t %-6.2f \n','Wind fetch',F)
end
fprintf('%s \t\t %-6.2f \n','Equiv. wind speed ',ue/mph2mps)
fprintf('%s \t\t %-6.2f \n','Adjus. wind speed ',ua/mph2mps)

fprintf('%s \t\t\t %-6.2f \n','Wave height ',Hmo/ft2m)
fprintf('%s \t\t\t %-6.2f \n','Wave period ',Tp)
