% Computes sediment transport rates using deepwater wave conditions
% English units only

%   INPUT
%   Hb: deepwater wave height [ft]
%   alpha: deepwater angle of wave crest [deg]
%   K: dimensionless coefficient
%   rho: density of water [slugs/ft^3]
%   rhos: density of the sediment [slugs/ft^3 - 5.14 in FORTRAN code]

%   OUTPUT
%   Q: sediment transport rate [ft^3/s]

%   OTHER:
%   deg2rad: factor to convert deg to rads
%   Pls: longshore energy flux factor

function [Q]=DEEP_TRANS(Ho,alpha,K,rho,g,rhos)

deg2rad=pi/180;
alphar=alpha*deg2rad;

Pls=0.04031*rho*(g^(3/2))*(Ho^(5/2))*((cos(alphar))^(1/4))*sin(2*alphar);

Q=(Pls*K)/((rhos-rho)*g*0.6);

end
    

