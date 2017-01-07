function [fndcst]=NFACS(yr,dayj,hr)

deg2rad=pi/180;

[dh,dI,dN,dNu,dnup,dnup2,dp,dp1,dpc,ds,dxi]=ORBIT(yr,dayj,hr);

I=dI*deg2rad;
Nu=dNu*deg2rad;
pc=dpc*deg2rad;

sinI=sin(I);
sinI2=sin(I/2);
sin2I=sin(2*I);
cosI=cos(I);
cosI2=cos(I/2);
tanI2=tan(I/2);

eq73=(2/3-sinI^2)/0.5021;
eq74=sinI^2/0.1578;
eq75=sinI*cosI2^2/0.3800;
eq76=sin2I/0.7214;
eq77=sinI*sinI2^2/0.0164;
eq78=cosI2^4/0.9154;
eq149=cosI2^6/0.8758;
eq196=sqrt(0.25+1.5*(cosI*cos(2*pc)/cosI2^2)+(9/4)*(cosI^2/cosI2^4));
eq207=eq75*eq196;
eq213=sqrt(1-12*tanI2^2*cos(2*pc)+36*tanI2^4);
eq215=eq78*eq213;
eq227=sqrt(0.8965*sin2I^2+0.6001*sin2I*cos(Nu)+0.1006);
eq235=0.001+sqrt(19.0444*sinI^4+2.7702*sinI^2*cos(2*Nu)+0.0981);


fndcst(1)=eq78;
fndcst(2)=1.0;
fndcst(3)=eq78;
fndcst(4)=eq227;
fndcst(5)=fndcst(1)^2;
fndcst(6)=eq75;
fndcst(7)=fndcst(1)^3;
fndcst(8)=fndcst(1)*fndcst(4);
fndcst(9)=1.0;
fndcst(10)=fndcst(1)^2;
fndcst(11)=eq78;
fndcst(12)=1.0;
fndcst(13)=eq78;
fndcst(14)=eq78;
fndcst(15)=eq77;
fndcst(16)=eq78;
fndcst(17)=1.0;
fndcst(18)=eq207;
fndcst(19)=eq76;
fndcst(20)=eq73;
fndcst(21)=1.0;
fndcst(22)=1.0;
fndcst(23)=eq78;
fndcst(24)=eq74;
fndcst(25)=eq75;
fndcst(26)=eq75;
fndcst(27)=1.0;
fndcst(28)=1.0;
fndcst(29)=eq75;
fndcst(30)=1.0;
fndcst(31)=eq78;
fndcst(32)=eq149;
fndcst(33)=eq215;
fndcst(34)=fndcst(1)^2*fndcst(4);
fndcst(35)=eq235;
fndcst(36)=fndcst(1)^4;
fndcst(37)=eq78;
end