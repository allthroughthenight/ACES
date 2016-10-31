function [RIi,Ru,sfc]=MADSN2_test(lsub,phi,ko)

L=(2*pi)/ko;
lsol=lsub/L;
fb=tan(2*phi);

c1=12.566371*lsol;

c2=sqrt(complex(1,-fb));
c3=complex(c1,0)*c2;

J0=besselj(0,c3);
J1=besselj(1,c3);

c4=J1*(complex(0,1)/c2);

denom=J0+c4;
psi=complex(2*pi*lsol,0)*c2;

req=(J0-c4)*exp(complex(0,c1))/denom;
RIi=abs(req);

rueq=exp(complex(0,c1/2))/denom;
Ru=abs(rueq);

if lsol<0.5
    sfc=0.84242;
else
    arg=2*psi*sqrt(y);
    J1top=besselj(1,arg);
    term=J1top/(psi*sqrt(y));
    top=term^3;
    %topint=int(top,y,0,1);
    bottom=y*(term^2);
    %botint=int(bottom,y,0,1);
    sfc=(4/(3*pi))*(top/bottom);
end

end