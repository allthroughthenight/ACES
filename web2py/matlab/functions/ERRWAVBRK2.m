% Error check for  wave breaking in the prescence of a structure

%   INPUT
%   T: water period
%   m: nearshore slope
%   ds: water depth at structure

%   OUTPUT
%   Hb: breaking wave height

function [Hbs]=ERRWAVBRK2(T,m,ds)
        a=1.36*(1-exp(-19*m));
        b=1/(0.64*(1+exp(-19.5*m)));
        term=(ds/T^2);
        P=a+(1+9.25*m^2*b-4*m*b)/term;
    
        term1=ds/(m*a*(18.5*m-8));
        term2=P^2-(((4*m*b*a)/term)*(9.25*m-4));
        Hbs=term1*(P-sqrt(term2));
end