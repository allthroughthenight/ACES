function [inlsys,tbw,start,stop]=IH1(tinl,tbay,tsea)

if tinl==1
    %One inlet can have one sea and one bay - assigned numbers indicate
    %order for computational routine (began at sea 1 and end at bay 2 for
    %inlet A)
    if tsea==1 && tbay==1
        tbw=1;
        start(1)=1;
        stop(1)=2;
        inlsys=1;
    end
    
else
    if tsea==1
        %Two inlets having one sea and one bay - assigned numbers indicate
        %order for computational routine (begin at sea 1 and end at bay 2 for
        %inlet A; begin at sea 1 and end at bay 2 for inlet B)
        tbw=2;
        start(1)=1;
        stop(1)=2;
        start(2)=1;
        stop(2)=2;
        inlsys=2;
    elseif tsea==2
        %Two inlets having two seas and one bay - assigned numbers indicate
        %order for computational routine (begin at sea 1 and end at bay 3 for
        %inlet A; begin at sea 2 and end at bay 3 for inlet B)
        tbw=3;
        start(1)=1;
        stop(1)=3;
        start(2)=2;
        inlsys=3;
    end
end


