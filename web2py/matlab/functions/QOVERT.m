% Determine wave overtopping rate

%   INPUT
%   H0: deepwater wave height
%   free: freeboard above still water level (height of structure minus
%   water depth at toe of structure)
%   R: runup on the structure
%   Qstar0: emperical coefficient
%   alpha: empirical coeffieint
%   theta: angle of structure slope with horizontal
%   U: onshore windspeed
%   g: gravitational acceleration

%   OUTPUT
%   qovertop: overtopping rate per unit width of structure

function [qovertop]=QOVERT(H0,free,R,Qstar0,alpha,theta,U,g)

prod=Qstar0*alpha*free*R*theta;

if prod<=0 || R<=free
    qovertop=0;
else
    
Cw=1+(U^2/1800)*((free/R)+0.1)*sin(theta);

arg1=(R+free)/(R-free);
qovertop=Cw*sqrt(g*Qstar0*(H0^3))*(arg1^(-0.1085/alpha));

end