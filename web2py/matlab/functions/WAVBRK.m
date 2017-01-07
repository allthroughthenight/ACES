function [Hb,db]=WAVBRK(H0,L0,T,m)

a=1.36*(1-exp(-19*m));
b=1/(0.64*(1+exp(-19.5*m)));
    
Hb=H0*0.575*(m^0.031)*((H0/L0)^(-0.254));
gamma=b-a*Hb/(T^2);
db=Hb/gamma;

end
    

