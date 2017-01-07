function [v,qcell]=IHRKGS(a,b,d,n,l,stime,delt,nbay,nsea,outpt,yr,mon,day,hr,tlhrs,bc_dt,bc_long,inflow_dt,inflow_q,N1,N2,ninlet,cdf,iss,icc,velin,velx,velch,nlocs,bay_area,beta)

y(1:ninlet)=1;
dery(1:ninlet)=0.001;

for j=1:nbay
    y(j+ninlet)=0;
    dery(j+ninlet)=1/nbay-ninlet*0.001;
end

ndim=ninlet+nbay;
for i=1:ndim
    aux(8,i)=0.066666667*dery(i);
end

x=1;
xend=stime;
prmt(4)=0.1;
prmt(5)=0;
xstop=outpt;
iter=0;
nvel=0;
nn=nsea+nbay;
iset=1;

for k=1:ninlet
    is=iss(k)+1;
    ic=icc(k);
    for i=1:is
        for j=1:ic
            hh(i,j,k)=0;
        end
    end
end

[v,qcell]=IHSETEQ(a,b,d,n,l,nsea,yr,mon,day,hr,tlhrs,bc_dt,bc_long,nbay,inflow_dt,inflow_q,y,hh,N1,N2,ninlet,cdf,iss,icc,velin,velx,velch,nlocs,bay_area,beta);
    


