function [tidelv,xtim]=IHINTT_sea(yr,mon,day,hr,tlhrs,delt,long)

acst=[28.9841042;30.0;28.4397295;15.0410686;57.9682084;13.9430356;86.9523127; ...
        44.0251729;60.0;57.4238337;28.5125831;90.0;27.9682084;27.8953548; ...
        16.1391017;29.4556253;15.0;14.4966939;15.5854433;0.5443747;0.0821373; ...
        0.0410686;1.0158958;1.0980331;13.4715145;13.3986609;29.9589333; ...
        30.0410667;12.8542862;14.9589314;31.0158958;43.4761563;29.5284789; ...
        42.9271398;30.0821373;115.9364169;58.9841042];
    
pcst=[2;2;2;1;4;1;6;3;4;4;2;6;2;2;1;2;1;1;1;0;0;0;0;0;1;1;2;2;1;1;2;3;2;3;2; ...
        8;4];
    
fid = fopen('tides_sihsource.txt');
C = textscan(fid, '%s %f %f');
fclose(fid);

cst=C{1};
amp=C{2};
ep=C{3};

deltmin=delt/60; %output time interval in minutes

ntid=floor(tlhrs/deltmin)+1;
[alpha,fndcst]=GAGINI(1,yr,mon,day,hr,tlhrs,long,ep,acst,pcst);

for i=1:ntid
    xtim(i)=(i-1)*deltmin;
    [tidelv(i)]=TIDELV(1,xtim(i),amp,alpha,fndcst,acst);
end

xtim=(0:length(tidelv)-1)*deltmin;
plot(xtim,tidelv)

