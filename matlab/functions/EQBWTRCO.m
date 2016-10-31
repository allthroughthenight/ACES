% Determines wave transmission and reflection coefficients for the
% equivalent rectangular breakwater found in function EQBWLE

%   INPUT
%   pref: porosity of reference material (0.435)
%   k: wavenumber
%   dref: one half mean diameter of reference material
%   aI: wave amplitude of equivalent incident wave
%   d: water depth
%   nu: kinematic viscosity (0.0000141)
%   lequ: equivalent length of rectangular breakwater from EQBWLE
%   g: acceleration of gravity

%   OUTPUT
%   Ti: transmission coefficient
%   Ri: reflection coefficient

%   OTHER
%   Rc: critical Reynolds number
%   F: friction factor
%   U: complex horizontal velocity component
%   Rd: particle Reynolds number
%   betar: hydrodynamic characterisitc of reference material

function [Ti,Ri]=EQBWTRCO(pref,k,dref,aI,d,nu,lequ,g)

    Rc=170.0;

    % used in solving the transmission and reflection coefficients
    nors=0.45;
    ss=(pref/0.45)^2;
    kon=k*pref;
       
    betar=2.7*((1-pref)/(pref^3*dref));

    % guess a lambda (intermediate value) and a value for F...iterate until the
    % difference is less than 2%
    diff=100;
    lambda=1.0;
    F=0.0;
    while diff>0.02
        Fnew=F;
        U=aI*sqrt(g/d)/(1+lambda);
        Rd=U*dref/nu;
        F=pref/(k*lequ);
        F=F*(sqrt(1+(1+Rc/Rd)*(16*betar*aI*lequ/(3*pi*d)))-1);
        lambda=k*lequ*F/(2*pref); %calculate new lambda
        diff=abs(Fnew-F)/F;
    end
    
    % used in solving the transmission and reflection coefficients
    fos=F/ss;

    %call function MADSN1 which solves for Ti and Ri
    [Ti,Ri]=MADSN1(nors,fos,kon*lequ);
end

        