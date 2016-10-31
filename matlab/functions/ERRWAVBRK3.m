% Error check for wave breaking where a finite slope is known (m>0)

%   INPUT
%   Ho: deepwater wave height
%   m: nearshore slope
%   Lo: deepwater wave length

%   OUTPUT
%   Hb: breaking wave height
%   db: breaker depth

function [Hb,db]=ERRWAVBRK3(Ho,Lo,T,m)

a=1.36*(1-exp(-19*m));
b=1/(0.64*(1+exp(-19.5*m)));
    
Hb=Ho*0.575*(m^0.031)*((Ho/Lo)^(-0.254));
gamma=b-a*Hb/(T^2);
db=Hb/gamma;

end
    