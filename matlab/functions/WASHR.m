%   INPUT
%   arg: ratio of observed wind elevation over stability length

function [phiu]=WASHR(arg)

Ri=arg;
Rinew=arg*(1-18*Ri)^(1/4);
diff=abs(Rinew-Ri);

while diff>0.001
    Ri=Rinew;
    Rinew=arg*(1-18*Ri)^(1/4);
    diff=abs(Rinew-Ri); 
end

phiu=1/(1-18*Rinew)^(1/4);