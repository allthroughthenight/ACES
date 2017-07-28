import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT

from ERRSTP import ERRSTP
from ERRWAVBRK2 import ERRWAVBRK2
from HTP import HTP
from LWTGEN import LWTGEN
from RUNUPR import RUNUPR
from RUNUPS import RUNUPS
from VERTKT import VERTKT

from EXPORTER import EXPORTER

## ACES Update to Python
#-------------------------------------------------------------
# Driver for Wave Transmission on Impermeable Structures (page 5-3 in ACES
# User's Guide). Provides estimates of wave runup and transmission on rough
# and smooth slope structures. It also addresses wave transmission over
# impermeable vertical walls and composite structures.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 19, 2011
# Date Verified: June 6, 2012 

# Requires the following functions:
# ERRSTP
# ERRWAVBRK2
# HTP
# LWTGEN
# RUNUPR
# RUNUPS
# VERTKT
# WAVELEN

# MAIN VARIABLE LIST:
#   MANDATORY INPUT
#   H: incident wave height (Hs for irregular waves)
#   T: wave period (Tp for irregular waves)
#   cotphi: cotan of nearshore slope
#   ds: water depth at structure toe
#   hs: structure height above toe 
#   wth: structure crest width
#   cottheta: cotan of structure slope (0.0 for vertical wall)

#   OPTIONAL INPUT
#   a: empirical coefficient for rough slope runup
#   b: empirical coefficeint for rough slope runup
#   R: wave runup (if known)
#   hB: toe protection or composite breakwater berm height above structure
#   toe

#   MANDATORY OUTPUT
#   Ht: transmitted wave height

#   OPTIONAL OUTPUT
#   R: wave runup

#   OTHERS
#   freeb: freeboard
#-------------------------------------------------------------

class WavetransImperm(BaseDriver):
    def __init__(self, H = None, T = None, cotphi = None, ds = None,\
            cottheta = None, hs = None, B = None, R = None, hB = None):
        self.exporter = EXPORTER("output/exportWavetransImperm.txt")

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

        if B != None:
            self.isSingleCase = True
            self.defaultValueB = B

        if R != None:
            self.isSingleCase = True
            self.defaultValueR = R

        if hB != None:
            self.isSingleCase = True
            self.defaultValue_hB = hB

        super(WavetransImperm, self).__init__()
        
        self.exporter.close()
    # end __init__

    def userInput(self):
        msg = "Calculation and slope type options:\n" +\
            "[1] Wave transmission only for smooth slope\n" +\
            "[2] Wave transmission only for vertical wall\n" +\
            "[3] Wave runup and transmission for rough slope\n" + \
            "[4] Wave runup and transmission for smooth slope\n" +\
            "Select option: "
        self.option = USER_INPUT.FINITE_CHOICE(msg, ["1", "2", "3", "4"])
        self.option = int(self.option)

        super(WavetransImperm, self).userInput()

        if self.option == 3:
            runupCoeffDataList = [\
                ['Riprap', 0.956, 0.398],\
                ['Quarrystone (Impermeable Base)', 0.692, 0.504],\
                ['Quarrystone (Permeable Base)', 0.775, 0.361],\
                ['Modified Cubes', 0.95, 0.69],\
                ['Tetrapods', 1.01, 0.91],\
                ['Quadrapods', 0.59, 0.35],\
                ['Hexapods', 0.82, 0.63],\
                ['Tribars', 1.81, 1.57],\
                ['Dolosse', 0.988, 0.703]]

            numOptions = len(runupCoeffDataList) + 1
            print("Suggested Empirical Rough Slope Runup Coeff Listing")
            for i in range(len(runupCoeffDataList)):
                print("[%d] %s\t%-6.3f\t%-6.3f" %\
                    (i + 1, runupCoeffDataList[i][0],\
                    runupCoeffDataList[i][1], runupCoeffDataList[i][2]))
            print("[%d] Enter custom values" % (numOptions))

            coeffChoice = USER_INPUT.FINITE_CHOICE("Select option: ",\
                [str(i + 1) for i in range(numOptions)])
            coeffChoice = int(coeffChoice)

            if coeffChoice == numOptions:
                self.a = USER_INPUT.DATA_VALUE("coefficient a", 0.0, 20.0)
                self.b = USER_INPUT.DATA_VALUE("coefficient b", 0.0, 20.0)
            else:
                self.a = runupCoeffDataList[coeffChoice - 1][1]
                self.b = runupCoeffDataList[coeffChoice - 1][2]
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField(\
                "H: incident wave height (Hs for irregular waves) (%s)" % (self.labelUnitDist),\
                0.1, 100.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField(\
                "T: wave period (Tp for irregular waves) (s)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_cotphi"):
            self.inputList.append(BaseField(\
                "cotphi: cotan of nearshore slope", 5.0, 10000.0))
        if not hasattr(self, "defaultValue_ds"):
            self.inputList.append(BaseField(\
                "ds: water depth at structure toe (%s)" % (self.labelUnitDist), 0.1, 200.0))

        if self.option != 2 and not hasattr(self, "defaultValue_cottheta"):
            self.inputList.append(BaseField(\
                "cottheta: cotan of structure slope (0.0 for vertical wall)", 0.0, 30.0))

        if not hasattr(self, "defaultValue_hs"):
            self.inputList.append(BaseField(\
                "hs: structure height above toe (%s)" % (self.labelUnitDist), 0.0, 200.0))
        if not hasattr(self, "defaultValueB"):
            self.inputList.append(BaseField(\
                "B: structure crest width (%s)" % (self.labelUnitDist), 0.0, 200.0))

        if self.option == 1 and not hasattr(self, "defaultValueR"):
            self.inputList.append(BaseField(\
                "R: wave runup (if known) (%s)" % (self.labelUnitDist), 0.0, 100.0))

        if self.option == 2 and not hasattr(self, "defaultValue_hB"):
            self.inputList.append(BaseField(\
                "hB: structure berm height above toe (%s)" % (self.labelUnitDist),\
                0.0, 200.0))
    # end defineInputDataList

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

        if self.option != 2:
            if hasattr(self, "defaultValue_cottheta"):
                cottheta = self.defaultValue_cottheta
            else:
                cottheta = caseInputList[currIndex]
                currIndex = currIndex + 1
        else:
            cottheta = 0

        if hasattr(self, "defaultValue_hs"):
            hs = self.defaultValue_hs
        else:
            hs = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueB"):
            B = self.defaultValueB
        else:
            B = caseInputList[currIndex]
            currIndex = currIndex + 1

        if self.option == 1:
            if hasattr(self, "defaultValueR"):
                R = self.defaultValueR
            else:
                R = caseInputList[currIndex]
                currIndex = currIndex + 1
        else:
            R = None

        if self.option == 2:
            if hasattr(self, "defaultValue_hB"):
                hB = self.defaultValue_hB
            else:
                hB = caseInputList[currIndex]
                currIndex = currIndex + 1
        else:
            hB = None

        return H, T, cotphi, ds, cottheta, hs, B, R, hB
    # end getCalcValues

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "wavetrans_imperm")

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, cotphi, ds, cottheta, hs, B, R, hB = self.getCalcValues(caseInputList)
        dataDict = {"H": H, "T": T, "cotphi": cotphi, "ds": ds,\
            "cottheta": cottheta, "hs": hs, "B": B, "R": R, "hB": hB}
        m = 1.0/cotphi

        if self.option != 2 and not (ds < hs):
            self.errorMsg = "Error: Method does not apply to submerged structures."
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        c, c0, cg, cg0, k, L, L0, reldep = LWTGEN(ds, T, self.g)

        Hbs = ERRWAVBRK2(T, m, ds)
        if not (H < Hbs):
            self.errorMsg = "Error: Wave broken at structure (Hbs = %6.2f %s" %\
                (Hbs, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        steep, maxstp = ERRSTP(H, ds, L)
        if not (steep < maxstp):
            self.errorMsg = "Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)" % (maxstp, steep)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        if cottheta == 0:
            if self.option != 2:
                self.errorMsg = "Error: A cotangent of zero indicates a vertical wall."
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            reldep = ds / L

            if not (reldep > 0.14 and reldep < 0.5):
                self.errorMsg = "Error: d/L conditions exceeded - 0.14 <= (d/L) <= 0.5"
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return
        else:
            theta = math.atan(1/cottheta)
            ssp = (1/cottheta)/math.sqrt(H/L0)

        if self.option == 3:
            R = RUNUPR(H, ssp, self.a, self.b)
            print("Runup\t\t%-6.3f" % R)
        elif self.option == 4:
            R = RUNUPS(H, L, ds, theta, ssp)
            print("Runup\t\t%-6.3f" % R)

        freeb = hs - ds

        if self.option != 2:
            Ht = HTP(B, hs, R, H, freeb)
        else:
            dl = ds - hB
            Ht = VERTKT(H, freeb, B, ds, dl)
        print("Transmitted wave height\t%-6.3f" % Ht)

        dataDict.update({"R": R, "Ht": Ht})
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("H\t\t%6.2f %s\n" % (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("T\t\t%6.2f %s\n" % (dataDict["T"], self.labelUnitDist))
        self.fileRef.write("cotphi\t\t%6.2f\n" % (dataDict["cotphi"]))
        self.fileRef.write("ds\t\t%6.2f %s\n" % (dataDict["ds"], self.labelUnitDist))
        self.fileRef.write("cottheta\t%6.2f\n" % (dataDict["cottheta"]))
        self.fileRef.write("hs\t\t%6.2f %s\n" % (dataDict["hs"], self.labelUnitDist))
        self.fileRef.write("B\t\t%6.2f %s\n" % (dataDict["B"], self.labelUnitDist))

        if self.option == 1:
            self.fileRef.write("R\t\t%6.2f %s\n" % (dataDict["R"], self.labelUnitDist))

        if self.option == 2:
            self.fileRef.write("hB\t\t%6.2f %s\n" % (dataDict["hB"], self.labelUnitDist))

        if self.option == 3:
            self.fileRef.write("a\t\t%6.3f\n" % (self.a))
            self.fileRef.write("b\t\t%6.3f\n" % (self.b))

        self.fileRef.write("\n")

        if self.errorMsg != None:
            self.fileRef.write("%s\n" % self.errorMsg)
        else:
            if self.option == 3 or self.option == 4:
                self.fileRef.write("Runup\t\t%6.3f\n" % dataDict["R"])
    
            self.fileRef.write("Transmitted wave height\t%-6.3f %s\n" %\
                (dataDict["Ht"], self.labelUnitDist))
        
        exportData = [dataDict["H"], dataDict["T"], dataDict["cotphi"],\
            dataDict["ds"], dataDict["cottheta"], dataDict["hs"],\
            dataDict["B"]]
        if self.option == 1:
            exportData.append(dataDict["R"])
        if self.option == 2:
            exportData.append(dataDict["hB"])
        if self.option == 3:
            exportData.append(self.a)
            exportData.append(self.b)
        
        if self.errorMsg != None:
            exportData.append("Error")
        else:
            if self.option == 3 or self.option == 4:
                exportData.append(dataDict["R"])
            exportData.append(dataDict["Ht"])
        self.exporter.writeData(exportData)
    # end fileOutputWriteData


driver = WavetransImperm()