function [Hnon,L,Hod,unon]=FWTPRE(g,T,H,d,u)
    
Hnon=H/(g*T^2);
L=((g*T^2)/(2*pi))*sqrt(tanh(1.22718*d/T^2));

if d/L>1.5
    Hod=0.0;
else
    Hod=H/d;
end

unon=u/sqrt(g*H);
