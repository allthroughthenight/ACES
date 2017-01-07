function [dL]=GODA5(dLo)

diff=100;
Ld=1.0/dLo;
Lod=Ld;

while diff>0.0005
    arg=2.0*pi/Ld;
    Ldnew=Lod*tanh(arg);
    diff=abs(Ldnew-Ld);
    Ld=(Ldnew+Ld)/2.0;
end
dL=1.0/Ldnew;


    