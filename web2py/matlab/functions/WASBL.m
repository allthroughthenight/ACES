% Solution in the constant stress region

%   INPUT
%   delt: air-sea temperature difference
%   uobs: observed wind speed
%   zobs: elevation of wind observation

%   OUTPUT
%   sbl10m: equivalent neutral windspeed at 10 m elevation 

function [sbl10m]=WASBL(uobs,delt,zobs)

diff1=100;
diff2=100;

L=delt;
z=1000; %10 m in cm
k=0.4; %von Karman constant

ustar=uobs*(z/zobs)^(-1/7);
cd=0.001*(0.75+0.067*0.01*uobs);
ustar=sqrt(cd)*ustar;
if delt>0
    ustar=0.8*ustar;
else
    ustar=1.2*ustar;
end

c1=0.1525;
c2=0.019/980;
c3=-0.00371;

while diff1>0.1
    z0=(c1/ustar)+(c2*ustar^2)+c3;
    lnzzo=log(zobs/z0);
    if abs(delt)<1
        psi=0;
    else
        while diff2>1.0
            [psi]=WAPSI((zobs/L),-1.5);
            Lnew=1.79*(ustar^2/delt)*(lnzzo-psi);
            diff2=abs(Lnew-L);
            if diff2>1.0
                L=Lnew;
            end
        end
    end
    ustarn=(uobs*k)/(lnzzo-psi);
    diff1=abs(ustar-ustarn);
    if diff1>0.1
        ustar=(ustar+ustarn)/2;
    end
end
sbl10m=(ustar/k)*log(z/z0);

       
%  for iter1=1:51
%      z0=(c1/ustar)+(c2*ustar^2)+c3
%      lnzrat=log(zobs/z0);
%      if abs(delt)<1
%          psi=0;
%      else
%          for iter2=1:51
%              psi=WAPSI((zobs/L),-1.5);
%              ln=ustar*ustar*1.79*(lnzrat-psi)/delt;
%              if abs(L-ln)<1.0
%                  break
%              end
%              L=ln;
%          end
%      end
%      ustarn=uobs*k/(lnzrat-psi);
%      if abs(ustar-ustarn)<0.1
%          break
%      end
%      ustar=(ustar+ustarn)*0.5;
%  end
%  sbl10m=2.5*ustar*log(1000/z0);
% end
%      
    

