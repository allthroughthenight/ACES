import math

from WASHR import WASHR

#   INPUT
#   arg: ratio of observed wind elevation over stability length
#   c: multiple coefficient for arg (if arg >0)

#   OUTPUT
#   psi: universal similarity function 

def WAPSI(arg, c):
	if arg > 0:
	    psi = c*arg
	else:
	    phi = WASHR(arg)
	    psi = 1.0 - phi - 3*math.log(phi) +\
	    	2.0*math.log((1.0 + phi)/2.0) +\
	    	2.0*math.atan(phi) - (math.pi/2.0) +\
	    	math.log((1.0 + phi**2)/2.0)

	return psi