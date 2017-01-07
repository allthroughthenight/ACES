% Miscellaneous linear wave theory bulk values

%   INPUT
%   cg: group velocity
%   h: still water depth at waveform
%   H: wave height
%   L: wave length
%   reldep: relative depth
%   rho: water density
%   g: gravitational acceleration
%   k: wavenumber

%   OUTPUT
%   E: mean energy density
%   P: mean energy flux
%   Ur: Ursell parameter
%   setdown: setdown

function [E,P,Ur,setdown]=LWTTWM(cg,h,H,L,reldep,rho,g,k)

E=(1/8)*rho*g*(H^2);
P=E*cg;
Ur=(H*(L^2))/(h^3);

if reldep<0.5
    setdown=(k*H^2)/(8*sinh(2*k*h));
else
    setdown=0;
end
end
