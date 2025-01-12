% Error check for wave steepness

%   INPUT
%   H: wave height
%   d: water depth
%   L: wave length

%   OUTPUT
%   steep: steepness of supplied conditions
%   maxstp: maximum wave steepness

function [steep,maxstp]=ERRSTP(H,d,L)

    steep=H/L;
    k=(2*pi)/L;
    maxstp=0.142*tanh(k*d);

end
    

