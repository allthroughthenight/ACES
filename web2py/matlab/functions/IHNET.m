function [inlt,dp2]=IHNET(inlt)
g=32.17;
fsum=0;

for k_inlt=1:length(inlt) %looping over number of inlets
    is=inlt(k_inlt).cs_no; %number of inlet cross-sections
    ic=inlt(k_inlt).chan_no; %number of inlet channels
    
    areamin=100000000;
    for i_cs=1:is %Looping over number of cross sections
        cs_area=0;
        inlt(k_inlt).cs(i_cs).elev=abs(inlt(k_inlt).cs(i_cs).elev);
        dp=inlt(k_inlt).cs(i_cs).elev;
        dx=inlt(k_inlt).cs(i_cs).dx;
        numpts=length(inlt(k_inlt).cs(i_cs).elev);
        
        for j_elev=1:(numpts-1) %Looping over number of elevations to calculate area
            cs_area=cs_area+dx*(dp(j_elev)+dp(j_elev+1))/2;
        end
        inlt(k_inlt).cs(i_cs).area=cs_area;
        
        if inlt(k_inlt).cs(i_cs).area<areamin
            areamin=inlt(k_inlt).cs(i_cs).area;
        end
    end
    q=areamin*3.23;
    
    for i_cs=1:is%isec %Looping over number of cross sections
        dp=inlt(k_inlt).cs(i_cs).elev;
        dx=inlt(k_inlt).cs(i_cs).dx;
        numpts=length(inlt(k_inlt).cs(i_cs).elev);
        
        inlt(k_inlt).cs(i_cs).width=dx*(numpts-1);
        
        %Splitting cross section into 2000 equal distant depths located at
        %delx2 using linear interpolation
        delx2=dx*(numpts-1)/1999;
        dp2(1)=0;
        dp2(2000)=0;
        
        for j=2:1999
            x_new=(j-1)*delx2; %x
            j1=floor(x_new/dx);
            deld=x_new-j1*dx; %x-xo
            j1=j1+1;
            dp2(j)=dp(j1)+deld*(dp(j1+1)-dp(j1))/dx; %yo+(x-xo)((y1-yo)/(x1-xo))
            if dp2(j)<0.0
                dp2(j)=1.0;
            end
        end
        
        %Compute mean depths, flow resistance parameters, and Manning's n
        %for each of the 1999 sections
        for j=2:2000
            dp2(j-1)=(dp2(j)+dp2(j-1))/2;
            xn=0.03777-0.000667*dp2(j-1);
            if xn<0.01
                xn=0.01;
            end
            ar=dp2(j-1)*delx2;
            c(j-1)=(ar*ar)*dp2(j-1)^0.3333/((xn*xn)*(q*q)*delx2);
        end
        csum=sum(c);
        
        %Compute weight function of each 1999 sections and fraction of flow
        %for 10 equal channels (20 cells/channel)
        delx20=delx2*20; %dx of equal channels
        dx2(1)=delx20;
        dpt(1:100)=0;
        flow2(1:100)=0;
        
        for j=1:1999
            c(j)=c(j)/csum;
            isub2=floor((j-1)/20+1); %channel increment (from 1-10)
            flow2(isub2)=flow2(isub2)+c(j)*100; %flow in each channel is a sum of the flow per 10 cells
            dpt(isub2)=dpt(isub2)+dp2(j); %sum of depths in for every 20 cells
            if isub2>1
                dx2(isub2)=dx2(isub2-1)+delx20;
            end
        end
        dpt=dpt/20; %average depth for 20 cells
        inlt(k_inlt).cs(i_cs).x=dx2;
        inlt(k_inlt).cs(i_cs).dpt=dpt;
        inlt(k_inlt).cs(i_cs).flow=flow2;
        
        ns(1:ic)=0;
        wgt(1:ic)=0;
        inlt(k_inlt).cs(i_cs).a(1:ic)=0;
        inlt(k_inlt).cs(i_cs).b(1:ic)=0;
        j=1;
        
        wt=1.0/ic;
        for ix=1:1999
            inlt(k_inlt).cs(i_cs).a(j)=inlt(k_inlt).cs(i_cs).a(j)+dp2(ix)*delx2; %channel area
            inlt(k_inlt).cs(i_cs).b(j)=inlt(k_inlt).cs(i_cs).b(j)+delx2; %channel width
            wgt(j)=wgt(j)+c(ix); %channel weight
            ns(j)=ns(j)+1;
            if wgt(j)>=wt
                j=j+1;
            end
            if wgt(j)>=wt && j>ic
                j=j-1;
            end
        end
        nit=50;
        
        for ibs=1:nit
            ccs=0;
            
            for j=1:ic %Looping over number of channels
                inlt(k_inlt).cs(i_cs).d(j)=inlt(k_inlt).cs(i_cs).a(j)/inlt(k_inlt).cs(i_cs).b(j); %channel depth (area/width)
                xn=0.0377-0.000667*inlt(k_inlt).cs(i_cs).d(j);
                if xn<=0.01
                    xn=0.01;
                end
                wgt(j)=inlt(k_inlt).cs(i_cs).a(j)^2*inlt(k_inlt).cs(i_cs).d(j)^0.3333/(xn^2*q^2*inlt(k_inlt).cs(i_cs).b(j));
            end
            ccs=sum(wgt);
            
            wgt=wgt./ccs;
           
            xmax=-1000000;
            xmin=1000000;
            difference=0;
            
            for j=1:ic
                er=abs(wgt(j)-wt)*100;
                if er>difference
                    difference=er;
                end
                xc(j)=(wgt(j)-wt)*1999*0.2;
                if xc(j)>xmax
                    jmax=j;
                    xmax=xc(j);
                end
                if xc(j)<xmin
                    jmin=j;
                    xmin=xc(j);
                end
                inlt(k_inlt).cs(i_cs).wgt(j)=wgt(j);
            end
            
            for j=1:ic
                ncor(j)=xc(j);
            end
            ncc=sum(ncor);
            
            if ncc<0
                ncor(jmin)=ncor(jmin)-ncc;
            end
            if ncc>0
                ncor(jmax)=ncor(jmax)-ncc;
            end
            
            ix=0;
            for j=1:ic
                inlt(k_inlt).cs(i_cs).a(j)=0;
                inlt(k_inlt).cs(i_cs).b(j)=0;
                ns(j)=ns(j)-ncor(j);
                if ns(j)<1
                    ns(j)=1;
                end
                nn=ns(j);
                
                for lfix=1:nn
                    ix=ix+1;
                    if ix>1999
                        break
                    end
                    inlt(k_inlt).cs(i_cs).a(j)=inlt(k_inlt).cs(i_cs).a(j)+dp2(ix)*delx2;
                    inlt(k_inlt).cs(i_cs).b(j)=inlt(k_inlt).cs(i_cs).b(j)+delx2;
                end
            end
            if difference<0.3
                break
            end
        end
        inlt(k_inlt).cs(i_cs).f=0;
        for j=1:ic
            xn=0.03777-0.000667*inlt(k_inlt).cs(i_cs).d(j);
            inlt(k_inlt).cs(i_cs).f=inlt(k_inlt).cs(i_cs).f+g*xn^2*abs(wgt(j)*q)*wgt(j)*q*inlt(k_inlt).cs(i_cs).b(j)/2.208*inlt(k_inlt).cs(i_cs).d(j)^0.3333*inlt(k_inlt).cs(i_cs).a(j)^2;
        end
        fsum=fsum+inlt(k_inlt).cs(i_cs).f;
    end
    for i_cs=1:is
        inlt(k_inlt).cs(i_cs).f=(inlt(k_inlt).cs(i_cs).f/fsum)*100;
    end
end



