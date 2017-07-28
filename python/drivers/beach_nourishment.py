import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
from BOVERF import BOVERF

## ACES Update to Python BEACH NOURISMENT and OVERFILL RATIO
#-------------------------------------------------------------
# Evaluates the suitable of borrow material as beach fill and give overfill
# nourishment ratios. (Aces Tech Manual Chapter 6-4-1)

# Updated by: Yaprak Onat
# Date Created: June 21, 2016
# Date Modified:

# Requires the following functions:


# MAIN VARIABLE LIST:
#   INPUT
#  Vol_i = initial volume (yd**3 or m**3) Range 1 to 10**8
#   M_R = Native mean (phi, mm) Range -5 to 5
#   ro_n = native standard deviation (phi) Range 0.01 to 5
#   M_b = borrow mean (phi, mm) Range -5 to 5
#   ro_b = borrow standard deviation (phi) Range 0.01 to 5
#
#   OUTPUT
#   R_A = Overfill Ratio
#   Rj = Renourishment factor
#   Vol_D = Design Volume (yd**3 or m**3)

#   OTHERS
#   g: gravity [32.17 ft / s**2]
#   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs / ft**3]
#   rhos: density of sediment [5.14 slugs / ft**3 in FORTRAN source code]
#-------------------------------------------------------------

class BeachNourishment(BaseDriver):
    def __init__(self, Vol_i = None, M_R = None, ro_n = None, M_b = None, ro_b = None):
        self.exporter = EXPORTER("output/exportBeachNourishment.txt")
        
        if Vol_i != None:
            self.isSingleCase = True
            self.defaultValueVol_i = Vol_i
        if M_R != None:
            self.isSingleCase = True
            self.defaultValueM_R = M_R
        if ro_n != None:
            self.isSingleCase = True
            self.defaultValue_ro_n = ro_n
        if M_b != None:
            self.isSingleCase = True
            self.defaultValueM_b = M_b
        if ro_b != None:
            self.isSingleCase = True
            self.defaultValue_ro_b = ro_b

        super(BeachNourishment, self).__init__()
        
        self.exporter.close()
    # end __init__

    def defineInputDataList(self):
        if self.isMetric:
            self.labelUnitVolumeRate = "m^3"
            self.labelUnitGrain = "mm"
        else:
            self.labelUnitVolumeRate = "yd^3"
            self.labelUnitGrain = "phi"

        self.inputList = []

        if not hasattr(self, "defaultValueVol_i"):
            self.inputList.append(BaseField(\
                "Vol_i: initial volume (%s)" % (self.labelUnitVolumeRate), 1, 10**8))

        if not hasattr(self, "defaultValueM_R"):
            self.inputList.append(BaseField(\
                "M_R: Native mean (%s)" % (self.labelUnitGrain), -5.0, 5.0))

        if not hasattr(self, "defaultValue_ro_n"):
            self.inputList.append(BaseField(\
                "ro_n: Native standard deviation (phi)", 0.01, 5.0))

        if not hasattr(self, "defaultValueM_b"):
            self.inputList.append(BaseField(\
                "M_b: Borrow mean (%s)" % (self.labelUnitGrain), -5.0, 5.0))

        if not hasattr(self, "defaultValue_ro_b"):
            self.inputList.append(BaseField(\
                "ro_b: Borrow standard deviation (phi)", 0.01, 5.0))
    # end defineInputList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "beach_nourishment")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueVol_i"):
            Vol_i = self.defaultValueVol_i
        else:
            Vol_i = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueM_R"):
            M_R = self.defaultValueM_R
        else:
            M_R = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ro_n"):
            ro_n = self.defaultValue_ro_n
        else:
            ro_n = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueM_b"):
            M_b = self.defaultValueM_b
        else:
            M_b = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ro_b"):
            ro_b = self.defaultValue_ro_b
        else:
            ro_b = caseInputList[currIndex]

        return Vol_i, M_R, ro_n, M_b, ro_b
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Vol_i, M_R, ro_n, M_b, ro_b = self.getCalcValues(caseInputList)

        catg = 0 # category of the material according to table 6-4-1 in Aces manual

        if self.isMetric:
            M_R = -(math.log(M_R) / math.log(2.0))
            M_b = -(math.log(M_b) / math.log(2.0))

        # Relationships of phi means and pho standard deviations
        if ro_b > ro_n:
            print('Borrow material is more poorly sorted than native material')
            if M_b > M_R:
                print('Borrow material is finer than native material')
                catg = 1
            else:
                print('Borrow material is coarser than native material')
                catg = 2
        else:
            if M_b < M_R:
               print('Borrow material is coarser than native material')
               catg = 3
            else:
               print('Borrow material is finer than native material')
               catg = 4
        # end if

        delta = (M_b-M_R)/ro_n # phi mean difference
        sigma = ro_b/ro_n # phi sorting ratio

        if sigma == 1:
            theta_1 = 0
            theta_2 = float("inf")
        else:
            # defining theta_1 and theta_2
            if catg == 1 or catg == 2:
                theta_1 = max(-1, (-delta/(sigma**2 - 1)))
                theta_2 = float("inf")
            else:
                theta_1 = -1
                theta_2 = max(-1, (1 + (2*delta/(1 - sigma**2))))

        # calculate overfill ratio
        bk1 = (theta_1 - delta)/sigma
        fn1 = BOVERF(bk1)
        ft1 = BOVERF(theta_1)

        if theta_2 == float("inf"):
            fn3 = ((1.0 - ft1)/sigma)*math.exp(0.5*(theta_1**2 - bk1**2))
            R_A = 1.0/(fn1 + fn3)
        else:
            bk2 = (theta_2 - delta)/sigma
            fn2 = BOVERF(bk2)
            ft2 = BOVERF(theta_2)
            fn3 = ((ft2 - ft1)/sigma)*math.exp(0.5*(theta_1**2 - bk1**2))
            R_A = 1.0 / (1 - fn2 + fn1 + fn3)
        # end if

        if R_A < 1.0:
            print("Error: Overfill ratio (R_A) < 1.0. Respecify data")

        R_j = math.exp((delta - 0.5*((ro_b**2 / ro_n**2) - 1)))

        Vol_D = R_A * Vol_i

        print("Overfill Ratio, R_A\t\t\t%6.2f" % (R_A))
        print("Renourishment factor, R_j\t\t%6.2f" % (R_j))
        print("Design Volume, Vol_D\t\t\t%6.2f %s" % (Vol_D, self.labelUnitVolumeRate))

        dataDict = {"Vol_i": Vol_i, "M_R": M_R, "ro_n": ro_n, "M_b": M_b,\
            "ro_b": ro_b, "R_A": R_A, "R_j": R_j, "Vol_D": Vol_D }
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("Vol_i\t%6.2f %s\n" %\
            (dataDict["Vol_i"], self.labelUnitVolumeRate))
        self.fileRef.write("M_R\t%6.2f %s\n" % (dataDict["M_R"], self.labelUnitGrain))
        self.fileRef.write("ro_n\t%6.2f\n" % (dataDict["ro_n"]))
        self.fileRef.write("M_b\t%6.2f %s\n" % (dataDict["M_b"], self.labelUnitGrain))
        self.fileRef.write("ro_b\t%6.2f\n\n" % (dataDict["ro_b"]))

        self.fileRef.write("Overfill Ratio, R_A\t\t\t%6.2f\n" % (dataDict["R_A"]))
        self.fileRef.write("Renourishment factor, R_j\t\t%6.2f\n" % (dataDict["R_j"]))
        self.fileRef.write("Design Volume, Vol_D\t\t\t%6.2f %s\n" %\
            (dataDict["Vol_D"], self.labelUnitVolumeRate))
        
        exportData = [dataDict["Vol_i"], dataDict["M_R"], dataDict["ro_n"],\
            dataDict["M_b"], dataDict["ro_b"]]
        if self.errorMsg != None:
            exportData.append("Error")
        else:
            exportData = exportData + [dataDict["R_A"], dataDict["R_j"],\
                dataDict["Vol_D"]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData


driver = BeachNourishment()