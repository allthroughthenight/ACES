function [v,qcell]=IHSETEQ(a,b,d,n,l,nsea,yr,mon,day,hr,tlhrs,delt,long,nbay,inflow_dt,q,y,hh,N1,N2,ninlet,cdf,iss,icc,ick,ici,icj,numc,aby,beta)

g=32.17;

for i=1:nsea
    [yy_sea,xtim]=IHINTT_sea(yr,mon,day,hr,tlhrs,delt,long);
    h(:,i)=yy_sea;
end

for i=1:nbay
    ii=(nsea+i);
    h(:,ii)=y(ninlet+i);
    [yy_bay]=IHINTT_bay(inflow_dt,q,tlhrs);
    qinflo(:,i)=yy_bay;
end


icount=1;
for k=1:ninlet
    zeta(k)=0;
    iflag(k)=0;
    amin(k)=1*10^(25);
    qq=y(k);
    cd=cdf(k);
    ic=icc(k);
    is=iss(k);
    le=0;
    
    for i=1:is
        for j=1:ic
            le=le+l(i,j,k)/ic;
        end
    end
    
    sumf=0;
    for i=1:is
        fy(i)=0;
        sumc=0;
        for j=1:ic
            den=n(i,j,k)^2*qq^2*b(i,j,k)*l(i,j,k);
            if den<=0.001
                den=1;
            end
            depth=d(i,j,k)+hh(i,j,k);
            if depth<=0.1
                depth=0.1;
            end
            if a(i,j,k)<0.1
                a(i,j,k)=0.1;
            end
            c(j)=a(i,j,k)^2*depth^0.33333/den;
            sumc=sumc+c(j);
        end
        
        for j=1:ic
            w(i,j)=c(j)/sumc;
        end
        fy(i)=1/sumc;
        sumf=sumf+fy(i);
    end
    i1=N1(k);
    i2=N2(k);
    ff=fy(1)/2;
    
    for j=1:ic
        hh(i,j,k)=h(i1)-(h(i1)-h(i2))/sumf*ff
    end
    
    if is>1
        for i=2:is
            ff=ff+(fy(i-1)+fy(i))/2;
            for j=1:ic
                hh(i,j,k)=h(i1)-(h(i1)-h(i2))/sumf*ff;
                if abs(hh(i,j,k))>100
                    hh(i,j,k)=0;
                end
            end
        end
    end
    ae=0;
    
    for i=1:is
        dl=0;
        aa=0;
        for j=1:ic
            dl=dl+l(i,j,k)/(ic*le);
            a(i,j,k)=b(i,j,k)*(d(i,j,k)+hh(i,j,k))+hh(i,j,k)*abs(hh(i,j,k))*(zeta(k)/ic);
            if a(i,j,k)<0.1
                a(i,j,k)=0.1;
            end
            aa=aa+a(i,j,k);
        end
        if aa<1.0
            iflag(k)=1;
        end
        if aa<amin(k)
            amin(k)=aa;
        end
        ae=ae+dl/aa;
    end
    
    ae=1/ae;
    vm(k)=qq/amin(k);
    if iflag(k)==1
        vm(k)=0;
    end
    rnk(k,2)=ae/(2*le)*cd*qq*abs(qq)/(amin(k)^2);
    rnk(k,3)=g*ae/le*(h(i2)-h(i1));
    rnk(k,4)=0;
    for i=1:is
        ac=0;
        for j=1:ic
            ac=ac+a(i,j,k);
        end
        for j=1:ic
            depth=d(i,j,k)+hh(i,j,k);
            if depth<0.1
                depth=0.1;
            end
            cc=ae/(le*ac)*g*n(i,j,k)^2*abs(w(i,j)*qq)*w(i,j)*qq*b(i,j,k)*l(i,j,k)/(2.208*depth^0.333*a(i,j,k)^2);
            rnk(k,4)=rnk(k,4)+cc;
        end
    end
    rnk(k,1)=-rnk(k,2)-rnk(k,3)-rnk(k,4);
    dery(k)=rnk(k,1);
    while numc>0 && icount<=numc && k==ick(icount)
        idx=ici(icount);
        jdx=icj(icount);
        wgt=w(idx,jdx,k);
        qcell=qq*wgt;
        v(icount)=qcell/a(idx,jdx,k);
        icount=icount+1 ;
    end
end

for i=1:nbay
    qt=qinflo(i);
    ii=i+nsea;
    nn=ii;
    
    for j=1:ninlet
        if N1(j)==nn
            qt=qt-y(j);
        end
        if N2(j)==nn
            qt=qt+y(j);
        end
    end
    qt
    abay=aby(i)*(1+beta(i)*h(nn));

    dery(ninlet+i)=qt/abay;
end
