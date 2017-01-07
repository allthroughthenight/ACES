
function [yy]=IHINTT_bay(dt,q,tlhrs)

dtmin=dt/60;

t=[0:dtmin:(length(q)-1)*dtmin];
x=[0:1:tlhrs];
yy=interp1(t,q,x,'spline');

plot(x,yy)
ylim([3000 4400])