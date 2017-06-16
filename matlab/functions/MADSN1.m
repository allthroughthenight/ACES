% Determine transmission and reflection coefficients for crib-style
% breakwaters

%   INPUT
%   nors: N/sqrt(S) = 0.45
%   fos: F/S
%   nkol: wavenumber x porosity of reference material x equivalent length

%   OUTPUT
%   Ti: transmission coefficient
%   Ri: reflection coefficeint

%   OTHER:
%   k: complex wave number

function [Ti,Ri]=MADSN1(nors,fos,nkol)
    
    % intermediate values
    eps=complex(nors,0)/sqrt(complex(1,-fos));
    theta=complex(0,1)*complex(nkol,0)/eps;

    c1=(complex(1,0)+eps)^2;
    c2=(complex(1,0)-eps)^2;
    c3=complex(1,0)-eps^2;
    denom=c1*exp(theta)-c2*exp(-theta);
 
    % transmission coefficient
    teq=complex(4,0)*eps/denom;
    Ti=abs(teq);

    %reflection coefficient
    req=(c3*(exp(theta)-exp(-theta)))/denom;
    Ri=abs(req);
    
end