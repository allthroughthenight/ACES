% Input required in centimeters

function [Ksout,Krout,Hmaxout,Hrmsout,Hmeanout,Hsigout,H10out,H02out,SBout,HoLo,dLoout,dHoout,xsave,theta2dout,etaout,Ht1,cdf,Ht2,cdf2]=GODA(Ho,dloc,Ts,S,direc,g)
deg2rad=pi/180;
Csave=0;
itest=0;
ym1=1;
ym2=0;
etam1=0;
etam2=0;
zm1=0;
jpn=0;
%
% Hx1=1;
% cdf1=1;
% Hx2=1;
% cdf2=1;

sbn=[3.2831,2.3158,1.3832,0.4599,-0.4599,-1.3832,-2.3158,-3.2831];
delp=[0.0014,0.0214,0.1359,0.3413,0.3413,0.1359,0.0214,0.0014];

% Calcuate deepwater wavelength
Lo=(g/(2*pi))*Ts^2;
xsave=Lo;
if (20*Ho)>Lo
    xsave=20*Ho;
end
d=xsave;

% Calculate deepwater wave steepness
HoLo=Ho/Lo;

% Find effective slope of beach (i.e., beach slope in the approach
% direction of propagation) for deepwater. This effective slope will change
% as the principal approach direction chenged due to Snell's Law
% refraction.
direcr=direc*deg2rad;
Seff=S/cos(direcr);

% Main computational portion of program. Calculations proceed as follows:
%   -Still water depth in deepwater divided into 100 increments.
%   -First depth increment acted upon.
%   -A first estimate for setup is linearly extrapolated from the setup
%       gradient from the previous step. This gradient is zero in
%       deepwater.
%   -In deepwater where d/Lo > 0.5, the calculation goes back to the first
%       step for the next depth increment. Once d/Lo =< 0.5, the remainder
%       of the calculations performed where the increment is reduced to
%       1/500th of the original still water depth.
%   -The effective refraction coefficient from subroutine GODA4 is
%       calculated.
%   -Probabilites at eight levels of surf beat are calculated. For each
%       level of surf beat, the still water depth, the first setup
%       estimated, and surf beat are added together.
%   -Wave characterisitcs are computed with the first estimate of setup. A
%       new value of setup is calculated directly from the radiation stress
%       equation.
%   -Program then checks to see if the 2nd value of setup is approximately
%       equal to the first estimated. If not, the program recalculates the
%       surf beat level probabilities at the new value of setup, and redoes
%       the calculation of setup from the radiation stress equation. If so,
%       the program calculates the total probabilities of wave height
%       occurrence. It will output the results if the water depth at a
%       point is approximately the same as a water depth of interest.
%
%   This is the beginning of the depth "loop" (i.e., beginning of the depth
%   incrementation along profile).

N=0;
M=0;
while d>dloc
    if M==1
        deld=xsave/100;
    elseif M==2
        deld=xsave/500;
    end
    
    if N==0
        d=xsave;
    else
        d=d-deld;
    end
    
    y=Seff*(xsave-d);
    
    %Find still water depth at location y
    dswl=d;
    dHo=dswl/Ho;
    
    N=N+1;
    
    diffy=ym1-ym2;
    if diffy==0
        diffy=0.125;
        deld=diffy/Seff;
    end
    
    eta=etam1+(y-ym1)*(etam1-etam2)/diffy;
    dLo=d/Lo;
    Cso=Lo/Ts;
    
    [dL]=GODA5(dLo);
    
    %Final coefficient of shoaling by method of Shuto
    [Ks,Csave,itest]=GODA3(Ts,Ho,d,g,Csave,itest);
    
    if (d/Lo)>0.5 && N~=1 && d>(dloc+30)
        ym1=y;
        M=1;
        L=d/dL;
        Cs=L/Ts;
        argum=Cs/Cso*sin(direcr);
        theta2=asin(argum);
        Seff=S/cos(theta2);
    else
        diff2=100;
        Hop=Ho;
        M=2;
        d=dswl+eta;
        while diff2>=0.07
            [Kreff]=GODA4(direc,Ts,d,Ho,g);
            sbrms=0.01*Hop/sqrt(Hop/Lo*(1+d/Hop));
            A2=(1.416/Ks)^2;
            
            p=zeros(1,150);
            di=zeros(1,8);
            x1=zeros(1,8);
            x2=zeros(1,8);
            q=zeros(1,150);
            
            for j=1:8
                di(j)=sbrms*sbn(j)+dswl+eta;
                arg=-1.5*pi*di(j)/Lo*(1+15*((1/Seff)^(4/3)));
                arg=min(arg,100);
                arg=max(arg,-100);
                
                x1(j)=0.18*(Lo/Hop)*(1-exp(arg))*Kreff;
                x1(j)=min(x1(j),2.8);
                
                if x1(j)>0
                    x=0;
                    x2(j)=(2/3)*x1(j);
                    delxx=(x1(1)/150);
                    arg2=-A2*(x1(j)^2);
                    arg2=min(arg2,100);
                    arg2=max(arg2,-100);
                    
                    for i=1:150
                        x=x+delxx;
                        arg=-A2*(x^2);
                        arg=max(arg,-100);
                        arg=min(arg,100);
                        
                        if x>x1(j)
                            q(i)=0;
                        elseif x<=x2(j)
                            q(i)=2*A2*x*exp(arg);
                        else
                            q(i)=2*A2*x*exp(arg)-(x-x2(j))/(x1(j)-x2(j))*2*A2*x1(j)*exp(arg2);
                        end
                    end
                    sumq=sum(q);
                    
                    fact=delp(j)/sumq;
                    for i=1:150
                        p(i)=p(i)+q(i)*fact;
                    end
                end
            end
            sump=sum(p);
            
            [Hmax,Hrms,Hmean,Hsig,H10,H02,etan,z]=GODA2(p,delxx,Ho,sump,dL,etam1,d,zm1);
            diff2=abs((etan-eta)/etan);
            if diff2>0.07
                eta=etan;
            end
        end
        
        [dL]=GODA5(dLo);
        L=d/dL;
        Cs=L/Ts;
        argum=Cs/Cso*sin(direcr);
        theta2=asin(argum);
        theta2d=theta2/deg2rad;
        Seff=S/cos(theta2);
        
        if N==1
            Ksout(1)=Ks;
            Hmaxout(1)=Hmax;
            Hrmsout(1)=Hrms;
            Hmeanout(1)=Hmean;
            Hsigout(1)=Hsig;
            H10out(1)=H10;
            H02out(1)=H02;
            dLout(1)=dL;
            SBout(1)=sbrms;
            dLoout(1)=dLo;
            dHoout(1)=dHo;
            theta2dout(1)=theta2d;
            etaout(1)=eta;
        else
            Ksout(2)=Ks;
            Krout(1)=Kreff;
            Hmaxout(2)=Hmax;
            Hrmsout(2)=Hrms;
            Hmeanout(2)=Hmean;
            Hsigout(2)=Hsig;
            H10out(2)=H10;
            H02out(2)=H02;
            dLout(2)=dL;
            SBout(2)=sbrms;
            dLoout(2)=dLo;
            dHoout(2)=dHo;
            theta2dout(2)=theta2d;
            etaout(2)=eta;
        end
        
        x=0;
        if Hsig<20
            delh=1.0;
        elseif Hsig<50
            delh=2;
        else
            delh=10;
        end
        
        ijk=0;
        ikj=0;
        H1=0;
        cump1=0;
        if N<=1
            Kreff=1.0;
        end
        jpn=jpn+1;
        
        for i=1:150
            x=x+delxx;
            H2=x*Hop;
            cump2=cump1+p(i)/sump;
            if cump2>0.9999
                cump1=cump2;
                H1=H2;
            else
                i1=H1/delh;
                i2=H2/delh;
                is=i2-i1;
                if is==0
                    cump1=cump2;
                    H1=H2;
                elseif is>0
                    if is<1
                        is=1;
                    end
                    for it=1:is
                        Ht=delh*(i1+it);
                        cump=cump1+(Ht-H1)/(H2-H1)*(cump2-cump1);
                        if cump>0.999
                            cump1=cump2;
                            H1=H2;
                        else
                            if jpn==1
                                ijk=ijk+1;
                                Ht1(ijk)=Ht;
                                cdf(ijk)=cump;
                            else
                                ikj=ikj+1;
                                Ht2(ikj)=Ht;
                                cdf2(ikj)=cump;
                            end
                        end
                    end
                    cump1=cump2;
                    H1=H2;
                end
            end
        end
        zm1=z;
        etam2=etam1;
        etam1=etan;
        ym2=ym1;
        ym1=y;
    end
end
