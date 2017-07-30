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

function [alpha0,H0,errorMsg]=LWTDWS(alpha,c,cg,c0,H)
alpha0 = 0;
H0 = 0;
errorMsg = '';

deg2rad=pi/180;

arg=(c0/c)*sin(alpha*deg2rad);
%assert(arg<1,'Error: Violation of assumptions for Snells Law')
if not(arg<1)
    errorMsg = 'Error: Violation of assumptions for Snells Law';
    return;
end

alpha0=(asin(arg))/deg2rad;

ksf=sqrt(c0/(2*cg)); %shoaling coefficient

alphaCos = cos(alpha0*deg2rad) / cos(alpha*deg2rad);
if alphaCos < 0
    errorMsg = 'Error: Alpha1 data out of range';
    return;
end
krf=sqrt(alphaCos); %refraction coefficient

H0=H/(ksf*krf);
end
