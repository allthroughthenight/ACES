% Error check for monochromatic wave breaking on simple plane beach

%   INPUT
%   d: water depth
%   kappa: breaking index

%   OUTPUT
%   Hb: breaking wave height

function [Hb]=ERRWAVBRK1(d,kappa)
Hb=kappa*d;
end