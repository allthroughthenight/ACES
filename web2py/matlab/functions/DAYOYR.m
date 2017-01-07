% Determines the day of the year

%   INPUT
%   yr: year of interest (ex. 1989)
%   month: month of interest (Jan=1...Dec=12)
%   day: day (of the month) of interest

%   OUTPUT
%   dayj: Julian day of the year

function [dayj]=DAYOYR(yr,month,day)

    daysinmonth=[0;31;59;90;120;151;181;212;243;273;304;334];
    if mod(yr,4)==0 %checking for leap year to add 1 day
        leapyr=1;
        daysinmonth(3:12)=daysinmonth(3:12)+leapyr;
    end
    dayj=daysinmonth(month)+day;
end


