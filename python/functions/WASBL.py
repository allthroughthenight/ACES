import math

from WAPSI import WAPSI

# Solution in the constant stress region

#   INPUT
#   delt: air-sea temperature difference
#   uobs: observed wind speed
#   zobs: elevation of wind observation

#   OUTPUT
#   sbl10m: equivalent neutral windspeed at 10 m elevation 

def WASBL(uobs, delt, zobs):
	diff1 = 100.0
	diff2 = 100.0

	L = delt
	z = 1000.0 #10 m in cm
	k = 0.4 #von Karman constant

	ustar = uobs*(z / zobs)**(-1.0/7.0)
	cd = 0.001*(0.75 + 0.067*0.01*uobs)
	ustar = math.sqrt(cd)*ustar

	if delt > 0.0:
		ustar = 0.8*ustar
	else:
		ustar = 1.2*ustar

	c1 = 0.1525
	c2 = 0.019/980.0
	c3 = -0.00371

	while diff1 > 0.1:
		z0 = (c1/ustar) + (c2*ustar**2) + c3
		lnzzo = math.log(zobs/z0)
		if abs(delt) < 1.0:
			psi = 0.0
		else:
			while diff2 > 1.0:
				psi = WAPSI((zobs/L), -1.5)
				Lnew = 1.79*(ustar**2/delt)*(lnzzo - psi)
				diff2 = abs(Lnew - L)
				if diff2 > 1.0:
					L = Lnew
			# end while loop
		# end if

		ustarn = (uobs*k)/(lnzzo - psi)
		diff1 = abs(ustar - ustarn)
		if diff1 > 0.1:
			ustar = (ustar + ustarn)/2.0
	# end while loop

	sbl10m = (ustar/k)*math.log(z/z0)

	return sbl10m