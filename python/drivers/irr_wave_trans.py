import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRWAVBRK1 import ERRWAVBRK1
from GODA import GODA
from GODA2 import GODA2
from GODA3 import GODA3
from GODA4 import GODA4
from GODA5 import GODA5

## ACES Update to python
#-------------------------------------------------------------
# Driver for Irregular Wave Transformation (page 3-2 of ACES User's
# Guide). Yields cumulative probability distributions of wave heights as
# a field of irregular waves propagate from deep water through the surf
# zone.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: July 1, 2011
# Date Verified: June 8, 2012

# Requires the following functions:
# ERRWAVBRK1
# GODA
# GODA2
# GODA3
# GODA4
# GODA5

# MAIN VARIABLE LIST:
#   INPUT
#   Ho: significant deepwater wave height
#   d: water depth
#   Ts: significant wave period
#   cotnsl: cotangent of nearshore slope
#   direc: principle direction of incident wave spectrum

#   OUTPUT
#   Hs: significant wave height
#   Hbar: mean wave height
#   Hrms: root-mean-square wave height
#   H10: average of highest 10 percent of all waves
#   H2: average of highest 2 percent of all waves
#   Hmax: maximum wave height
#   Ks: shoaling coefficient
#   psi: root-mean-square surf beat
#   Sw: wave setup
#   HoLo: deepwater wave steepness
#   Kr: effective refraction coefficient
#   doH: ratio of water depth to deepwater wave height
#   doL: relative water depth

#   OTHERS
#-------------------------------------------------------------

class IrrWaveTrans(BaseDriver):
    def __init__(self, Ho = None, d = None, Ts = None,\
        cotnsl = None, direc = None):
        if Ho != None:
            self.isSingleCase = True
            self.defaultValueHo = Ho
        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d
        if Ts != None:
            self.isSingleCase = True
            self.defaultValueTs = Ts
        if cotnsl != None:
            self.isSingleCase = True
            self.defaultValue_cotnsl = cotnsl
        if direc != None:
            self.isSingleCase = True
            self.defaultValue_direc = direc

        super(IrrWaveTrans, self).__init__()
    # end __init__

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueHo"):
            if self.isMetric:
                self.inputList.append(BaseField(\
                    "Ho: significant deepwater wave height (m)", 0.61, 6.09))
            else:
                self.inputList.append(BaseField(\
                    "Ho: significant deepwater wave height (ft)", 2.0, 20.0))

        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField(\
                "d: water depth (%s)" % self.labelUnitDist, 10.0, 5000.0))
        if not hasattr(self, "defaultValueTs"):
            self.inputList.append(BaseField(\
                "Ts: significant wave period (s)", 4.0, 16.0))
        if not hasattr(self, "defaultValue_cotnsl"):
            self.inputList.append(BaseField(\
                "cotnsl: cotangent of nearshore slope", 30.0, 100.0))
        if not hasattr(self, "defaultValue_direc"):
            self.inputList.append(BaseField(\
                "direc: principle direction of incident wave spectrum (deg)", -75.0, 75.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "irr_wave_trans")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueHo"):
            Ho = self.defaultValueHo
        else:
            Ho = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_d"):
            d = self.defaultValue_d
        else:
            d = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueTs"):
            Ts = self.defaultValueTs
        else:
            Ts = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotnsl"):
            cotnsl = self.defaultValue_cotnsl
        else:
            cotnsl = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_direc"):
            direc = self.defaultValue_direc
        else:
            direc = caseInputList[currIndex]

        return Ho, d, Ts, cotnsl, direc
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Ho, d, Ts, cotnsl, direc = self.getCalcValues(caseInputList)

        m2cm = 100.0
        g = self.g * m2cm

        # Convert meter input to centimeters
        Ho = Ho * m2cm
        d = d * m2cm

        Hb = ERRWAVBRK1(d, 0.78)
        if not (Ho < Hb):
            print("Error: Input wave broken (Hb = %6.2f %s" % (Hb, self.labelUnitDist))
            return

        Ks, Kr, Hmax, Hrms, Hbar, Hs, H10, H02, SBrms, HoLo, dLo,\
            dHo, deepd, theta, Sw, Hxo, cdfo, Hx, cdfx =\
            GODA(Ho, d, Ts, cotnsl, direc, g)

        print("\tSubject\tDeep\tUnits")
        print("Hs\t%-6.2f\t%-6.2f\t%s" %\
            (Hs[1]/m2cm, Hs[0]/m2cm, self.labelUnitDist))
        print("Hmean\t%-6.2f\t%-6.2f\t%s" %\
            (Hbar[1]/m2cm, Hbar[0]/m2cm, self.labelUnitDist))
        print("Hrms\t%-6.2f\t%-6.2f\t%s" %\
            (Hrms[1]/m2cm, Hrms[0]/m2cm, self.labelUnitDist))
        print("H10%%\t%-6.2f\t%-6.2f\t%s" %\
            (H10[1]/m2cm, H10[0]/m2cm, self.labelUnitDist))
        print("H02%%\t%-6.2f\t%-6.2f\t%s" %\
            (H02[1]/m2cm, H02[0]/m2cm, self.labelUnitDist))
        print("Hmax%%\t%-6.2f\t%-6.2f\t%s" %\
            (Hmax[1]/m2cm, Hmax[0]/m2cm, self.labelUnitDist))
        print("\nKs\t%-6.4f\t%-6.4f" % (Ks[1], Ks[0]))
        print("SBrms\t%-6.4f\t%-6.4f\t%s" %\
            (SBrms[1]/m2cm, SBrms[0]/m2cm, self.labelUnitDist))
        print("Sw\t%-6.4f\t%-6.4f\t%s" %\
            (Sw[1]/m2cm, Sw[0]/m2cm, self.labelUnitDist))
        print("Ho/Lo\t%-6.4f\t%-6.4f" % (HoLo, HoLo))
        print("Kr\t%-6.4f" % Kr)
        print("d/Ho\t%-6.4f\t%-6.4f" % (dHo[1], dHo[0]))
        print("d/Lo\t%-6.4f\t%-6.4f" % (dLo[1], dLo[0]))

        dataDict = {"Ho": Ho, "d": d, "Ts": Ts, "cotnsl": cotnsl,\
            "direc": direc, "Hs": Hs, "Hbar": Hbar, "Hrms": Hrms,\
            "H10": H10, "H02": H02, "Hmax": Hmax, "Ks": Ks,\
            "SBrms": SBrms, "Sw": Sw, "HoLo": HoLo, "Kr": Kr,\
            "dHo": dHo, "dLo": dLo}
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        m2cm = 100.0

        self.fileRef.write("Input\n")
        self.fileRef.write("Ho\t%6.2f %s\n" % (dataDict["Ho"]/m2cm, self.labelUnitDist))
        self.fileRef.write("d\t%6.2f %s\n" % (dataDict["d"]/m2cm, self.labelUnitDist))
        self.fileRef.write("Ts\t%6.2f s\n" % dataDict["Ts"])
        self.fileRef.write("cotnsl\t%6.2f\n" % dataDict["cotnsl"])
        self.fileRef.write("direc\t%6.2f deg\n\n" % dataDict["direc"])

        self.fileRef.write("\tSubject\tDeep\tUnits\n")
        self.fileRef.write("Hs\t%-6.2f\t%-6.2f\t%s\n" %\
            (dataDict["Hs"][1]/m2cm, dataDict["Hs"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("Hmean\t%-6.2f\t%-6.2f\t%s\n" %\
            (dataDict["Hbar"][1]/m2cm, dataDict["Hbar"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("Hrms\t%-6.2f\t%-6.2f\t%s\n" %\
            (dataDict["Hrms"][1]/m2cm, dataDict["Hrms"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("H10%%\t%-6.2f\t%-6.2f\t%s\n" %\
            (dataDict["H10"][1]/m2cm, dataDict["H10"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("H02%%\t%-6.2f\t%-6.2f\t%s\n" %\
            (dataDict["H02"][1]/m2cm, dataDict["H02"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("Hmax%%\t%-6.2f\t%-6.2f\t%s\n" %\
            (dataDict["Hmax"][1]/m2cm, dataDict["Hmax"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("\nKs\t%-6.4f\t%-6.4f\n" % (dataDict["Ks"][1], dataDict["Ks"][0]))
        self.fileRef.write("SBrms\t%-6.4f\t%-6.4f\t%s\n" %\
            (dataDict["SBrms"][1]/m2cm, dataDict["SBrms"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("Sw\t%-6.4f\t%-6.4f\t%s\n" %\
            (dataDict["Sw"][1]/m2cm, dataDict["Sw"][0]/m2cm, self.labelUnitDist))
        self.fileRef.write("Ho/Lo\t%-6.4f\t%-6.4f\n" % (dataDict["HoLo"], dataDict["HoLo"]))
        self.fileRef.write("Kr\t%-6.4f\n" % dataDict["Kr"])
        self.fileRef.write("d/Ho\t%-6.4f\t%-6.4f\n" % (dataDict["dHo"][1], dataDict["dHo"][0]))
        self.fileRef.write("d/Lo\t%-6.4f\t%-6.4f\n" % (dataDict["dLo"][1], dataDict["dLo"][0]))
    # end fileOutputWriteData


driver = IrrWaveTrans()