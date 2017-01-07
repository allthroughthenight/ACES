% Calculates wave amplification factor, phase angle, and amplified wave
% height for the combined diffraction and reflection of monochromatic
% incident waves (small amplitude wave theory) approaching (from infinitiy)
% a vertical wedge of arbitrary wedge angle

%   INPUT
%   x: x-coordinate [m] (Cartesian coord system)
%   y: y-coordinate [m] (Cartesian coord system)
%   Hi: incident wave height [m]
%   waveA: approach angle of incident wave [deg] (measured counter-clockwise
%          from x-axis)
%   wedgeA: internal angle of wedge [deg] (measured clockwise from x-axis)
%   L: wavelength [m]

%   OUTPUT
%   H: modified wave height at (x,y) [m]
%   phi: modulus of velocity potential at (x,y)
%   beta: phase angle of velocity potential at (x,y) [rad]
%   error: triggers error

function [phi,beta,H,error]=DRWEDG(x,y,Hi,waveA,wedgeA,L)

error=0;
twopi=2*pi;
deg2rad=pi/180;

r=sqrt(x^2+y^2); %convert to polar coordinates

if x==0 && y==0
    theta=0;
else
    theta=atan2(y,x);
    if theta<0
        theta=twopi+theta;
    end
end

%check to see if (x,y) is located within the structure
radwed=wedgeA*deg2rad;
totang=theta+radwed;
if totang>twopi
    error=1;
    phi=0;
    beta=0;
    H=0;
    return
end

%solve for velocity potential function at (r,theta)
kr=(2*pi/L)*r;
nu=(360-wedgeA)/180;

[J0]=besselj(0,kr);

n=1;
order(n)=n/nu;
Jnu(n)=besselj(order,kr);
tolr=10^-8;
count=0;

while count<9
    n=n+1;
    order(n)=n/nu;
    Jnu(n)=besselj(order(n),kr);
    if Jnu(n)<tolr
        count=count+1;
    else
        count=0;
    end
end

wa=waveA*deg2rad;
    
i=sqrt(-1);
for j=1:length(Jnu)
    F(j)=(exp(i*order(j)*pi/2))*Jnu(j)*cos(order(j)*wa)*cos(order(j)*theta);
end
F=sum(F);
Fpot=(2/nu)*(J0+2*F);

%determine modulus
fr=real(Fpot);
fi=imag(Fpot);
phi=sqrt(fr^2+fi^2); %modulus
if wa<tolr
    phi=phi/2;
end

%determine phase angle
if phi<tolr
    beta=0; %phase difference
else
    beta=atan2(fi,fr);
end

H=Hi*phi; %modified wave height
end
