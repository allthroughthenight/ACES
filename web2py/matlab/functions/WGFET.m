% Determine "representative" fetch and wave direction

%   INPUT
%   ang1: angle of first radial fetch
%   dang: angle increment between radials
%   wdir: wind direction approach
%   x: radial fetch length at given angles

%   OUTPUT
%   F: representative fetch length
%   phi: angle between wind and wave directions
%   theta: angle of wave direction (relative to North)

function [F,phi,theta]=WGFET(ang1,dang,wdir,x)

%Interpolate radial fetch lengths around the compass
% Values are interpolated at whole degress so dang >=1

nang=length(x); %length of radial fetches
angn=ang1+(nang-1)*dang;
angnm=angn-dang;
nangm=nang-1;
angle=ang1;
i=1;

for j=1:nang
    fa(j)=angle+(j-1)*dang;
end

xx=zeros(360);
xfin=zeros(360);

for deg=round(ang1):1:round(angn);
    ideg=floor(deg);
    
    if ideg<1
        ideg=ideg+360;
    end
    if deg>360
        ideg=ideg-360;
    end
    
    if deg<=ang1
        xx(ideg)=x(1);
    elseif deg>=angn
        xx(ideg)=x(nang);
    else
        if deg>fa(i+1)
            angle=min(angnm,(angle+dang));
            i=min(nangm,(i+1));
        end           
        tmp=(x(i+1)-x(i))/dang;
        xx(ideg)=x(i)+tmp*(deg-angle);
    end
end

for i=1:360
    sumx=0;
    for j=1:15
        k=i-8+j;
        if k<1
            k=k+360;
        end
        if k>360
            k=k-360;
        end
        sumx=sumx+xx(k);
    end
    xfin(i)=sumx/15;
end

iwdir=round(wdir);
if iwdir<1
    iwdir=iwdir+360;
end
pmax=0;

for i=0:90
    k=iwdir+i;
    if k>360
        k=k-360;
    end
    km=iwdir-i;
    if km<1
        km=km+360;
    end
    
    if xfin(k)<xfin(km)
        k=km;
    end
    
    ftmp=max(xfin(k),0);
    phitmp=i;
    ptmp=ftmp^0.28*cos(phitmp*(pi/180))^0.44;
    if ptmp>pmax
        pmax=ptmp;
        phi=phitmp;
        theta=real(k);
        F=ftmp;
    end
end
    


    
    
