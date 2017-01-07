% Determine wave and setup statistics

function [Hmax,Hrms,Hmean,Hsig,H10,H02,etan,z]=GODA2(p,delxx,Hop,sump,dL,etam1,d,zm1)

cump=0;
Hsig=0;
Hrms=0;
Hmean=0;
H10=0;
H02=0;
x=0;
Hmax=0;

for i=1:150
    x=x+delxx;
    cump=cump+p(i)/sump;
    if cump>0.666
        Hsig=Hsig+x*Hop*p(i)/sump*3;
    end
    if cump>0.90
        H10=H10+x*Hop*p(i)/sump*10;
    end
    if cump>0.98
        H02=H02+x*Hop*p(i)/sump*50;
    end
    if cump>0.996
        Hmax=Hmax+x*Hop*p(i)/sump*250;
    end
    
    Hmean=Hmean+x*Hop*p(i)/sump;
    Hrms=Hrms+x^2*p(i)/sump;
end
Hrms=sqrt(Hrms)*Hop;

z=1/8*Hrms^2*(0.5+4*pi*dL/(sinh(4*pi*dL)));
etan=etam1-(1/d*(z-zm1))*0.7;
if abs(etan)<10^(-20)
    etan=0.000001;
end

    