% Perform wind adjustments

%   INPUT
%   uobs: observed windspeed
%   zobs: elevation of wind observation
%   delt: air-sea temperature difference
%   F: fetch length
%   tobs: duration of wind observation
%   tfin: duration of final desired windspeed
%   latt: Latitude of wind observation
%   obstyp: Type of wind observation
%           1 = overwater (shipboard)
%           2 = overwater (not shipboard)
%           3 = at shore (off to onshore)
%           4 = at shore (on to offshore)
%           5 = over land
%           6 = geostrophic wind

%   OUTPUT
%   ue: equivalent neutral windspeed at 10 m elevation and at desired final
%       duration
%   error: message indication non-convergence

function [ue]=WADJ(uobs,zobs,delt,F,tobs,tfin,latt,obstyp)

mtocm=100;

if obstyp==1
    %Ship-based wind observations over water
    u=1.864*uobs^(7/9);
    [u10m]=WASBL(u*mtocm,delt,zobs*mtocm);
    u10m=u10m/mtocm;
elseif obstyp==2 || obstyp==3
    %Wind observation over water (not ship-based) or at the shoreline
    %(wind direction from offshore to onshore)
    [u10m]=WASBL(uobs*mtocm,delt,zobs*mtocm);
    u10m=u10m/mtocm;
elseif obstyp==4 || obstyp==5
    %Winds over land or at the shoreline (wind direction from onshore
    %to offshore)
    [u]=WAGEOS(uobs*mtocm,zobs*mtocm,30);         
    omega=7.2921150*10^-5; %Earth's angular velocity (2pi/86164.09)    
    f=2*omega*sin(latt); %Coriolis force
    [u10m]=WAPBL(u,delt,f,0,0);
    u10m=u10m/mtocm;
elseif obstyp==6
    %Geostrophic winds
    omega=(2*pi)/(24*3600); %Earth's angular velocity       
    f=2*omega*sin(latt); %Coriolis force
    [u10m]=WAPBL(uobs*mtocm,delt,f,0,0);  
    u10m=u10m/mtocm;
end
ue=u10m;

if F<16000
    ue=0.9*ue;
end

if tobs<=1
    assert(tobs>1,'Error: Observed windspeed duration must be > 1 s.')
elseif tobs<3600
    eqshrt=1.277+0.296*tanh(0.9*log10(45/tobs));
    u3600=ue/eqshrt;
elseif tobs==3600
    u3600=ue;
elseif tobs>3600
    eqlong=-0.15*log10(tobs)+1.5334;
    u3600=ue/eqlong;
end

if tfin<=1
    assert(tfind>1,'Error: Final windspeed duration must be > 1 s.')
elseif tfin<3600
    eqshrt=1.277+0.296*tanh(0.9*log10(45/tfin));
    ue=u3600*eqshrt;
elseif tfin==3600
    ue=u3600;
elseif tfin>3600
    eqlong=-0.15*log10(tfin)+1.5334;
    ue=u3600*eqlong;
end