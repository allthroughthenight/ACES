import math
import sys
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK2 import ERRWAVBRK2
from WAVELEN import WAVELEN

## ACES Update to python
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Driver for Toe Protection Design (page 4 - 2 in ACES User's Guide).
# Determines armor stone size and width of a toe protection apron for
# vertical structures, such as seawalls, bulkheads, quay walls, breakwaters,
# and groins.

# Updated by: Mary Anderson, USACE - CHL - Coastal Processes Branch
# Date Created: April 13, 2011
# Date Verified: June 5, 2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK2
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   Hi: wave height (m)
#   T: wave period (sec)
#   ds: water depth at structure (m)
#   cotphi: cotangent of nearshore slope
#   Kp: passive earth pressure coefficient
#   de: sheet - pile penetration depth (m)
#   ht: height of toe protection layer above mudline
#   unitwt: unit weight of rock (N / m^3)

#   OUTPUT
#   width: width of toe protection apron (m)
#   w: weight of individual armor unit (N)
#   dt: water depth at top of toe protection layer (m)

#   OTHERS
#   H20weight: specific weight of water
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

class ToeDesign(BaseDriver):
    def __init__(self, H = None, T = None, ds = None, cotphi = None,\
        Kp = None, de = None, ht = None, unitwt = None):
        if H != None:
            self.isSingleCase = True
            self.defaultValueH = H
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if ds != None:
            self.isSingleCase = True
            self.defaultValue_ds = ds
        if cotphi != None:
            self.isSingleCase = True
            self.defaultValue_cotphi = cotphi
        if Kp != None:
            self.isSingleCase = True
            self.defaultValueKp = Kp
        if de != None:
            self.isSingleCase = True
            self.defaultValue_de = de
        if ht != None:
            self.isSingleCase = True
            self.defaultValue_ht = ht
        if unitwt != None:
            self.isSingleCase = True
            self.defaultValue_unitwt = unitwt

        super(ToeDesign, self).__init__()
    # end __init__

    def userInput(self):
        super(ToeDesign, self).userInput()

        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField(\
                "Hi: wave height (%s)" % (self.labelUnitDist), 0.1, 100.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField(\
                "T: wave period (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_ds"):
            self.inputList.append(BaseField(\
                "ds: water depth at structure (%s)" % (self.labelUnitDist), 0.1, 200.0))
        if not hasattr(self, "defaultValue_cotphi"):
            self.inputList.append(BaseField(\
                "cotphi: cotangent of nearshore slope", 5.0, 10000.0))
        if not hasattr(self, "defaultValueKp"):
            self.inputList.append(BaseField(\
                "Kp: passive earth pressure coefficient", 0.0, 50.0))
        if not hasattr(self, "defaultValue_de"):
            self.inputList.append(BaseField(\
                "de: sheet-pile penetration depth (%s)" % (self.labelUnitDist), 0.0, 200.0))
        if not hasattr(self, "defaultValue_ht"):
            self.inputList.append(BaseField(\
                "ht: height of toe protection layer above mudline (%s)" % (self.labelUnitDist), 0.1, 200.0))
        if not hasattr(self, "defaultValue_unitwt"):
            self.inputList.append(BaseField(\
                "unitwt: unit weight of rock (%s/%s^3)" % (self.labelUnitWt, self.labelUnitDist), 1.0, 99999.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "toe_design")

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

        if hasattr(self, "defaultValue_ds"):
            ds = self.defaultValue_ds
        else:
            ds = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotphi"):
            cotphi = self.defaultValue_cotphi
        else:
            cotphi = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueKp"):
            Kp = self.defaultValueKp
        else:
            Kp = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_de"):
            de = self.defaultValue_de
        else:
            de = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ht"):
            ht = self.defaultValue_ht
        else:
            ht = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_unitwt"):
            unitwt = self.defaultValue_unitwt
        else:
            unitwt = caseInputList[currIndex]

        return H, T, ds, cotphi, Kp, de, ht, unitwt
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, ds, cotphi, Kp, de, ht, unitwt =\
            self.getCalcValues(caseInputList)

        H20weight = self.g * self.rho

        specgrav = unitwt / H20weight

        dl = ds - ht
        m = 1.0 / cotphi

        if not (ds / (T**2) > 0.0037424):
            print("Error: Limiting value detected...Hbs cannot be solved.")
            return

        Hbs = ERRWAVBRK2(T, m, ds)
        if not (H < Hbs):
            print("Error: Wave broken at structure (Hbs = %6.2f %s" %\
                (Hbs, self.labelUnitDist))

        L, k = WAVELEN(dl, T, 50, self.g)

        steep, maxstp = ERRSTP(H, dl, L)
        if not (steep < maxstp):
            print("Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f" % (maxstp, steeps))

        b1 = de*Kp
        b2 = 2.0*H
        b3 = 0.4*ds
        b = [1.0, b1, b2, b3]
        b = max(b)

        arg1 = (4.0*math.pi*dl/L)
        kappa = (arg1/math.sinh(arg1))*((math.sin(2.0*math.pi*b/L))**2)
        arg2 = ((1.0 - kappa)/(kappa**(1.0/3.0)))*(dl/H)
        Ns = 1.3*arg2 + 1.8*math.exp(-1.5*(1.0 - kappa)*arg2)

        Ns = max(Ns, 1.8)

        w = (unitwt*(H**3))/((Ns**3)*((specgrav - 1.0)**3))

        print("\nWidth of toe apron\t\t%6.2f %s" %\
            (b, self.labelUnitDist))
        print("Weight of individual armor unit\t%6.2f %s" %\
            (w, self.labelUnitWt))
        print("Water depth at top of tow\t%6.2f %s" %\
            (dl, self.labelUnitDist))

        dataDict = {"H": H, "T": T, "ds": ds, "cotphi": cotphi,\
            "Kp": Kp, "de": de, "ht": ht, "unitwt": unitwt,\
            "b": b, "w": w, "dl": dl}
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("H\t\t\t\t%6.2f %s\n" %\
            (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("T\t\t\t\t%6.2f s\n" % dataDict["T"])
        self.fileRef.write("ds\t\t\t\t%6.2f %s\n" %\
            (dataDict["ds"], self.labelUnitDist))
        self.fileRef.write("cotphi\t\t\t\t%6.2f\n" % dataDict["cotphi"])
        self.fileRef.write("Kp\t\t\t\t%6.2f\n" % dataDict["Kp"])
        self.fileRef.write("de\t\t\t\t%6.2f %s\n" %\
            (dataDict["de"], self.labelUnitDist))
        self.fileRef.write("ht\t\t\t\t%6.2f %s\n" %\
            (dataDict["ht"], self.labelUnitDist))
        self.fileRef.write("unitwt\t\t\t\t%6.2f %s/%s^3\n" %\
            (dataDict["unitwt"], self.labelUnitWt, self.labelUnitDist))

        self.fileRef.write("\nWidth of toe apron\t\t%6.2f %s\n" %\
            (dataDict["b"], self.labelUnitDist))
        self.fileRef.write("Weight of individual armor unit\t%6.2f %s\n" %\
            (dataDict["w"], self.labelUnitWt))
        self.fileRef.write("Water depth at top of tow\t%6.2f %s\n" %\
            (dataDict["dl"], self.labelUnitDist))
    # end fileOutputWriteData


driver = ToeDesign()