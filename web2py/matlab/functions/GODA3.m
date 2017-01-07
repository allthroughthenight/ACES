% Subroutine to find the shoaling coefficient based on the methof of Shuto

function [Ks,Csave,itest]=GODA3(Ts,Hdeep,d,g,Csave,itest)
del=100;

Lo=(g/(2*pi))*Ts^2;
dLo=d/Lo;
[dL]=GODA5(dLo);
n=0.5*(1+4*pi*dL/sinh(4*pi*dL));
L=d/dL;
C=L/Ts;
Co=(g/(2*pi))*Ts;
Ks=sqrt(0.5/n*Co/C);
H=Hdeep*Ks;
F=980*H*Ts^2/(d^2);

if itest==1
    Ks=Csave/(d^(2/7)*H);
    H=Hdeep*Ks;
    F=980*H*Ts^2/(d^2);
        if F<50
            itest=1;
            return
        else
            itest=2;
            Csave=H*d^(5/2)*(sqrt(980*H*Ts^2/(d^2))-2*(sqrt(3)));
            return
        end
elseif itest==2
    while del>0.05
        Hn=Csave/(d^(5/2)*(sqrt(980*H*Ts^2/(d^2))-2*sqrt(3)));
        del=abs((Hn-H)/Hn);
        if del<0.05
            break
        end
        H=Hn;
    end
    Ks=Hn/Hdeep;
elseif itest==0
    if F<30
        itest=0;
        return
    else
        itest=1;
        Csave=H*d^(2/7);
        return
    end
end
    
    










    