% Deepwater duration-limited wave growth estimates: embodies open water and
% restricted fetch forms

%   INPUT
%   u: wind velocity
%   dur: wind duration
%   g: gravitational acceleration
%   ue: equivalent neutral windspeed (at 10 m)
%   wgtyp: wave-growth equation type
%           1 = open water (deep)
%           3 = restricted fetch (deep)

%   OUTPUT
%   Hdl: duration-limited wave height
%   Tdl: duration-limited wave period

function [Hdl,Tdl]=WGDL(u,dur,g,wgtyp)

tbar=g*dur/u;

if wgtyp==1
    %Open water - deep
    Hdl=0.0000851*(u^2/g)*tbar^(5/7);
    Tdl=0.0702*(u/g)*tbar^0.411;

elseif wgtyp==3
    %Restricted fetch - deep
    %u=uacos(phi)
    Hdl=0.000103*(u^2/g)*tbar^0.69;
    Tdl=0.082*(u/g)*tbar^0.39;  
end