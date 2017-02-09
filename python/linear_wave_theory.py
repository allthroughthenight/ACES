from helper_functions import *
import math

###############################################################################
## ACES Update to Python
#-------------------------------------------------------------
# Driver for Linear Wave Theory (page 2-1 in ACES User's Guide)
# Yields first-order approximations for various wave parameters of wave
# motion as predicted by linear wave theory

# Updated by: Evan Hataishi
# Date Created: February 6, 2017
# Date Verified: --

# Requires the following functions:
# ERRWAVBRK1
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   H: wave height (m or ft)
#   T: wave period (sec)
#   d: water depth (m or ft)
#   z: vertical coordinate (m or ft)
#   xL: horizontal coordinate as fraction of wavelength (x/L)

#   OUTPUT
#   L: wavelength (m or ft)
#   C: wave celerity (m/sec or ft/sec)
#   Cg: group celerity (m/sec or ft/sec)
#   E: energy density (N-m/m^2 or ft-lb/ft^2)
#   Ef: energy flux (N-m/sec-m or ft-lb/sec-ft)
#   Ur: Ursell number
#   eta: surface elevation (m or ft)
#   px: horizontal particle displacement (m or ft)
#   pz: vertical particle displacement (m or ft)
#   u: horizontal particle velocity (m/sec or ft/sec)
#   w: vertical particle velocity (m/sec or ft/sec)
#   dudt: horizontal particle acceleration (m/sec^2 or ft/sec^2)
#   dwdt: vertical particle accleration (m/sec^2 or ft/sec^2)
#   pres: pressure (N/m^2 or lb ft^2 )
###############################################################################
def linearWaveTheory(H, T, d, z, xL, unitSystem):
    ## *********** Don't change anything here ******************
    twopi = 2 * math.pi
    nIteration = 50
    if unitSystem == 'I': # imperial
        g = 32.17 # gravitational acceleration (ft/sec^2)
        rho = 1.989 # rho/g = 63.99/32.17 lb sec^2/ft^4 (sea water)
    elif unitSystem == 'M': # metric
        rho = 1025.09
        g = 9.81

    L, k = wavelen(d, T, nIteration, g)

    theta =  xL * twopi # theta=(kx-wt) where arbitrarily t=0 and k=2*pi/L

    # Check for monochromatic wave breaking (depth limited - no slope)
    Hb = errwavbrk1(d, 0.78)
    if (H >= Hb):
        print("Error: Input wave broken (Hb = %6.2f m)" % Hb)
        return

    # Check to make sure vertical coordinate is within waveform
    eta = (H / 2) * math.cos(theta)
    if not (z < eta and (z + d) > 0):
        print("Error: Point outside waveform.")
        return

    # Main computations
    arg = (2 * k * d / (math.sinh(2 * k * d)))
    tot = d + z

    C = L / T
    Cg = 0.5 * (1 + arg) * C
    E = (1 / 8) * rho * g * (H**2)
    Ef = E * Cg
    Ur = L**2 * H / (d**3)
    px = (-H / 2) * (math.cosh(k * tot) / math.sinh( k * d)) * math.sin(theta)
    py = ( H / 2) * (math.sinh(k * tot) / math.sinh(k * d)) * math.cos(theta)
    u = (H * math.pi / T) * (math.cosh(k * tot) / math.sinh( k * d)) * math.cos(theta)
    w = (H * math.pi / T) * (math.sinh(k * tot) / math.sinh(k * d)) * math.sin(theta)
    dudt = (H * 2 * math.pi**2 / (T**2)) * (math.cosh(k * tot) / math.sinh(k * d)) * math.sin(theta)
    dwdt = (-H * 2 * math.pi**2 / (T**2)) * (math.sinh(k * tot) / math.sinh(k * d)) * math.cos(theta)
    pres = -rho * g * z + rho * g * (H / 2) * (math.cosh(k * tot) / math.cosh(k * d)) * math.cos(theta)
    # come back to this!!! supposed to be py rather than pz??
    pz = 0
    return H, T, d, z, xL, L, C, Cg, E, Ef, Ur, eta, px, py, pz, u, w, dudt, dwdt, pres

class LinearWaveTheoryOutput:
    # Default INPUT
    H = 6.30
    T = 8
    d = 20.0
    z = -12.0
    xL = 0.75

    # OUTPUT
    L = 0
    C = 0
    Cg = 0
    E = 0
    Ef = 0
    Ur = 0
    eta = 0
    px = 0
    # missing py from matlab documentation
    py = 0
    pz = 0
    u = 0
    w = 0
    dudt = 0
    dwdt = 0
    pres = 0

    def __init__(self): pass

    def toString(self):
        print("\t\t\t\t\t %s \n" % ("Units"))
        print("%s \t\t %-6.2f \t %s \n" % ("Wavelength", self.L, "m"))
        print("%s \t\t %-6.2f \t %s \n" % ("Celerity", self.C, "m/s"))
        print("%s \t\t %-6.2f \t %s \n" % ("Group speed", self.Cg, "m/s"))
        print("%s \t\t %-8.2f \t %s \n" % ("Energy density", self.E, "N-m/m^2"))
        print("%s \t\t %-8.2f \t %s \n" % ("Energy flux", self.Ef, "N-m/m-s"))
        print("%s \t\t %-6.2f \n" % ("Ursell number", self.Ur))
        print("%s \t\t %-6.2f \t %s \n" % ("Elevation", self.eta, "m"))
        print("%s \t %-6.2f \t %s \n" % ("Horz. displacement", self.px, "m"))
        print("%s \t %-6.2f \t %s \n" % ("Vert. displacement", self.py, "m"))
        print("%s \t\t %-6.2f \t %s \n" % ("Horz. velocity", self.u, "m/s"))
        print("%s \t\t %-6.2f \t %s \n" % ("Vert. velocity", self.w,"m/s"))
        print("%s \t %-6.2f \t %s \n" % ("Horz. acceleration", self.dudt, "m/s^2"))
        print("%s \t %-6.2f \t %s \n" % ("Vert. acceleration", self.dwdt, "m/s^2"))
        print("%s \t\t %-8.2f \t %s \n" % ("Pressure", self.pres, "N/m^2"))
