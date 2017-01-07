function [yc,yt,pc,pt,mc,mt]=WFVW2(N,d,L,H,x,ww,method)

dd=d/N;
yo=0;
k=2*pi/L;

yc=zeros(N+1,1);
yt=zeros(N+1,1);
pc=zeros(N+1,1);
pt=zeros(N+1,1);
mc=zeros(N+1,1);
mt=zeros(N+1,1);

%Miche-Rundgren Method
cosh1=cosh(k*d);
sinh1=sinh(k*d);
tanh1=tanh(k*d);

theta1=1+3/(4*sinh1^2)-1/(4*cosh1^2);
theta2=3/(4*sinh1^2)+1/(4*cosh1^2);

for i=1:(N+1)
    cosh2=cosh(k*(d+yo));
    cosh3=cosh(k*(2*d+yo));
    cosh4=cosh(k*yo);
    sinh2=sinh(k*(d+yo));
    sinh3=sinh(k*(2*d+yo));
    sinh4=sinh(k*yo);
    F4 = sinh4/sinh1/cosh1;
    F3 = sinh4/sinh1/sinh1;
    F7 = (1-1/(4.*cosh1*cosh1))*cosh3-2.*tanh1*sinh3+.75*(cosh4/(sinh1*sinh1)-2.*cosh2/cosh1);
    F8 = cosh3/(4.*cosh1*cosh1)-2.*tanh1*sinh3+.75*(cosh4/(sinh1*sinh1)-2.*cosh2/cosh1);
    j=N+2-i;
    
    %Sea surface elevation when crest and trough at wall (y0=0)
    %Miche-Rundgren valid for both methods
    if i==1
        ycb=yo+(H/2)*(1+x)*(sinh2/sinh1)+(pi*H/4)*(H/L)*(sinh2/sinh1)*(cosh2/sinh1)*((1+x)^2*theta1+(1-x)^2*theta2);
        ytb=yo-(H/2)*(1+x)*(sinh2/sinh1)+(pi*H/4)*(H/L)*(sinh2/sinh1)*(cosh2/sinh1)*((1+x)^2*theta1+(1-x)^2*theta2);
    end
    
    if method==0 %Miche-Rundgren (method=0)
        yc(j,1)=yo+(H/2)*(1+x)*(sinh2/sinh1)+(pi*H/4)*(H/L)*(sinh2/sinh1)*(cosh2/sinh1)*((1+x)^2*theta1+(1-x)^2*theta2);
        yt(j,1)=yo-(H/2)*(1+x)*(sinh2/sinh1)+(pi*H/4)*(H/L)*(sinh2/sinh1)*(cosh2/sinh1)*((1+x)^2*theta1+(1-x)^2*theta2);
        
        theta3=(1-1/(4*cosh1^2))*cosh3-2*tanh1*sinh3+(3/4)*(cosh4/sinh1^2-2*cosh2/cosh1);
        theta4=cosh3/(4*cosh1^2)-2*tanh1*sinh3+(3/4)*(cosh4/(sinh1^2)-2*cosh2/cosh1);
    
        pcr=-yo-(H/2)*(1+x)*sinh4/(sinh1*cosh1)-(pi*H/4)*(H/L)*(sinh4/sinh1^2)*((1+x)^2*theta3+(1-x)^2*theta4);
        pc(j,1)=ww*pcr;
        
        ptr=-yo+(H/2)*(1+x)*sinh4/(sinh1*cosh1)-(pi*H/4)*(H/L)*(sinh4/sinh1^2)*((1+x)^2*theta3+(1-x)^2*theta4);
        pt(j,1)=ww*ptr;
    else %Sainflou (method=1)     
        yc(j,1)=yo+H*(sinh2/sinh1)+pi*H*(H/L)*(sinh2/sinh1)*(cosh2/sinh1); %vertical elevation when crest at wall
        yt(j,1)=yo-H*(sinh2/sinh1)+pi*H*(H/L)*(sinh2/sinh1)*(cosh2/sinh1); %vertical elevation when trough at wall
        
        pcr=-yo-H*(sinh4/(sinh1*cosh1)); %pressure when crest at wall
        pc(j,1)=pcr*ww;
        
        ptr=-yo+H*(sinh4/(sinh1*cosh1)); %pressure when trough at wall
        pt(j,1)=ptr*ww;
    end
    
    mc(j,1)=pc(j,1)*(yc(j,1)+d); %incremental moment for cresh
    mt(j,1)=pt(j,1)*(yt(j,1)+d); %incremental moment for trough
    
    yo=yo-dd;
end

yc(N+1)=ycb;
yt(N+1)=ytb;

        
    



