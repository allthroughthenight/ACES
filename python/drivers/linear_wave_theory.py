import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRWAVBRK1 import ERRWAVBRK1
from WAVELEN import WAVELEN
import numpy as np
import matplotlib.pyplot as plt

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Linear Wave Theory (page 2-1 in ACES User's Guide)
# Yields first-order approximations for various wave parameters of wave
# motion as predicted by linear wave theory

# Transferred by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: March 17, 2011
# Date Modified: June 26th, 2016 by yaprak

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
#   LOOK AT PZ AND PY
#   pz: vertical particle displacement (m or ft)
#   u: horizontal particle velocity (m/sec or ft/sec)
#   w: vertical particle velocity (m/sec or ft/sec)
#   dudt: horizontal particle acceleration (m/sec^2 or ft/sec^2)
#   dwdt: vertical particle accleration (m/sec^2 or ft/sec^2)
#   pres: pressure (N/m^2 or lb ft^2 )
## -------------------------------------------------------------

class LinearWaveTheory(BaseDriver):
    def __init__(self, H = None, T = None, d = None,\
        z = None, xL = None):
        if H != None:
            self.isSingleCase = True
            self.defaultValueH = H
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d
        if z != None:
            self.isSingleCase = True
            self.defaultValue_z = z
        if xL != None:
            self.isSingleCase = True
            self.defaultValue_xL = xL

        super(LinearWaveTheory, self).__init__()

        self.performPlot()
    # end __init__

    def userInput(self):
        super(LinearWaveTheory, self).userInput()

        self.waterType, self.rho =\
            USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField(\
                "H: wave height (%s)" % self.labelUnitDist, 0.1, 200.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField(\
                "T: wave period (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField(\
                "d: water depth (%s)" % self.labelUnitDist, 0.1, 5000.0))
        if not hasattr(self, "defaultValue_z"):
            self.inputList.append(BaseField(\
                "z: vertical coordinate (%s)" % self.labelUnitDist,\
                -5100.0, 100.0))
        if not hasattr(self, "defaultValue_xL"):
            self.inputList.append(BaseField(\
                "xL: horizontal coordinate as fraction of wavelength (x/L)",\
                0.0, 1.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "linear_wave_theory")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueH"):
            H = self.defaultValueH
        else:
            H = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueT"):
            T = self.defaultValueT
        else:
            T = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_d"):
            d = self.defaultValue_d
        else:
            d = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_z"):
            z = self.defaultValue_z
        else:
            z = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_xL"):
            xL = self.defaultValue_xL
        else:
            xL = caseInputList[currIndex]
            currIndex = currIndex + 1

        return H, T, d, z, xL
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, d, z, xL = self.getCalcValues(caseInputList)

        twopi = 2*math.pi
        nIteration = 50

        L, k = WAVELEN(d, T, nIteration, self.g)

        theta = xL*twopi #theta=(kx-wt) where arbitrarily t=0 and k=2*pi/L

        # Check for monochromatic wave breaking (depth limited - no slope)
        Hb = ERRWAVBRK1(d, 0.78)
        if not (H < Hb):
            print("Error: Input wave broken (Hb = %6.2f %s)" %\
                (Hb, self.labelUnitDist))

        # Check to make sure vertical coordinate is within waveform
        eta = (H/2)*math.cos(theta)
        if not (z < eta and (z + d) > 0):
            print("Error: Point outside waveform.")

        # Main Computations
        arg = (2*k*d/(math.sinh(2*k*d)))
        tot = d + z

        C = L/T
        Cg = 0.5*(1 + arg)*C
        E = (1.0/8.0)*self.rho*self.g*(H**2)
        Ef = E*Cg
        Ur = L**2*H/(d**3)
        px = (-H/2)*(math.cosh(k*tot)/math.sinh(k*d))*math.sin(theta)
        py = (H/2)*(math.sinh(k*tot)/math.sinh(k*d))*math.cos(theta)
        u = (H*math.pi/T)*(math.cosh(k*tot)/math.sinh(k*d))*math.cos(theta)
        w = (H*math.pi/T)*(math.sinh(k*tot)/math.sinh(k*d))*math.sin(theta)
        dudt = (H*2*math.pi**2/(T**2))*(math.cosh(k*tot)/math.sinh(k*d))*math.sin(theta)
        dwdt = (-H*2*math.pi**2/(T**2))*(math.sinh(k*tot)/math.sinh(k*d))*math.cos(theta)
        pres = -self.rho*self.g*z + self.rho*self.g*(H/2)*(math.cosh(k*tot)/math.cosh(k*d))*math.cos(theta)

        # plotting waveform
        plotxL = np.arange(-1, 1, 0.001)
        plottheta = plotxL * np.pi * 2

        ploteta = (H / 2) * np.cos(plottheta)
        plotu = (H * np.pi / T) * (np.cosh(k * tot) / np.sinh(k * d)) * np.cos(plottheta)
        plotw = (H * np.pi / T) * (np.sinh(k * tot) / np.sinh(k * d)) * np.sin(plottheta)

        plt.subplot(3, 1, 1)
        plt.plot(plotxL, ploteta, lw=2)
        plt.ylabel('Elevation [%s]' % self.labelUnitDist)
        plt.ylim(min(ploteta) - 1, max(ploteta) + 1)
        plt.axhline(color = 'r', linestyle = '--')

        # subplot
        plt.subplot(3, 1, 2)
        plt.plot(plotxL, plotu, lw=2)
        plt.axhline(color = 'r', linestyle = '--')
        plt.ylabel('Velocity, u [%s/s]' % self.labelUnitDist)
        plt.ylim(min(plotu) - 1, max(plotu) + 1)

        # subplot
        plt.subplot(3, 1, 3)
        plt.plot(plotxL, plotw, lw=2)
        plt.axhline(color = 'r', linestyle = '--')
        plt.ylabel('Velocity, w [%s/s]' % self.labelUnitDist)
        plt.ylim(min(plotw) - 1, max(plotw) + 1)

        plt.tight_layout(pad=0.4)

        plt.show()

        print("\t\t\t\t\tUnits")
        print("Wavelength\t\t\t%-6.2f\t%s" % (L, self.labelUnitDist))
        print("Celerity\t\t\t%-6.2f\t%s/s" % (C, self.labelUnitDist))
        print("Group speed\t\t\t%-6.2f\t%s/s" % (Cg, self.labelUnitDist))
        print("Energy density\t\t\t%-8.2f%s-%s/%s^2" %\
            (E, self.labelUnitWt, self.labelUnitDist, self.labelUnitDist))
        print("Energy flux\t\t\t%-8.2f%s-%s/%s-s" %\
            (Ef, self.labelUnitWt, self.labelUnitDist, self.labelUnitDist))
        print("Ursell number\t\t\t%-6.2f" % Ur)
        print("Water Surface Elevation\t\t%-6.2f\t%s" %\
            (eta, self.labelUnitDist))
        print("Horz. displacement\t\t%-6.2f\t%s" % (px, self.labelUnitDist))
        print("Vert. displacement\t\t%-6.2f\t%s" % (py, self.labelUnitDist))
        print("Horz. velocity\t\t\t%-6.2f\t%s/s" % (u, self.labelUnitDist))
        print("Vert. velocity\t\t\t%-6.2f\t%s/s" % (w, self.labelUnitDist))
        print("Horz. acceleration\t\t%-6.2f\t%s/s^2" %\
            (dudt, self.labelUnitDist))
        print("Vert. acceleration\t\t%-6.2f\t%s/s^2" %\
            (dwdt, self.labelUnitDist))
        print("Pressure\t\t\t%-8.2f%s/%s^2" %\
            (pres, self.labelUnitWt, self.labelUnitDist))

        dataDict = {"H": H, "T": T, "d": d, "z": z, "xL": xL,\
            "L": L, "C": C, "Cg": Cg, "E": E, "Ef": Ef,\
            "Ur": Ur, "eta": eta, "px": px, "py": py,\
            "u": u, "w": w, "dudt": dudt, "dwdt": dwdt, "pres": pres}
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Linear Wave Theory Summary\n\n");

        self.fileRef.write("Input\n")
        self.fileRef.write("Wave heights\t\t\t%8.2f %s\n" %\
            (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("Wave period\t\t\t%8.2f s\n" % dataDict["T"])
        self.fileRef.write("Water depth\t\t\t%8.2f %s\n" %\
            (dataDict["d"], self.labelUnitDist))
        self.fileRef.write("Vertical coordinate\t\t%8.2f %s\n" %\
            (dataDict["z"], self.labelUnitDist))
        self.fileRef.write("Horizontal coordinate as\t%8.2f (x/L)\n" %\
            dataDict["xL"])
        self.fileRef.write("fraction of wavelength\n\n")

        self.fileRef.write("Item\t\t\t\tValue\t\tUnits\n")
        self.fileRef.write("Wavelength\t\t\t%8.2f\t%s\n" % (dataDict["L"], self.labelUnitDist))
        self.fileRef.write("Celerity\t\t\t%8.2f\t%s/s\n" % (dataDict["C"], self.labelUnitDist))
        self.fileRef.write("Group speed\t\t\t%8.2f\t%s/s\n" % (dataDict["Cg"], self.labelUnitDist))
        self.fileRef.write("Energy density\t\t\t%8.2f\t%s-%s/%s^2\n" %\
            (dataDict["E"], self.labelUnitWt, self.labelUnitDist, self.labelUnitDist))
        self.fileRef.write("Energy flux\t\t\t%8.2f\t%s-%s/%s-s\n" %\
            (dataDict["Ef"], self.labelUnitWt, self.labelUnitDist, self.labelUnitDist))
        self.fileRef.write("Ursell number\t\t\t%8.2f\n" % dataDict["Ur"])
        self.fileRef.write("Water Surface Elevation\t\t%8.2f\t%s\n" %\
            (dataDict["eta"], self.labelUnitDist))
        self.fileRef.write("Horz. displacement\t\t%8.2f\t%s\n" % (dataDict["px"], self.labelUnitDist))
        self.fileRef.write("Vert. displacement\t\t%8.2f\t%s\n" % (dataDict["py"], self.labelUnitDist))
        self.fileRef.write("Horz. velocity\t\t\t%8.2f\t%s/s\n" % (dataDict["u"], self.labelUnitDist))
        self.fileRef.write("Vert. velocity\t\t\t%8.2f\t%s/s\n" % (dataDict["w"], self.labelUnitDist))
        self.fileRef.write("Horz. acceleration\t\t%8.2f\t%s/s^2\n" %\
            (dataDict["dudt"], self.labelUnitDist))
        self.fileRef.write("Vert. acceleration\t\t%8.2f\t%s/s^2\n" %\
            (dataDict["dwdt"], self.labelUnitDist))
        self.fileRef.write("Pressure\t\t\t%8.2f\t%s/%s^2\n" %\
            (dataDict["pres"], self.labelUnitWt, self.labelUnitDist))
    # end fileOutputWriteData

    def performPlot(self):
        pass
    # end performPlot


driver = LinearWaveTheory()
