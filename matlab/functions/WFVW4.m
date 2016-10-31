% Input value 'p' includes hydrostatic pressure
% To define wave pressure 'wp' remove hydrostatic pressue from values of
% 'p' below SWL. Pressure is the same above SWL for both values (0).
% Hydrostatic pressue is waves & hydrostatic pressure minus wave pressure.
% Hydrostatic pressue increases from 0 at SWL to rho*g*d at the bottom.

function [hp,wp]=WFVW4(N,y,p,ww)

for i=1:(N+1)
    if y(i)<0
        wp(i,1)=p(i)+ww*y(i);
        hp(i,1)=p(i)-wp(i,1);
    else
        wp(i,1)=p(i);
        hp(i,1)=0;
    end
end

