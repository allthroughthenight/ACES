%Solution of PBL equations for 10 m elevation wind velocity (with known
%geostrophic wind velocity)

%   INPUT
%   vg: geostrophic windspeed
%   delt: air-sea temperature difference
%   f: Coriolis parameter
%   H: horizontal temperature gradient
%   phi: angle between vg and H

%   OUTPUT
%   gpbl: equivalent neutral windspped at 10 m elevation


function [gpbl]=WAPBL(vg,delt,f,H,phi)

phi=phi*(pi/180);
z=1000;
diff1=100;
diff2=100;
diff3=100;

if abs(delt)>15
    delt=15*(abs(delt)/delt);
end

k=0.4;
L=delt;

as0=0.8;
bs0=3.5;
aml=7-as0;

ab=k*(H/3)*cos(phi);
bb=k*(H/3)*sin(phi);
a=as0+ab;
b=bs0+bb;

ustar=0.15*vg/abs(b);

c1=0.1525;
c2=0.0144/980;
c3=-0.00317;

while diff3>0.1
    while diff1>0.1
        z0=(c1/ustar)+(c2*ustar^2)+c3;
        theta=asin(b*ustar/(vg*k));
        ustarn=k*vg*cos(theta)/(log(ustar/(f*z0))-a);
        diff1=abs(ustarn-ustar);
        ustar=(ustar+ustarn)/2;

        if ustar<0
            ustar=0.1;
            z0=(c1/ustar)+(c2*ustar^2)+c3;
            gpbl=(ustar/k)*log(z/z0);
            return
        end

        if abs(b*ustar)>k*vg
            ustar=k*vg/abs(b)-1.0^(-10);
        end
    end

    ustar=ustarn;
    z0=(c1/ustar)+(c2*ustar^2)+c3;

    if abs(delt)<1
        gpbl=(ustar/k)*log(z/z0);
        return
    end

    while diff2>1.0
        lnzz0=log(1005/z0);
        [psi]=WAPSI((1005/L),-7);
        Ln=1.79*(ustar^2/delt)*(lnzz0-psi);
        diff2=abs(Ln-L);
        L=Ln;
    end
    
    mu=(k*ustar)/(f*L);
    if mu<=0
        as=as0+aml*(1-exp(0.015*mu));
        bs=bs0-(bs0-0.23)*(1-exp(0.03*mu));
    else
        as=as0-0.96*sqrt(mu)+log(sqrt(mu+1));
        bs=bs0+0.7*sqrt(mu);
    end
    an=max((as+ab),-15);
    bn=min((bs+bb),15);
    
    diff3=abs(a-an);
    a=an;
    b=bn;
    if abs(b*ustar)>k*vg
        ustar=k*vg/abs(b)-1.0^(-10);
    end
    diff1=100;
    diff2=100;
end

z0=(c1/ustar)+(c2*ustar^2)+c3;
gpbl=(ustar/k)*log(z/z0);







