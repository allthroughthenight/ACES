# Error check for monochromatic wave breaking on simple plane beach

#   INPUT
#   d: water depth
#   kappa: breaking index

#   OUTPUT
#   Hb: breaking wave height

def ERRWAVBRK1(d, kappa):
    Hb = kappa * d
    return Hb
