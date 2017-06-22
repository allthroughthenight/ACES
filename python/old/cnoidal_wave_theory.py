from helper_functions import *
import math

def cnoidalWaveTheory(H, T, d, z, xL, time, O):
    output = cnoidalWaveTheory()
    output.H = H
    output.T = T
    output.d = d
    output.z = z
    output.xL = xL
    output.time = time
    output.O = O

    epsi = H/d
    Hb = errwavbrk1(d, 0.78)

    return output

class cnoidalWaveTheoryOutput:
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

cnoidalWaveTheory(6.30, 8, 20.0, -12, 0.75)
#    # INPUT
#    H = 6.30
#    T = 8
#    d = 20.0
#    z = -12.0
#    xL = 0.75
