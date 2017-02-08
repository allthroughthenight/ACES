from helper_functions import *
import math

def linearWaveTheory(H, T, d, z, xL, unitSystem):
    output = LinearWaveTheoryOutput()
    output.H = H
    output.T = T
    output.d = d
    output.z = z
    output.xL = xL
    output.unitSystem = 'I'

    # Converstion section
    twopi = 2 * math.pi
    nIteration = 50
    if unitSystem == 'I': # imperial
        g=32.17 # gravitational acceleration (ft/sec^2)
        rho=1.989 # rho/g = 63.99/32.17 lb sec^2/ft^4 (sea water)
    elif unitSystem == 'M': # metric
        rho = 1025.09
        g = 9.81
    # end conversion

    output.L, k = wavelen(output.d, output.T, nIteration, g)

    theta =  output.xL * twopi

    # Check for monochromatic wave breaking (depth limited - no slope)
    Hb = errwavbrk1(d, 0.78)
    if (output.H >= Hb):
        print("Error: Input wave broken (Hb = %6.2f m)\n" % (Hb))
        return

    # Check to make sure vertical coordinate is within waveform
    eta = (output.H / 2) * math.cos(theta)
    if z >= eta or (z + d) <= 0:
       print("Error: Point outside waveform.\n")
       return

    # Main computations
    arg = (2 * k * output.d / (math.sinh(2 * k * output.d)))
    tot = output.d + output.z

    output.C = output.L / output.T
    output.Cg = 0.5 * (1 + arg) * output.C
    output.E = (1 / 8) * rho * g * (output.H**2)
    output.Ef = output.E * output.Cg
    output.Ur = output.L**2 * output.H / (output.d**3)
    output.px = (-output.H / 2) * (math.cosh(k * tot) / math.sinh( k * output.d)) * math.sin(theta)
    output.py = ( output.H / 2) * (math.sinh(k * tot) / math.sinh(k * output.d)) * math.cos(theta)
    output.u = (output.H * math.pi / output.T) * (math.cosh(k * tot) / math.sinh( k * output.d)) * math.cos(theta)
    output.w = (output.H * math.pi / output.T) * (math.sinh(k * tot) / math.sinh(k * output.d)) * math.sin(theta)
    output.dudt = (output.H * 2 * math.pi**2 / (output.T**2)) * (math.cosh(k * tot) / math.sinh(k * output.d)) * math.sin(theta)
    output.dwdt = (-output.H * 2 * math.pi**2 / (output.T**2)) * (math.sinh(k * tot) / math.sinh(k * output.d)) * math.cos(theta)
    output.pres = -rho * g * output.z + rho * g * (output.H / 2) * (math.cosh(k * tot) / math.cosh(k * output.d)) * math.cos(theta)

    return output

class LinearWaveTheoryOutput:
    # INPUT
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
    # missing from matlab documentation
    py = 0
    pz = 0
    u = 0
    w = 0
    dudt = 0
    dwdt = 0
    pres = 0

    def __init__(self): pass
    # syntax - self.test = test

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
