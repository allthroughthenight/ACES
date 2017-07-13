import math

# Estimation of geostrophic wind

#   INPUT
#   z0: roughness length
#   zobs: elevation of wind observation
#   uobs: observed windspeed

#   OUTPUT
#   vg: geostrophic winds (cm/s)

def WAGEOS(uobs, zobs, z0):
	if z0 <= 0:
	    z0 = 30

	k = 0.4

	ustar = (k*uobs)/math.log(zobs/z0)
	cdland = 0.00255*z0**0.1639
	vg = ustar/math.sqrt(cdland)

	return vg