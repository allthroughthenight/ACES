% Solves for reflection coefficient, non-dimensional runup amplitude, and
% friction slope for rough impermeable slopes

%   INPUT
%   lsub: water depth x cotangent of structure slope
%   phi: friction angle [rads]
%   ko: wavenumber

%   OUTPUT
%   R: reflection coefficient
%   Ru: nondimensional runup amplitude
%   sfc: friction slope constant

function [R,Ru,fsc]=MADSN2(lsub,phi,k)

    L=(2*pi)/k;
    lsol=lsub/L;

    fb=tan(2*phi);
    c1=2*k*lsub;
    c2=sqrt(complex(1.0,-fb));

    arg=complex(c1,0)*c2;

    J0=besselj(0.0,arg);
    J1=besselj(1.0,arg);

    c3=(complex(0,1)/c2)*J1;

    denom=J0+c3;

    psi=complex(c1/2,0)*c2;

    req=((J0-c3)/denom)*exp(complex(0,c1));
    R=abs(req);

    rueq=exp(complex(0,c1/2))/denom;
    Ru=abs(rueq);

    if lsol<0.05
        fsc=0.84242;
    else
        fun=@(y) abs((besselj(1,2*psi.*sqrt(y))./(psi.*sqrt(y))).^3);      
        topint=quad(fun,0,1);

        fun=@(y) abs(y.*(besselj(1,2*psi.*sqrt(y))./(psi.*sqrt(y))).^2);
        botint=quad(fun,0,1);
        
        fsc=(4/(3*pi))*(topint/botint);
    end
end