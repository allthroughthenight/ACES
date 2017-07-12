import math

# Determine "representative" fetch and wave direction

#   INPUT
#   ang1: angle of first radial fetch
#   dang: angle increment between radials
#   wdir: wind direction approach
#   x: radial fetch length at given angles

#   OUTPUT
#   F: representative fetch length
#   phi: angle between wind and wave directions
#   theta: angle of wave direction (relative to North)

def WGFET(ang1, dang, wdir, x):
	#Interpolate radial fetch lengths around the compass
	# Values are interpolated at whole degress so dang >=1

	nang = len(x) #length of radial fetches
	angn = ang1 + (nang - 1)*dang
	angnm = angn - dang
	nangm = nang - 1
	angle = ang1
	i = 0

	fa = []
	for j in range(nang):
		fa.append(angle + j*dang)

	xx = [0.0 for j in range(360)]
	xfin = [0.0 for j in range(360)]

	for deg in range(int(round(ang1)), int(round(angn)) + 1):
		ideg = deg
		if ideg < 0:
			ideg += 360
		if ideg >= 360:
			ideg -= 360

		if deg <= ang1:
			xx[ideg - 1] = x[0]
		elif deg >= angn:
			xx[ideg - 1] = x[nang - 1]
		else:
			if deg > fa[i + 1]:
				angle = min(angnm, angle + dang)
				i = min(nangm - 1, i + 1)
			tmp = (x[i + 1] - x[i])/dang
			xx[ideg - 1] = x[i] + tmp*(deg - angle)
	# end for loop

	for i in range(360):
		sumx = 0.0

		for j in range(15):
			k = i - 7 + j
			if k < 0:
				k += 360
			if k >= 360:
				k -= 360

			sumx += xx[k]

		xfin[i] = sumx / 15.0
	# end for loop

	iwdir = int(round(wdir))
	if iwdir < 0:
		iwdir += 360
	pmax = 0.0

	for i in range(91):
		k = iwdir + i - 1
		if k >= 360:
			k -= 360

		km = iwdir - i - 1

		if km < 0:
			km += 360

		if xfin[k] < xfin[km]:
			k = km

		ftmp = max(xfin[k], 0.0)
		phitmp = i
		ptmp = ftmp**0.28 * math.cos(phitmp*(math.pi / 180.0))**0.44

		if ptmp > pmax:
			pmax = ptmp
			phi = phitmp
			theta = k + 1
			F = ftmp
	# end for loop

	return F, phi, theta