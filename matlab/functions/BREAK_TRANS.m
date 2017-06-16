% Computes sediment transport rates using breaking wave conditions
% English units only

%   INPUT
%   Hb: breaking wave height [ft]
%   alpha: wave crest angle with the shoreline [deg]
%   K: dimensionless coefficient
%   rho: density of water [slugs/ft^3]
%   rhos: density of the sediment [slugs/ft^3 - 5.14 in FORTRAN code]

%   OUTPUT
%   Q: sediment transport rate [ft^3/s]

%   OTHER:
%   deg2rad: factor to convert deg to rads
%   Pls: longshore energy flux factor

function [Q]=BREAK_TRANS(Hb,alpha,K,rho,g,rhos)

deg2rad=pi/180;
alphar=alpha*deg2rad;

Pls=0.07071*rho*(g^(3/2))*(Hb^(5/2))*sin(2*alphar);


Q=(Pls*K)/((rhos-rho)*g*0.6);

end
    

