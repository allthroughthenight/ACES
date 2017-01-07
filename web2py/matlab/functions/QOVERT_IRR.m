% Determine wave overtopping rate for irregular waves

%   INPUT
%   H0: deepwater wave height
%   free: freeboard above still water level (height of structure minus
%   water depth at toe of structure)
%   R: runup on the structure
%   Qstar0: empirical coefficient
%   alpha: empirical coeffieint
%   theta: angle of structure slope with horizontal
%   U: onshore windspeed
%   g: gravitational acceleration

%   OUTPUT
%   qovertop: overtopping rate per unit width of structure

function [qovertop]=QOVERT_IRR(H0,free,R,Qstar0,alpha,theta,U,g)

if R<free
    isum=999;
    total=1000.0;
else
    isum=199;
    total=200.0;
end

for i=1:isum
    p=(1/total)*i;
    Ri=sqrt(log(1/p)/2)*R;
    [Q(i)]=QOVERT(H0,free,Ri,Qstar0,alpha,theta,U,g);
end
qovertop=sum(Q)/isum;
