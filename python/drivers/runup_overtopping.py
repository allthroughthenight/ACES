import sys
import math
import numpy as np
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK2 import ERRWAVBRK2
from LWTDWS import LWTDWS
from LWTGEN import LWTGEN
from QOVERT import QOVERT
from QOVERT_IRR import QOVERT_IRR
from RUNUPR import RUNUPR
from RUNUPS import RUNUPS
from WAVELEN import WAVELEN

#check for option 3, vert wall
## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Wave Runup and Overtopping on Impermeable Structures (page 5-2
# in ACES User's Guide). Provides estimates of wave runup and overtopping
# on rough and smooth slope structures that are assumed to be impermeable

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 18, 2011
# Date Verified: June 6, 2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK2
# LWTDWS
# LWTGEN
# QOVERT
# QOVERT_IRR
# RUNUPR
# RUNUPS
# WAVELEN

# MAIN VARIABLE LIST:
#   MANDATORY INPUT
#   H: incident wave height (Hs for irregular waves)
#   T: wave period (Tp for irregular waves)
#   cotphi: cotan of nearshore slope
#   ds: water depth at structure toe
#   cottheta: cotan of structure slope (0.0 for vertical walls)
#   hs: structure height above toe

#   OPTIONAL INPUT
#   a: empirical coefficient for rough slope runup
#   b: empirical coefficeint for rough slope runup
#   alpha: empirical coefficient for overtopping
#   Qstar0: empiricial coefficient for overtopping
#   U: onshore wind velocity for overtoppping
#   R: wave runup (if known)

#   MANDATORY OUTPUT
#   H0: deepwater wave height
#   relht0: deepwater realtive height (d / H)
#   steep0: deepwater wave steepness

#   OPTIONAL OUTPUT
#   R: wave runup
#   Q: overtopping

#   OTHERS
#   freeb: freeboard
#-------------------------------------------------------------

class RunupOvertopping(BaseDriver):
    def __init__(self, H = None, T = None, cotphi = None,\
        ds = None, cottheta = None, hs = None):
        if H != None:
            self.isSingleCase = True
            self.defaultValueH = H
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if cotphi != None:
            self.isSingleCase = True
            self.defaultValue_cotphi = cotphi
        if ds != None:
            self.isSingleCase = True
            self.defaultValue_ds = ds
        if cottheta != None:
            self.isSingleCase = True
            self.defaultValue_cottheta = cottheta
        if hs != None:
            self.isSingleCase = True
            self.defaultValue_hs = hs

        self.conversionKnots2mph = 1.15077945 #1 knots = 1.15077945 mph

        super(RunupOvertopping, self).__init__()
    # end __init__

    def userInput(self):
        print('%s \n\n' % 'Calculation and slope type options: ')
        print('%s \n' % 'Monochromatic Waves')
        print('%s \n' % '[1] Rough <------------- Runup -------------> [2] Smooth')
        print('%s \n' % '[3] Rough <----------- Overtopping ---------> [4] Smooth')
        print('%s \n\n' % '[5] Rough <----- Runup and Overtopping -----> [6] Smooth')
        print('%s \n' % 'Irregular Waves')
        print('%s \n\n' % '[7] Rough <----- Runup and Overtopping -----> [8] Smooth')

        self.option = USER_INPUT.FINITE_CHOICE("Select option (1 - 8): ",\
            ["1", "2", "3", "4", "5", "6", "7", "8"])
        self.option = int(self.option)

        self.has_rough_slope = self.option == 1 or\
            self.option == 5 or self.option == 7 or self.option == 8
        self.has_overtopping = self.option > 2
        self.has_runup = self.option != 3 and self.option != 4

        if self.option == 3:
            R_default = 15.0
        elif self.option == 4:
            R_default = 20.0
        else:
            R_default = 0.0

        super(RunupOvertopping, self).userInput()

        print(self.inputList)
        # self.roughSlopeCoeffDict = {"a": 0.956, "b": 0.398,\
        #     "alpha": 0.076473, "Qstar0": 0.025, "U": 35.0, "R": R_default}
        if self.option != 2:
            self.roughSlopeCoeffDict = USER_INPUT.ROUGH_SLOPE_COEFFICIENTS(\
                self.has_rough_slope, self.has_overtopping, self.has_runup,\
                {"numCases": len(self.dataOutputList), "R_default": R_default})
        else:
            self.roughSlopeCoeffDict = {}
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField("H: incident wave height (Hs for irregular waves) (%s)" %\
                (self.labelUnitDist), 0.1, 100.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField("T: wave period (Tp for irregular waves) (s)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_cotphi"):
            self.inputList.append(BaseField("cotphi: cotan of nearshore slope", 5.0, 10000.0))
        if not hasattr(self, "defaultValue_ds"):
            self.inputList.append(BaseField("ds: water depth at structure toe (%s)" %\
                self.labelUnitDist, 0.1, 200.0))
        if not hasattr(self, "defaultValue_cottheta"):
            self.inputList.append(BaseField("cottheta: cotan of structure slope (0.0 for vertical walls)",\
                0.0, 30.0))
        if not hasattr(self, "defaultValue_hs"):
            self.inputList.append(BaseField("hs: structure height above toe (%s)" % self.labelUnitDist,\
                0.0, 200.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "runup_overtopping")

    def getCalcValues(self, caseInputList, caseIndex):
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

        if hasattr(self, "defaultValue_cotphi"):
            cotphi = self.defaultValue_cotphi
        else:
            cotphi = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ds"):
            ds = self.defaultValue_ds
        else:
            ds = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cottheta"):
            cottheta = self.defaultValue_cottheta
        else:
            cottheta = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_hs"):
            hs = self.defaultValue_hs
        else:
            hs = caseInputList[currIndex]

        print(self.roughSlopeCoeffDict)

        coeffDict = {}
        for coeffName in ["a", "b", "alpha", "Qstar0", "U", "R"]:
            if coeffName in self.roughSlopeCoeffDict:
                coeffDict[coeffName] = self.roughSlopeCoeffDict[coeffName]
            elif (coeffName + "List") in self.roughSlopeCoeffDict:
                coeffDict[coeffName] =\
                    self.roughSlopeCoeffDict[coeffName + "List"][caseIndex]
            else:
                coeffDict[coeffName] = None

        return H, T, cotphi, ds, cottheta, hs,\
            coeffDict["a"],\
            coeffDict["b"],\
            coeffDict["alpha"],\
            coeffDict["Qstar0"],\
            coeffDict["U"],\
            coeffDict["R"]
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, cotphi, ds, cottheta, hs, a, b, alpha, Qstar0, U, R =\
            self.getCalcValues(caseInputList, caseIndex)

        m = 1.0/cotphi

        if not (ds < hs):
            print("Error: Method does not apply to submerged structures.")
            return

        Hbs = ERRWAVBRK2(T, m, ds)
        if not (H < Hbs):
            print("Error: Wave broken at structure (Hbs = %6.2f %s)" %\
                (Hbs, self.labelUnitDist))
            return

        c, c0, cg, cg0, k, L, L0, reldep = LWTGEN(ds, T, self.g)

        steep, maxstp = ERRSTP(H, ds, L)
        if not (steep < maxstp):
            print("Error: Input wave unstable (Max: %0.4f. [H/L] = %0.4f" %\
                (maxstp, steep))
            return

        alpha0, H0 = LWTDWS(0.0, c, cg, c0, H)

        relht0 = ds/H0
        steep0 = H0 / (self.g * T**2)

        if np.isclose(cottheta, 0):
            if not (self.option != 1):
                print("Error: Vertical wall cannot have rough slope.")
                return

            theta = 0.5*math.pi
            ssp = 1000
        else:
            theta = math.atan(1.0/cottheta)
            ssp = (1.0/cottheta)/math.sqrt(H/L0)
        # end if

        print("Deepwater")
        print("\tWave height, Hs0\t\t%-6.3f %s" % (H0, self.labelUnitDist))
        print("\tRelative height, ds/H0\t\t%-6.3f" % relht0)
        print("\tWave steepness, Hs0/(gT^2)\t%-6.6f" % steep0)

        freeb = hs - ds

        dataDict = {"H": H, "T": T, "cotphi": cotphi, "ds": ds,\
            "cottheta": cottheta, "hs": hs, "a": a, "b": b,\
            "alpha": alpha, "Qstar0": Qstar0, "U": U, "H0": H0,\
            "relht0": relht0, "steep0": steep0}

        if self.option == 1:
            R = RUNUPR(H, ssp, a, b)
        elif self.option == 2:
            R = RUNUPS(H, L, ds, theta, ssp)
        elif self.option == 3:
            Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, self.g)
        elif self.option == 4:
            Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, self.g)
        elif self.option == 5:
            R = RUNUPR(H, ssp, a, b)
            Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, self.g)
        elif self.option == 6:
            R = RUNUPS(H, L, ds, theta, ssp)
            Q = QOVERT(H0, freeb, R, Qstar0, alpha, theta, U, self.g)
        elif self.option == 7:
            R = RUNUPR(H, ssp, a, b)
            Q = QOVERT_IRR(H0, freeb, R, Qstar0, alpha, theta, U, self.g)
        elif self.option == 8:
            R = RUNUPS(H, L, ds, theta, ssp)
            Q = QOVERT_IRR(H0, freeb, R, Qstar0, alpha, theta, U, self.g)

        if self.option == 1 or self.option == 2 or\
            self.option == 5 or self.option == 6 or\
            self.option == 7 or self.option == 8:
            print("Runup\t\t\t\t\t%-6.3f %s" % (R, self.labelUnitDist))
        if self.option == 3 or self.option == 4 or\
            self.option == 5 or self.option == 6 or\
            self.option == 7 or self.option == 8:
            print("Overtopping rate per unit width\t\t%-6.3f %s^3/sec-%s" %\
                (Q, self.labelUnitDist, self.labelUnitDist))
            dataDict["Q"] = Q

        dataDict["R"] = R
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("H\t\t%6.2f %s\n" %\
            (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("T\t\t%6.2f s\n" % dataDict["T"])
        self.fileRef.write("cotphi\t\t%6.2f\n" % dataDict["cotphi"])
        self.fileRef.write("ds\t\t%6.2f %s\n" %\
            (dataDict["ds"], self.labelUnitDist))
        self.fileRef.write("cottheta\t%6.2f\n" % dataDict["cottheta"])
        self.fileRef.write("hs\t\t%6.2f %s\n" %\
            (dataDict["hs"], self.labelUnitDist))

        if "a" in dataDict and dataDict["a"] != None:
            self.fileRef.write("a\t\t%6.4f\n" % dataDict["a"])
        if "b" in dataDict and dataDict["b"] != None:
            self.fileRef.write("b\t\t%6.4f\n" % dataDict["b"])
        if "alpha" in dataDict and dataDict["alpha"] != None:
            self.fileRef.write("alpha\t\t%6.4f\n" % dataDict["alpha"])
        if "Qstar0" in dataDict and dataDict["Qstar0"] != None:
            self.fileRef.write("Qstar0\t\t%6.4f\n" % dataDict["Qstar0"])
        if "U" in dataDict and dataDict["U"] != None:
            self.fileRef.write("U\t\t%6.4f kn\n" %\
                (dataDict["U"]/self.conversionKnots2mph))
        if "R" in dataDict and dataDict["R"] != None and not self.has_runup:
            self.fileRef.write("R\t\t%6.4f %s\n" %\
                (dataDict["R"], self.labelUnitDist))

        self.fileRef.write("\nDeepwater\n")
        self.fileRef.write("\tWave height, Hs0\t\t%-6.3f %s\n" %\
            (dataDict["H0"], self.labelUnitDist))
        self.fileRef.write("\tRelative height, ds/H0\t\t%-6.3f\n" %\
            dataDict["relht0"])
        self.fileRef.write("\tWave steepness, Hs0/(gT^2)\t%-6.6f\n" %\
            dataDict["steep0"])

        if self.option == 1 or self.option == 2 or\
            self.option == 5 or self.option == 6 or\
            self.option == 7 or self.option == 8:
            self.fileRef.write("Runup\t\t\t\t\t%-6.3f %s\n" %\
                (dataDict["R"], self.labelUnitDist))
        if self.option == 3 or self.option == 4 or\
            self.option == 5 or self.option == 6 or\
            self.option == 7 or self.option == 8:
            self.fileRef.write("Overtopping rate per unit width\t\t%-6.3f %s^3/sec-%s\n" %\
                (dataDict["Q"], self.labelUnitDist, self.labelUnitDist))
    # end fileOutputWriteData


driver = RunupOvertopping()