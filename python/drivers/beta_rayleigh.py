import sys
import math
import scipy.special as sp
import matplotlib.pyplot as plt
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK1 import ERRWAVBRK1
from WAVELEN import WAVELEN

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Beta-Rayleigh Distribution (page 1-2 of ACES User's Guide).
# Provides a statistical representation for a shallow-water wave height
# distribution.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 28, 2011
# Date Verified: June 27, 2012
# Modifications done by Yaprak Onat
# Last Verified:

# Requires the following functions:
# ERRWAVBRK1
# WAVELEN
# ERRSTP

# MAIN VARIABLE LIST:
#   INPUT
#   Hmo: zero-moment wave height [m]
#   Tp: peak wave period [s]
#   d: water depth [m]

#   OUTPUT
#   Hrms: root-mean-square wave height [m]
#   Hmed: median wave height [m]
#   H13: significant wave height (average of the 1/3 highest waves) [m]
#   H110: average of the 1/10 highest waves [m]
#   H1100: average of the 1/100 highest waves [m]

#   OTHER:
#------------------------------------------------------------

class BetaRayleigh(BaseDriver):
    def __init__(self, Hmo = None, Tp = None, d = None):
        self.exporter = EXPORTER("output/exportBetaRayleigh")

        if Hmo != None:
            self.isSingleCase = True
            self.defaultValueHmo = Hmo
        if Tp != None:
            self.isSingleCase = True
            self.defaultValueTp = Tp
        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d

        super(BetaRayleigh, self).__init__()

        self.exporter.close()
    # end __init__

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueHmo"):
            self.inputList.append(BaseField("Hmo: zero-moment wave height [%s]" % (self.labelUnitDist), 0.1, 60.0))
        if not hasattr(self, "defaultValueTp"):
            self.inputList.append(BaseField("Tp: peak wave period [s]", 2.0, 30.0))
        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField("d: water depth [%s]" % (self.labelUnitDist), 0.1, 3000.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "beta_rayleigh")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueHmo"):
            Hmo = self.defaultValueHmo
        else:
            Hmo = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueTp"):
            Tp = self.defaultValueTp
        else:
            Tp = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_d"):
            d = self.defaultValue_d
        else:
            d = caseInputList[currIndex]

        return Hmo, Tp, d
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Hmo, Tp, d = self.getCalcValues(caseInputList)
        dataDict = {"Hmo": Hmo, "Tp": Tp, "d": d}

        Htype = []
        Htype.append(0.50) #Hmed;
        Htype.append(0.66) #H1/3 (1-1/3);
        Htype.append(0.90) #H1/10 (1-1/10);
        Htype.append(0.99) #H1/100 (1-1/100);

        Hb = ERRWAVBRK1(d, 0.9)
        if Hmo >= Hb:
            self.errorMsg =\
                "Error: Input wave broken (Hb = %6.2f %s)" % (Hb, self.labelUnitDist)

            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        L, k = WAVELEN(d, Tp, 50, self.g)
        steep, maxstp = ERRSTP(Hmo, d, L)
        if steep >= maxstp:
            self.errorMsg =\
                "Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)" % (maxstp, steep)

            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        dterm = d/(self.g*Tp**2)
        k = 0
        sum1 = 0

        if dterm > 0.01:
            print("Input conditions indicate Rayleigh distribution")
            Hb = math.sqrt(5)*Hmo
            Hinc = Hb/10000
            sigma = Hmo/4
            Hrms = 2*math.sqrt(2)*sigma

            H = [0]
            p = [0]
            index = [0, 0, 0, 0]
            for i in range(2, 10002):
                # Rayleigh distribution
                H.append(Hinc * (i - 1))
                term1 = math.exp(-(H[i - 1]/Hrms)**2)
                term2 = (2 * H[i - 1])/Hrms**2
                p.append(term1 * term2)

                sum1 = sum1 + (p[i - 1]*Hinc)
                if k < 4 and sum1 > Htype[k]:
                    index[k] = i
                    k = k + 1

            Hout = []
            for k in range(1, 4):
                sum2 = 0
                Hstart = H[index[k]]
                Hinc = (Hb - Hstart)/10000
                pprv = p[index[k]]
                Hprv = Hstart

                for i in range(2, 10001):
                    Hnxt = Hstart + Hinc*(i - 1)
                    term1 = math.exp(-(Hnxt/Hrms)**2)
                    term2 = (2 * Hnxt)/Hrms**2
                    pnxt = term1 * term2
                    darea = 0.5*(pprv + pnxt)*Hinc # area of a trapezoid
                    sum2 = sum2 + (Hinc/2.0 + Hprv)*darea
                    pprv = pnxt
                    Hprv = Hnxt
                Hout.append(sum2 / (1 - Htype[k])) # computing centroid (areasum = 1-Htype)
        else:
            Hb = d
            Hinc = Hb / 100
            print("Input conditions indicate Beta-Rayleigh distribution")
            a1 = 0.00089
            b1 = 0.834
            a2 = 0.000098
            b2 = 1.208

            d1 = a1*dterm**(-b1)
            if d1 > 35.0:
                self.errorMsg = "Error: d/gT^2 approaching infinity"

                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            Hrms = (1/math.sqrt(2))*math.exp(d1)*Hmo # root-mean-square wave height

            d2 = a2 * dterm**(-b2)
            if d2 > 35.0:
                self.errorMsg = "Error: d/gT^2 approaching infinity"

                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            Hrmsq = (1/math.sqrt(2))*math.exp(d2)*Hmo**2 # root-mean-quad wave height

            # Computing alpha and beta
            K1 = (Hrms / Hb)**2
            K2 = (Hrmsq**2) / (Hb**4)

            alpha = (K1*(K2 - K1))/(K1**2 - K2)
            beta = ((1 - K1)*(K2 - K1))/(K1**2 - K2)

            term1 = (2*sp.gamma(alpha + beta))/(sp.gamma(alpha)*sp.gamma(beta))

            H = []
            p = []
            index = [0, 0, 0, 0]
            for i in range(101):
                # Beta-Rayleigh distribution
                H.append(Hinc*i)
                term2 = (H[i]**(2*alpha - 1))/(Hb**(2*alpha))
                term3 = (1 - (H[i]/Hb)**2)**(beta - 1)
                p.append(term1 * term2 * term3)

                sum1 = sum1 + (p[i]*Hinc)
                if k < 4 and sum1 > Htype[k]:
                    index[k] = i
                    k = k + 1

            Hout = []
            for k in range(1, 4):
                sum2 = 0
                Hstart = H[index[k]]
                Hinc = (Hb - Hstart)/20
                pprv = p[index[k]]
                Hprv = Hstart

                for i in range(1, 20):
                    Hnxt = Hstart + Hinc*i
                    term2 = (Hnxt**(2*alpha - 1))/(Hb**(2*alpha))
                    term3 = (1 - (Hnxt/Hb)**2)**(beta - 1)
                    pnxt = term1*term2*term3
                    darea = 0.5*(pprv + pnxt)*Hinc # area of a trapezoid
                    sum2 = sum2 + (Hinc/2.0 + Hprv)*darea
                    pprv = pnxt
                    Hprv = Hnxt

                Hout.append(sum2 / (1 - Htype[k])) # computing centroid (areasum = 1-Htype)

        Hmed = H[index[0]]

        print("Wave heights")
        print("Hrms\t\t%6.2f %s" % (Hrms, self.labelUnitDist))
        print("Hmed\t\t%6.2f %s" % (Hmed, self.labelUnitDist))
        print("H(1/3)\t\t%6.2f %s" % (Hout[0], self.labelUnitDist))
        print("H(1/10)\t\t%6.2f %s" % (Hout[1], self.labelUnitDist))
        print("H(1/100)\t%6.2f %s" % (Hout[2], self.labelUnitDist))

        dataDict["Hrms"] = Hrms
        dataDict["Hmed"] = Hmed
        dataDict["Hout"] = Hout
        self.fileOutputWriteMain(dataDict, caseIndex)

        if self.isSingleCase:
            self.plotDict = {"Hrms": Hrms, "Hmed": Hmed, "Hout": Hout,\
                "H": H, "p": p}
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("Hmo       %8.2f %s\n" % (dataDict["Hmo"], self.labelUnitDist))
        self.fileRef.write("Tp        %8.2f s\n" % (dataDict["Tp"]))
        self.fileRef.write("d         %8.2f %s\n\n" % (dataDict["d"], self.labelUnitDist))

        if self.errorMsg != None:
            self.fileRef.write("%s\n" % self.errorMsg)
        else:
            self.fileRef.write("Wave heights\n")
            self.fileRef.write("Hrms      %8.2f %s\n" % (dataDict["Hrms"], self.labelUnitDist))
            self.fileRef.write("Hmed      %8.2f %s\n" % (dataDict["Hmed"], self.labelUnitDist))
            self.fileRef.write("H(1/3)    %8.2f %s\n" % (dataDict["Hout"][0], self.labelUnitDist))
            self.fileRef.write("H(1/10)   %8.2f %s\n" % (dataDict["Hout"][1], self.labelUnitDist))
            self.fileRef.write("H(1/100)  %8.2f %s\n" % (dataDict["Hout"][2], self.labelUnitDist))

        exportData = [dataDict["Hmo"], dataDict["Tp"], dataDict["d"]]
        if self.errorMsg != None:
            exportData.append(self.errorMsg)
        else:
            exportData = exportData + [dataDict["Hrms"], dataDict["Hmed"],\
                dataDict["Hout"][0], dataDict["Hout"][1], dataDict["Hout"][2]]
        self.exporter.writeData(exportData)
    # end fileOutputWrite

    def hasPlot(self):
        return True

    def performPlot(self):
        plt.figure(1, figsize = self.plotConfigDict["figSize"],\
            dpi = self.plotConfigDict["dpi"])
        plt.plot(self.plotDict["Hout"][0], 0, "ks",\
            self.plotDict["Hout"][1], 0, "ro",\
            self.plotDict["Hout"][2], 0, "bd",\
            self.plotDict["Hrms"], 0, "g*",\
            self.plotDict["Hmed"], 0, "m^",\
            self.plotDict["H"], self.plotDict["p"])
        plt.xlabel("H [%s]" % self.labelUnitDist,\
            fontsize = self.plotConfigDict["axisLabelFontSize"])
        plt.ylabel("Probability density p(H)",\
            fontsize = self.plotConfigDict["axisLabelFontSize"])
        plt.legend([r"H$_{1/3}$", r"H$_{1/10}$", r"H$_{1/100}$",\
            r"H$_{rms}$", r"H$_{med}$"])

        plt.show()

        self.fileOutputPlotWriteData()
    # end performPlot

    def fileOutputPlotWriteData(self):
        self.fileRef.write("Counter\tWave height\tProbability density\n")

        for i in range(len(self.plotDict["H"])):
            self.fileRef.write("%d\t%-6.5f\t\t%-6.5f\n" %\
                ((i + 1), self.plotDict["H"][i], self.plotDict["p"][i]))
    # end fileOutputPlotWriteData


driver = BetaRayleigh()