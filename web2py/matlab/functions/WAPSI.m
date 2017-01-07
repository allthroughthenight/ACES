%   INPUT
%   arg: ratio of observed wind elevation over stability length
%   c: multiple coefficient for arg (if arg >0)

%   OUTPUT
%   psi: universal similarity function 

function [psi]=WAPSI(arg,c)

if arg>0
    psi=c*arg;
else
    [phi]=WASHR(arg);
    psi=1-phi-3*log(phi)+2*log((1+phi)/2)+2*atan(phi)-(pi/2)+log((1+phi^2)/2);
end