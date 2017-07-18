import math

# Redefines an angle in 0-360 (+) format

#   INPUT
#   arg: angle to be redefined

#   OUTPUT:
#   angle360: redefined angle between 0-360 deg

def ANG360(arg):
    zero = 360.0
    angle360 = arg % zero
    if angle360 < 0.0:
        angle360 = angle360 + zero

    return angle360