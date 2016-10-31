% Snell's Law applied to determine deepwater values

%   INPUT
%   alpha: wave crest angle with shoreline
%   c: wave celerity
%   cg: group velocity
%   c0: deepwater wave celerity
%   H: wave height

%   OUTPUT
%   alpha0: deepwater angle of wavecrest
%   H0: deepwater wave height

function [alpha0,H0]=LWTDWS(alpha,c,cg,c0,H)

deg2rad=pi/180;

arg=(c0/c)*sin(alpha*deg2rad);
assert(arg<1,'Error: Violation of assumptions for Snells Law')

alpha0=(asin(arg))/deg2rad;

ksf=sqrt(c0/(2*cg)); %shoaling coefficient
krf=sqrt(cos(alpha0*deg2rad)/cos(alpha*deg2rad)); %refraction coefficient
 
H0=H/(ksf*krf);
end
