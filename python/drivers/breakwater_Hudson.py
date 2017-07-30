import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Breakwater Design Using Hudson and Related Equations
# (page 4-1 in ACES User's Guide). Estimates armor weight, minimum crest,
# width, armor thickness, and the number of armor units per unit area of
# a breakwater using Hudson and related equations.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 13, 2011
# Date Modified:

# Requires the following functions:
# no functions required

# MAIN VARIABLE LIST:
#   INPUT
#   unitwt: armor specific unit weight (N/m^3) - 1 N/m^3 = 157 ft/lb^3
#   H: wave height (m)
#   Kd: stability coefficient
#   kdelt: layer coefficient
#   P: average porosity of armor layer
#   cotssl: cotangent of structure slope
#   n: number of armor units comprising the thickness of the armor layer

#   OUTPUT
#   w: weight of individual armor unit (N)
#   b: crest width of breakwater (m)
#   r: average cover layer thickness (m)
#   Nr: number of single armor units per unit surface area

#   OTHERS
#   rho: density of water (kg/m^3)
#   H20weight: specific weight of water
#-------------------------------------------------------------

class BreakwaterHudson(BaseDriver):
    def __init__(self, unitwt = None, H = None, Kd = None,\
        kdelt = None, P = None, cotssl = None, n = None):
        self.exporter = EXPORTER("output/exportBreakwaterHudson")

        if unitwt != None:
            self.isSingleCase = True
            self.defaultValue_unitwt = unitwt
        if H != None:
            self.isSingleCase = True
            self.defaultValueH = H
        if Kd != None:
            self.isSingleCase = True
            self.defaultValueKd = Kd
        if kdelt != None:
            self.isSingleCase = True
            self.defaultValue_kdelt = kdelt
        if P != None:
            self.isSingleCase = True
            self.defaultValueP = P
        if cotssl != None:
            self.isSingleCase = True
            self.defaultValue_cotssl = cotssl
        if n != None:
            self.isSingleCase = True
            self.defaultValue_n = n

        super(BreakwaterHudson, self).__init__()

        self.exporter.close()
    # end __init__

    def userInput(self):
        super(BreakwaterHudson, self).userInput()

        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValue_unitwt"):
            self.inputList.append(BaseField(\
                "unitwt: armor specific unit weight (%s/%s^3)" %\
                (self.labelUnitWt, self.labelUnitDist), 1.0, 99999.0))
        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField(\
                "H: wave height (%s)" % self.labelUnitDist, 0.1, 100.0))
        if not hasattr(self, "defaultValueKd"):
            self.inputList.append(BaseField(\
                "Kd: stability coefficient", 0.0, 10.0))
        if not hasattr(self, "defaultValue_kdelt"):
            self.inputList.append(BaseField(\
                "kdelt: layer coefficient", 0.0, 2.0))
        if not hasattr(self, "defaultValueP"):
            self.inputList.append(BaseField(\
                "P: average porosity of armor layer", 0.0, 54.0))
        if not hasattr(self, "defaultValue_cotssl"):
            self.inputList.append(BaseField(\
                "cotssl: cotangent of structure slope", 1.0, 6.0))
        if not hasattr(self, "defaultValue_n"):
            self.inputList.append(BaseField(\
                "n: number of armor units comprising the thickness of the armor layer", 1.0, 3.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "breakwater_Hudson")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValue_unitwt"):
            unitwt = self.defaultValue_unitwt
        else:
            unitwt = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueH"):
            H = self.defaultValueH
        else:
            H = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueKd"):
            Kd = self.defaultValueKd
        else:
            Kd = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_kdelt"):
            kdelt = self.defaultValue_kdelt
        else:
            kdelt = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueP"):
            P = self.defaultValueP
        else:
            P = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotssl"):
            cotssl = self.defaultValue_cotssl
        else:
            cotssl = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_n"):
            n = self.defaultValue_n
        else:
            n = caseInputList[currIndex]

        return unitwt, H, Kd, kdelt, P, cotssl, n
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        unitwt, H, Kd, kdelt, P, cotssl, n =\
            self.getCalcValues(caseInputList)
        dataDict = {"unitwt": unitwt, "H": H, "Kd": Kd,\
            "kdelt": kdelt, "P": P, "cotssl": cotssl, "n": n}

        H20weight = self.rho*self.g #64 lb/ft^3 for seawater, 62.4 for fresh

        specgrav = unitwt / H20weight


        w = (unitwt*H**3)/(Kd*(specgrav - 1.0)**3 * cotssl)
        if w < 0.0:
            self.errorMsg = "Error: Unit weight must be greater than water weight"
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return
        
        r = n*kdelt*(w/unitwt)**(1.0/3.0)
        Nr = 1000.0*n*kdelt*(1.0 - P/100.0)*(unitwt/w)**(2.0/3.0)
        b = 3.0*kdelt*(w/unitwt)**(1.0/3.0)
        
        if self.isMetric:
            if w > 8000.0:
                w = w/8896.4 #1 ton = 8896.4 N
                self.labelUnitWtLrg = "tons"
            else:
                self.labelUnitWtLrg = "N"
        else:
            if w > 2000.0:
                w = w/2000.0
                self.labelUnitWtLrg = "tons"
            else:
                self.labelUnitWtLrg = "lbs"
        # end if

        print("Weight of individual unit\t%6.2f %s" %\
            (w, self.labelUnitWtLrg))
        print("Crest width\t\t\t%6.2f %s" % (b, self.labelUnitDist))
        print("Average cover layer thickness\t%6.2f %s" %\
            (r, self.labelUnitDist))
        print("Number of single armor unit\t%6.2f" % Nr)

        dataDict.update({"w": w, "b": b, "r": r, "Nr": Nr})
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("unitwt                             %6.2f %s/%s^3\n" %\
            (dataDict["unitwt"], self.labelUnitWt, self.labelUnitDist))
        self.fileRef.write("H                                  %6.2f %s\n" %\
            (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("Kd                                 %6.2f\n" % dataDict["Kd"])
        self.fileRef.write("kdelt                              %6.2f\n" % dataDict["kdelt"])
        self.fileRef.write("P                                  %6.2f %%\n" % dataDict["P"])
        self.fileRef.write("cotssl                             %6.2f\n" % dataDict["cotssl"])
        self.fileRef.write("n                                  %6.2f\n\n" % dataDict["n"])

        if self.errorMsg != None:
            self.fileRef.write("%s\n" % self.errorMsg)
        else:
            self.fileRef.write("Weight of individual unit\t%6.2f %s\n" %\
                (dataDict["w"], self.labelUnitWtLrg))
            self.fileRef.write("Crest width\t\t\t%6.2f %s\n" %\
                (dataDict["b"], self.labelUnitDist))
            self.fileRef.write("Average cover layer thickness\t%6.2f %s\n" %\
                (dataDict["r"], self.labelUnitDist))
            self.fileRef.write("Number of single armor unit\t%6.2f\n" % dataDict["Nr"])
        
        exportData = [dataDict["unitwt"], dataDict["H"], dataDict["Kd"],\
            dataDict["kdelt"], dataDict["P"], dataDict["cotssl"],\
            dataDict["n"]]
        if self.errorMsg != None:
            exportData.append(self.errorMsg)
        else:
            exportData = exportData + [dataDict["w"], dataDict["b"],\
                dataDict["r"], dataDict["Nr"]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData


driver = BreakwaterHudson()