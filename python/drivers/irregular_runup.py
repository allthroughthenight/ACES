import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Irregular Wave Runup on Beaches (page 5-1 in ACES # User's Guide).
# Provides an approach to calculate runup statistical parameters for wave
# runup on smooth slope linear beaches.

# Updated by: Mary Anderson,  USACE-CHL-Coastal Processes Branch
# Date Created: April 18,  2011
# Date Verified: June 6,  2012

# Requires the following functions:
# no functions required

# MAIN VARIABLE LIST:
#   INPUT
#   Hs0: deepwater significant wave height
#   Tp: peak energy wave period (sec)
#   cottheta: cotangent of foreshore slope

#   OUTPUT
#   Rmax: maximum runup
#   R2: runup exceeded by 2 percent of the runups
#   R110: Average of the highest one-tenth of the runups
#   R13: Average of highest one-third of the runups
#   Ravg: average run

#   OTHERS
#   I: Irribarren number
#-------------------------------------------------------------

class IrregularRunup(BaseDriver):
    def __init__(self, Hs0 = None, Tp = None, cottheta = None):
        self.exporter = EXPORTER("output/exportIrregularRunup.txt")

        if Hs0 != None:
            self.isSingleCase = True
            self.defaultValueHs0 = Hs0
        if Tp != None:
            self.isSingleCase = True
            self.defaultValueTp = Tp
        if cottheta != None:
            self.isSingleCase = True
            self.defaultValue_cottheta = cottheta

        super(IrregularRunup, self).__init__()

        self.exporter.close()
    # end __init__

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueHs0"):
            self.inputList.append(BaseField(\
                "Hs0: deepwater significant wave height (%s)" %\
                (self.labelUnitDist), 0.1, 100.0))
        if not hasattr(self, "defaultValueTp"):
            self.inputList.append(BaseField(\
                "Tp: peak energy wave period (sec)", 0.1, 100.0))
        if not hasattr(self, "defaultValue_cottheta"):
            self.inputList.append(BaseField(\
                "cottheta: cotangent of foreshore slope", 0.1, 100.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "irregular_runup")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueHs0"):
            Hs0 = self.defaultValueHs0
        else:
            Hs0 = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueTp"):
            Tp = self.defaultValueTp
        else:
            Tp = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cottheta"):
            cottheta = self.defaultValue_cottheta
        else:
            cottheta = caseInputList[currIndex]

        return Hs0, Tp, cottheta
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Hs0, Tp, cottheta = self.getCalcValues(caseInputList)
        dataDict = {"Hs0": Hs0, "Tp": Tp, "cottheta": cottheta}

        #Coefficients provided by Mase (1989)
        amax = 2.32
        bmax = 0.77
        a2 = 1.86
        b2 = 0.71
        a110 = 1.70
        b110 = 0.71
        a13 = 1.38
        b13 = 0.70
        aavg = 0.88
        bavg = 0.69

        L0 = self.g * (Tp**2) / (2 * math.pi)
        steep = Hs0 / L0
        if not (steep < 0.142):
            self.errorMsg = 'Error: Input wave unstable (Max: 0.142, [H/L] = %0.4f)' % steep
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        tantheta = 1 / cottheta
        I = tantheta / math.sqrt(Hs0 / L0)

        Rmax = Hs0 * amax * (I**bmax)
        R2 = Hs0 * a2 * (I**b2)
        R110 = Hs0 * a110 * (I**b110)
        R13 = Hs0 * a13 * (I**b13)
        Ravg = Hs0 * aavg * (I**bavg)

        print('%s\t\t\t%6.2f %s' % ('Maximum runup', Rmax, self.labelUnitDist))
        print('%s\t%6.2f %s' % ('Runup exceeded by 2% of runup', R2, self.labelUnitDist))
        print('%s\t%6.2f %s' % ('Avg. of highest 1 / 10 runups', R110, self.labelUnitDist))
        print('%s\t%6.2f %s' % ('Avg. of highest 1 / 3 runups', R13, self.labelUnitDist))
        print('%s\t\t\t%6.2f %s' % ('Average runup', Ravg, self.labelUnitDist))

        dataDict.update({"Rmax": Rmax, "R2": R2, "R110": R110, "R13": R13,\
            "Ravg": Ravg})
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("Hs0\t\t\t%6.2f %s\n" %\
            (dataDict["Hs0"], self.labelUnitDist))
        self.fileRef.write("Tp\t\t\t%6.2f s\n" % dataDict["Tp"])
        self.fileRef.write("cottheta\t\t%6.2f\n\n" % dataDict["cottheta"])

        if self.errorMsg != None:
            self.fileRef.write("%s\n" % self.errorMsg)
        else:
            self.fileRef.write('%s\t\t\t%6.2f %s\n' %\
                ('Maximum runup', dataDict["Rmax"], self.labelUnitDist))
            self.fileRef.write('%s\t%6.2f %s\n' %\
                ('Runup exceeded by 2% of runup', dataDict["R2"], self.labelUnitDist))
            self.fileRef.write('%s\t%6.2f %s\n' %\
                ('Avg. of highest 1 / 10 runups', dataDict["R110"], self.labelUnitDist))
            self.fileRef.write('%s\t%6.2f %s\n' %\
                ('Avg. of highest 1 / 3 runups', dataDict["R13"], self.labelUnitDist))
            self.fileRef.write('%s\t\t\t%6.2f %s\n' %\
                ('Average runup', dataDict["Ravg"], self.labelUnitDist))
        
        exportData = [dataDict["Hs0"], dataDict["Tp"], dataDict["cottheta"]]
        if self.errorMsg != None:
            exportData.append("Error")
        else:
            exportData = exportData + [dataDict["Rmax"], dataDict["R2"],\
                dataDict["R110"], dataDict["R13"], dataDict["Ravg"]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData


driver = IrregularRunup()