import sys
import math
import numpy as np
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK1 import ERRWAVBRK1
from ERRWAVBRK2 import ERRWAVBRK2
from MADSEELG import MADSEELG
from WAVELEN import WAVELEN

from EXPORTER import EXPORTER

## ACES Update to Python
#-------------------------------------------------------------
# Driver for Wave Transmission on Permeable Structures (page 5-4 in ACES
# User's Guide). Determines wave transmission coefficients and transmitted
# wave heights for permeable breakwaters with crest elevations at or
# above the still-water level.

# Updated by: Yaprak Onat
# Date Created: June 21, 2016
# Date Modified:

#Requires English units

# Requires the following functions:
# ERRSTP
# ERRWAVBRK1
# EQBWLE
# EQBWTRCO
# MADSEELG
# MADSN1
# MADSN2
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   H: incident wave height
#   T: wave period
#   ds: water depth at structure toe
#   nummat: number of materials comprising the breakwater
#   d50: mean diameter of each material
#   p: porosity of each material
#   hs: structure height above toe
#   cotnssl: cotan of nearshore slope
#   b: structure crest width
#   cottheta: cotangent of structure slope
#   numlay: number of horizontal layers in the breakwater
#   th: thickness of each horizontal layer
#   hlen: horizontal length of each matertial in each layer

#   OUTPUT
#   Kr: wave reflection coefficient
#   KTt: wave transmission coefficient - through
#   KTo: wave transmission coefficient - overtopping
#   KT: wave transmission coefficient - total
#   Ht: transmitted wave height

#   OTHERS
#   freeb: freeboard
#-------------------------------------------------------------

class WavetransPerm(BaseDriver):
    def __init__(self, H = None, T = None, ds = None, d50 = None,\
        por = None, hs = None, cottheta = None, b = None,\
        th = None, hlen = None):
        self.exporter = EXPORTER("output/exportWavetransPerm")

        if H != None:
            self.isSingleCase = True
            self.defaultValueH = H
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if ds != None:
            self.defaultValue_ds = ds
        if d50 != None:
            self.defaultValue_d50 = d50
        if por != None:
            self.defaultValue_por = por
        if hs != None:
            self.defaultValue_hs = hs
        if cottheta != None:
            self.defaultValue_cottheta = cottheta
        if b != None:
            self.defaultValue_b = b
        if th != None:
            self.defaultValue_th = th
        if hlen != None:
            self.defaultValue_hlen = hlen

        super(WavetransPerm, self).__init__()
        
        self.exporter.close()
    # end __init__

    def userInput(self):
        super(WavetransPerm, self).userInput()

        if hasattr(self, "defaultValue_ds"):
            self.ds = self.defaultValue_ds
        else:
            self.ds = USER_INPUT.DATA_VALUE(\
                "ds: water depth at structure toe (%s)" %\
                self.labelUnitDist, 0.1, 200.0)

        # define NM and NL if any relevant defaults are used
        if hasattr(self, "defaultValue_d50"):
            self.d50 = self.defaultValue_d50
            self.NM = len(self.d50)

        if hasattr(self, "defaultValue_por"):
            self.por = self.defaultValue_por
            self.NM = len(self.por)

        if hasattr(self, "defaultValue_th"):
            self.th = self.defaultValue_th
            self.NL = len(self.th)

        if hasattr(self, "defaultValue_hlen"):
            self.hlen = self.defaultValue_hlen
            self.NM = len(self.hlen)
            self.NL = len(self.hlen[0])

        if not hasattr(self, "NM"):
            self.NM = USER_INPUT.DATA_VALUE(\
                "NM: number of materials comprising the breakwater", 1, 4)
            self.NM = int(self.NM)

        if not hasattr(self, "d50"):
            self.d50 = []
            for i in range(self.NM):
                self.d50.append(USER_INPUT.DATA_VALUE(\
                    "d50: mean diameter of material #%d (%s)" %\
                    ((i + 1), self.labelUnitDist), 0.05, 99.0))

        if not hasattr(self, "defaultValue_por"):
            self.por = []
            for i in range(self.NM):
                self.por.append(USER_INPUT.DATA_VALUE(\
                    "p: porosity of material #%d (%%)" % (i + 1), 0.0, 100.0))
            self.por = [i / 100.0 for i in self.por]

        if not hasattr(self, "defaultValue_hs"):
            self.hs = USER_INPUT.DATA_VALUE(\
                "hs: structure height above toe (%s)" %\
                self.labelUnitDist, 0.1, 200.0)
        else:
            self.hs = self.defaultValue_hs

        if not hasattr(self, "defaultValue_cottheta"):
            self.cottheta = USER_INPUT.DATA_VALUE(\
                "cottheta: cotangent of structure slope", 1.0, 5.0)
        else:
            self.cottheta = self.defaultValue_cottheta

        if not hasattr(self, "defaultValue_b"):
            self.b = USER_INPUT.DATA_VALUE(\
                "b: structure crest width (%s)" % self.labelUnitDist, 0.1, 200.0)
        else:
            self.b = self.defaultValue_b

        if not hasattr(self, "NL"):
            self.NL = USER_INPUT.DATA_VALUE(\
                "NL: number of horizontal layers in the breakwater", 1, 4)
            self.NL = int(self.NL)

        if not hasattr(self, "th"):
            self.th = []
            for i in range(self.NL):
                self.th.append(USER_INPUT.DATA_VALUE(\
                    "th: thickness of horizontal layer #%d (%s)" %\
                    ((i + 1), self.labelUnitDist), 0.1, 200.0))

        if not hasattr(self, "hlen"):
            self.hlen = []
            for i in range(self.NM):
                self.hlen.append([])

                for j in range(self.NL):
                    self.hlen[i].append(USER_INPUT.DATA_VALUE(\
                        "hlen: horizontal length of material #%d in layer #%d (%s)" %\
                        ((i + 1), (j + 1), self.labelUnitDist), 0.0, 200.0))


        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField(\
                "H: incident wave height (%s)" % self.labelUnitDist, 0.1, 100.0))

        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField("T: wave period (s)", 1.0, 1000.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "wavetrans_perm")

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

        return H, T, self.ds, self.d50, self.por, self.hs,\
            self.cottheta, self.b, self.th, self.hlen
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, ds, d50, por, hs, cottheta, b, th, hlen =\
            self.getCalcValues(caseInputList)
        dataDict = {"H": H, "T": T, "ds": ds, "d50": d50, "por": por,\
            "hs": hs, "cottheta": cottheta, "b": b, "th": th,\
            "hlen": hlen}
        
        if not self.isMetric:
            if self.water == "S" or self.water == "s":
                nu = 14.643223710**(-6) #salt water
            else:
                nu = 0.0000141 #ft^2/s KINEMATIC VISCOSITY OF THE WATER AT 50 DEGREES FAHRENHEIT
        else:
            if self.water == "S" or self.water == "s":
                nu = 1.3604*10**(-6) # salt water
            else:
                nu = 1.307*10**(-6) # m^2/s fresh

        Hb = ERRWAVBRK1(ds, 0.78)
        if not (H < Hb):
            self.errorMsg = "Error: Input wave broken (Hb = %6.2f %s)" % (Hb, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        Hbs = ERRWAVBRK2(T, 1.0/cottheta, ds)
        if not (H < Hbs):
            self.errorMsg = "Error: Input wave breaking at toe of the structure (Hbs = %6.2f %s)" % (Hbs, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        L, k = WAVELEN(ds, T, 50, self.g)

        steep, maxstp = ERRSTP(H, ds, L)
        if not (steep < maxstp):
            self.errorMsg = "Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)" %\
                (maxstp, steep)
                
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        if not (ds < hs):
            self.errorMsg = "Error: Method does not apply to submerged structures."
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        if not (np.isclose(sum(th), ds)):
            self.errorMsg = "Error: Water depth must equal sum of all layer thicknesses."
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        KTt, Kto, KT, Kr, Ht, L = MADSEELG(\
            H, T, ds, hs, b, self.NL, th, hlen, self.NM, d50, por, cottheta, nu, self.g)

        print("Reflection coefficient, Kr\t\t%-6.3f" % Kr)
        print("Wave transmission coefficient")
        print("Wave Transmission (Through), KTt\t%-6.3f" % KTt)
        print("Wave Transmission (Overtopping), KTo\t%-6.3f" % Kto)
        print("Wave Transmission (Total), KT\t\t%-6.3f" % KT)
        print("Transmitted wave height, Ht\t\t%-6.2f %s" % (Ht, self.labelUnitDist))

        dataDict.update({"Kr": Kr, "KTt": KTt, "Kto": Kto, "KT": KT, "Ht": Ht})
        self.fileOutputWriteMain(dataDict)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("H\t\t%6.2f %s\n" % (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("T\t\t%6.2f s\n" % dataDict["T"])
        self.fileRef.write("ds\t\t%6.2f %s\n" % (dataDict["ds"], self.labelUnitDist))
        for i in range(len(dataDict["d50"])):
            self.fileRef.write("d50 #%i\t\t%6.2f %s\n" %\
                ((i + 1), dataDict["d50"][i], self.labelUnitDist))
        for i in range(len(dataDict["por"])):
            self.fileRef.write("por #%i\t\t%6.2f%%\n" %\
                ((i + 1), dataDict["por"][i]*100))
        self.fileRef.write("hs\t\t%6.2f %s\n" %\
            (dataDict["hs"], self.labelUnitDist))
        self.fileRef.write("cottheta\t%6.2f\n" % dataDict["cottheta"])
        self.fileRef.write("b\t\t%6.2f %s\n" %\
            (dataDict["b"], self.labelUnitDist))
        for i in range(len(dataDict["th"])):
            self.fileRef.write("th #%d\t\t%6.2f %s\n" %\
                ((i + 1), dataDict["th"][i], self.labelUnitDist))
        for i in range(len(dataDict["hlen"])):
            for j in range(len(dataDict["hlen"][i])):
                self.fileRef.write("Len mat %d,\t%6.2f %s\n" %\
                    ((i + 1), dataDict["hlen"][i][j], self.labelUnitDist))
                self.fileRef.write("  layer %d\n" % (j + 1))

        if self.errorMsg != None:
            self.fileRef.write("\n%s\n" % self.errorMsg)
        else:
            self.fileRef.write("\nReflection coefficient, Kr\t\t%-6.3f\n" %\
                dataDict["Kr"])
            self.fileRef.write("Wave transmission coefficient\n")
            self.fileRef.write("Wave Transmission (Through), KTt\t%-6.3f\n" %\
                dataDict["KTt"])
            self.fileRef.write("Wave Transmission (Overtopping), KTo\t%-6.3f\n" %\
                dataDict["Kto"])
            self.fileRef.write("Wave Transmission (Total), KT\t\t%-6.3f\n" %\
                dataDict["KT"])
            self.fileRef.write("Transmitted wave height, Ht\t\t%-6.2f %s\n" %\
                (dataDict["Ht"], self.labelUnitDist))
        
        exportData = [dataDict["H"], dataDict["T"], dataDict["ds"]] +\
            [i for i in dataDict["d50"]] + [i*100 for i in dataDict["por"]] +\
            [dataDict["hs"], dataDict["cottheta"], dataDict["b"]] +\
            [i for i in dataDict["th"]] +\
            [j for i in dataDict["hlen"] for j in i]
        if self.errorMsg != None:
            exportData.append(self.errorMsg)
        else:
            exportData = exportData + [dataDict["Kr"], dataDict["KTt"],\
                dataDict["Kto"], dataDict["KT"], dataDict["Ht"]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData


driver = WavetransPerm()