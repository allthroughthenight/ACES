% Determine runup on a rough slope

%   INPUT
%   H: incident wave height at toe of structure
%   xi: surf parameter
%   a: dimensionless coefficient
%   b: dimensionless coefficient

%   OUTPUT
%   runupr: runup on a rough slope

function [runupr]=RUNUPR(H,xi,a,b)

runupr=(H*a*xi)/(1+b*xi);

end