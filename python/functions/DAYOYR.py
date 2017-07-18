import math

# Determines the day of the year

#   INPUT
#   yr: year of interest (ex. 1989)
#   month: month of interest (Jan=1...Dec=12)
#   day: day (of the month) of interest

#   OUTPUT
#   dayj: Julian day of the year

def DAYOYR(yr, month, day):
    daysinmonth = [0,31,59,90,120,151,181,212,243,273,304,334]

    if (yr % 4) == 0: #checking for leap year to add 1 day
        leapyr = 1

        for i in range(2, 12):
        	daysinmonth[i] = daysinmonth[i] + leapyr
    # end if

    dayj = daysinmonth[month - 1] + day

    return dayj