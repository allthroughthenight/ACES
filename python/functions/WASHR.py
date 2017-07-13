#   INPUT
#   arg: ratio of observed wind elevation over stability length

def WASHR(arg):
	Ri = arg
	Rinew = arg*(1.0 - 18.0*Ri)**(1.0/4.0)
	diff = abs(Rinew - Ri)

	while diff > 0.001:
	    Ri = Rinew
	    Rinew = arg*(1.0 - 18.0*Ri)**(1.0/4.0)
	    diff = abs(Rinew - Ri)

	phiu = 1.0/(1.0 - 18.0*Rinew)**(1.0/4.0)

	return phiu