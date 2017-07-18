import math

# Transforms trapezoidal breakwater into a hydraulically equivalent
# rectangular breakwater

#   INPUT
#   rechd: head difference across equivalent rectangular breakwater
#   traphd: head difference across trapezoidal breakwater
#   d: water depth
#   nummat: number of materials in the breakwater
#   numlay: number of layers in the breakwater
#   diam: mean diameter of material in the breakwater
#   por: porosity of the various materials
#   thk: thickness of each layer
#   len: length of each material in the breakwater
#   pref: porosity of reference material (0.435)
#   dref: one half mean diameter of reference material

#   OUTPUT
#   lequiv: equivalent length of rectangular breakwater

#   OTHER:
#   betar and beta: turbulent resistance coefficients for the equivalent
#                   and trapezoidal breakwater

def EQBWLE(rechd, traphd, d, nummat, numlay, diam, por, thk, hlen, pref, dref):
    # find betar and beta
    beta0 = 2.7
    betar = beta0*((1.0 - pref)/(pref**3*dref))

    beta = []
    for i in range(nummat):
        beta.append(beta0*((1.0 - por[i])/(por[i]**3*diam[i])))

    # find equivalent rectangular breakwater length
    ind = [0.0 for i in range(nummat)]
    ind2 = [0.0 for j in range(numlay)]
    for j in range(numlay): #layer is columns
        for k in range(nummat): # material number is rows
            ind[k] = (beta[k]/betar)*hlen[k][j]

        sum1 = sum(ind)
        ind2[j] = (thk[j]/d)/math.sqrt(sum1)

    sum2 = sum(ind2)
    lequiv = 1.0/sum2**2*(rechd/traphd)

    return lequiv