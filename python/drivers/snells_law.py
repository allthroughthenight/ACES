import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK1 import ERRWAVBRK1
from ERRWAVBRK3 import ERRWAVBRK3
from LWTDWS import LWTDWS
from LWTGEN import LWTGEN
from LWTTWM import LWTTWM
from LWTTWS import LWTTWS

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Lineat Wave Theory with Snell's Law (page 3-1 in ACES User's Guide)
# Provides a simple estimate for wave shoaling and refraction using Snell's
# Law with wave properties predicted by linear wave theory

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 11, 2011
# Date Verified: June 6, 2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK1
# ERRWAVBRK3
# LWTDWS
# LWTGEN
# LWTTWM
# LWTTWS
# ERRWAVBRK3
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   H1: wave height at known location (m)
#   T: wave period at known location (sec)
#   d1: water depth at known location (m)
#   alpha1: wave crest angle (deg)
#   cotphi: cotan of nearshore slope
#   d2: water depth at desired location (m)

#   OUTPUT
#   H0: deepwater wave height (m)
#   H2: wave height at subject location (m)
#   alpha0: deepwater wave crest angle (deg)
#   alpha2: wave crest angle at subject location (deg)
#   L0: deepwater wavelength (m)
#   L1: wavelength at known location (m)
#   L2: wavelength at subject location (m)
#   c1: wave celerity at known location (m/s)
#   c0: deepwater wave celerity (m/s)
#   c2: wave celerity at subject location (m/s)
#   cg1: group speed at known location (m/s)
#   cg0: deepwater group speed (m/s)
#   cg2: group speef at subject location (m/s)
#   E1: energy density at known location (N-m/m^2)
#   E0: deepwater energy density (N-m/m^2)
#   E2: enery density at subject location (N-m/m^2)
#   P1: energy flux at known location (N-m/m-s)
#   P0: deepwater wave flux (N-m/m-s)
#   P2: wave flux at subject location (N-m/m-s)
#   HL: deepwater wave steepness
#   Ur1: Ursell number at known location
#   Ur2: Ursell number at desired location
#   Hb: breaking wave height (m)
#   db: breaking wave depth (m)
#-------------------------------------------------------------

class SnellsLaw(BaseDriver):
    def __init__(self, H1 = None, T = None, d1 = None, alpha1 = None,\
        cotphi = None, d2 = None):
        self.exporter = EXPORTER("output/exportSnellsLaw")
        
        if H1 != None:
            self.isSingleCase = True
            self.defaultValueH1 = H1
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if d1 != None:
            self.isSingleCase = True
            self.defaultValue_d1 = d1
        if alpha1 != None:
            self.isSingleCase = True
            self.defaultValue_alpha1 = alpha1
        if cotphi != None:
            self.isSingleCase = True
            self.defaultValue_cotphi = cotphi
        if d2 != None:
            self.isSingleCase = True
            self.defaultValue_d2 = d2

        super(SnellsLaw, self).__init__()

        self.exporter.close()
    # end __init__

    def userInput(self):
        super(SnellsLaw, self).userInput()

        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH1"):
            self.inputList.append(BaseField("H1: wave height at known location (%s)" % (self.labelUnitDist), 0.1, 200.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField("T: wave period at known location (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_d1"):
            self.inputList.append(BaseField("d1: water depth at known location (%s)" % (self.labelUnitDist), 0.1, 5000.0))
        if not hasattr(self, "defaultValue_alpha1"):
            self.inputList.append(BaseField("alpha1: wave crest angle (deg)", 0.0, 90.0))
        if not hasattr(self, "defaultValue_cotphi"):
            self.inputList.append(BaseField("cotphi: cotan of nearshore slope", 5.0, 1000.0))
        if not hasattr(self, "defaultValue_d2"):
            self.inputList.append(BaseField("d2: water depth at desired location (%s)" % (self.labelUnitDist), 0.1, 5000.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "snells_law")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueH1"):
            H1 = self.defaultValueH1
        else:
            H1 = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueT"):
            T = self.defaultValueT
        else:
            T = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_d1"):
            d1 = self.defaultValue_d1
        else:
            d1 = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_alpha1"):
            alpha1 = self.defaultValue_alpha1
        else:
            alpha1 = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotphi"):
            cotphi = self.defaultValue_cotphi
        else:
            cotphi = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_d2"):
            d2 = self.defaultValue_d2
        else:
            d2 = caseInputList[currIndex]

        return H1, T, d1, alpha1, cotphi, d2
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H1, T, d1, alpha1, cotphi, d2 =\
            self.getCalcValues(caseInputList)
        dataDict = {"H1": H1, "T": T, "d1": d1, "alpha1": alpha1,\
            "cotphi": cotphi, "d2": d2}
        
        m = 1.0 / cotphi

        Hb = ERRWAVBRK1(d1, 0.78)
        if not (H1 < Hb):
            self.errorMsg = "Error: Known wave broken (Hb = %6.2f %s)" % (Hb, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        #determine known wave properties
        c1, c0, cg1, cg0, k1, L1, L0, reldep1 = LWTGEN(d1, T, self.g)
        E1, P1, Ur1, setdown1 = LWTTWM(cg1, d1, H1, L1, reldep1, self.rho, self.g, k1)

        steep, maxstp = ERRSTP(H1, d1, L1)
        if not (steep < maxstp):
            self.errorMsg = "Error: Known wave unstable (Max: %0.4f, [H/L] = %0.4f)" % (maxstp, steep)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        #determine deepwater wave properties
        alpha0, H0 = LWTDWS(alpha1, c1, cg1, c0, H1)

        E0 = (1.0/8.0)*self.rho*self.g*(H0**2)
        P0 = E0*cg0
        HL = H0/L0

        if not (HL < (1.0/7.0)):
            self.errorMsg = "Error: Deepwater wave unstable, [H0/L0] > (1/7)"
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        #determine subject wave properties
        c2, c0, cg2, cg0, k2, L2, L0, reldep2 = LWTGEN(d2, T, self.g)
        alpha2, H2, kr, ks = LWTTWS(alpha0, c2, cg2, c0, H0)
        E2, P2, Ur2, sedown2 = LWTTWM(cg2, d2, H2, L2, reldep2, self.rho, self.g, k2)

        Hb, db = ERRWAVBRK3(H0, L0, T, m)
        if not (H2 < Hb):
            self.errorMsg = "Error: Subject wave broken (Hb = %6.2f %s, hb = %6.2f %s" %\
                (Hb, self.labelUnitDist, db, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        steep, maxstp = ERRSTP(H2, d2, L2)
        if not (steep < maxstp):
            self.errorMsg = "Error: Subject wave unstable (Max: %0.4f, [H/L] = %0.4f)" % (maxstp, steep)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        print("\t\t\tKnown\t\tDeepwater\t\tSubject\t\tUnits")
        print("Wave height\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s" %\
            (H1, H0, H2, self.labelUnitDist))
        print("Wave crest angle\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\tdeg" %\
            (alpha1, alpha0, alpha2))
        print("Wavelength\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s" %\
            (L1, L0, L2, self.labelUnitDist))
        print("Celerity\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s/s" %\
            (c1, c0, c2, self.labelUnitDist))
        print("Group speed\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s/s" %\
            (cg1, cg0, cg2, self.labelUnitDist))
        print("Energy density\t\t%-8.2f\t%-8.2f\t\t%-8.2f\t%s-%s/%s^2" %\
            (E1, E0, E2, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        print("Energy flux\t\t%-8.2f\t%-8.2f\t\t%-8.2f\t%s-%s/sec-%s" %\
            (P1, P0, P2, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        print("Ursell number\t\t%-5.2f\t\t\t\t\t%-5.2f" % (Ur1, Ur2))
        print("Wave steepness\t\t\t\t%-5.2f" % HL)

        print("\nBreaking Parameters")
        print("Breaking height\t\t%-5.2f %s" % (Hb, self.labelUnitDist))
        print("Breaking depth\t\t%-5.2f %s" % (db, self.labelUnitDist))

        dataDict.update({"H0": H0, "H2": H2,\
            "alpha0": alpha0, "alpha2": alpha2, "L1": L1,\
            "L0": L0, "L2": L2, "c1": c1, "c0": c0, "c2": c2,\
            "cg1": cg1, "cg0": cg0, "cg2": cg2, "E1": E1, "E0": E0,\
            "E2": E2, "P1": P1, "P0": P0, "P2": P2, "Ur1": Ur1,\
            "Ur2": Ur2, "HL": HL, "Hb": Hb, "db": db})
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("H1\t%6.2f %s\n" % (dataDict["H1"], self.labelUnitDist))
        self.fileRef.write("T\t%6.2f s\n" % dataDict["T"])
        self.fileRef.write("d1\t%6.2f %s\n" % (dataDict["d1"], self.labelUnitDist))
        self.fileRef.write("alpha1\t%6.2f deg\n" % dataDict["alpha1"])
        self.fileRef.write("cotphi\t%6.2f\n" % dataDict["cotphi"])
        self.fileRef.write("d2\t%6.2f %s\n\n" % (dataDict["d2"], self.labelUnitDist))

        if self.errorMsg != None:
            self.fileRef.write("%s\n" % self.errorMsg)
        else:
            self.fileRef.write("\t\t\tKnown\t\tDeepwater\t\tSubject\t\tUnits\n")
            self.fileRef.write("Wave height\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s\n" %\
                (dataDict["H1"], dataDict["H0"], dataDict["H2"], self.labelUnitDist))
            self.fileRef.write("Wave crest angle\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\tdeg\n" %\
                (dataDict["alpha1"], dataDict["alpha0"], dataDict["alpha2"]))
            self.fileRef.write("Wavelength\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s\n" %\
                (dataDict["L1"], dataDict["L0"], dataDict["L2"], self.labelUnitDist))
            self.fileRef.write("Celerity\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s/s\n" %\
                (dataDict["c1"], dataDict["c0"], dataDict["c2"], self.labelUnitDist))
            self.fileRef.write("Group speed\t\t%-5.2f\t\t%-5.2f\t\t\t%-5.2f\t\t%s/s\n" %\
                (dataDict["cg1"], dataDict["cg0"], dataDict["cg2"], self.labelUnitDist))
            self.fileRef.write("Energy density\t\t%-8.2f\t%-8.2f\t\t%-8.2f\t%s-%s/%s^2\n" %\
                (dataDict["E1"], dataDict["E0"], dataDict["E2"], self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
            self.fileRef.write("Energy flux\t\t%-8.2f\t%-8.2f\t\t%-8.2f\t%s-%s/sec-%s\n" %\
                (dataDict["P1"], dataDict["P0"], dataDict["P2"], self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
            self.fileRef.write("Ursell number\t\t%-5.2f\t\t\t\t\t%-5.2f\n" %\
                (dataDict["Ur1"], dataDict["Ur2"]))
            self.fileRef.write("Wave steepness\t\t\t\t%-5.2f\n" % dataDict["HL"])
    
            self.fileRef.write("\nBreaking Parameters\n")
            self.fileRef.write("Breaking height\t\t%-5.2f %s\n" %\
                (dataDict["Hb"], self.labelUnitDist))
            self.fileRef.write("Breaking depth\t\t%-5.2f %s\n" %\
                (dataDict["db"], self.labelUnitDist))
            
        exportData = [dataDict["H1"], dataDict["T"], dataDict["d1"],\
            dataDict["alpha1"], dataDict["cotphi"], dataDict["d2"]]
        if self.errorMsg != None:
            exportData.append(self.errorMsg)
        else:
            exportData = exportData + [dataDict["H1"], dataDict["H0"],\
                dataDict["H2"], dataDict["alpha1"], dataDict["alpha0"],\
                dataDict["alpha2"], dataDict["L1"], dataDict["L0"],\
                dataDict["L2"], dataDict["c1"], dataDict["c0"],\
                dataDict["c2"], dataDict["cg1"], dataDict["cg0"],\
                dataDict["cg2"], dataDict["E1"], dataDict["E0"],\
                dataDict["E2"], dataDict["P1"], dataDict["P0"],\
                dataDict["P2"], dataDict["Ur1"], dataDict["Ur2"],\
                dataDict["HL"]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData


driver = SnellsLaw()