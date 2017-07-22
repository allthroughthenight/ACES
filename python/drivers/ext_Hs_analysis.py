import sys
import math
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK1 import ERRWAVBRK1
from WAVELEN import WAVELEN

## ACES Update to MATLAB
#-------------------------------------------------------------
# Driver for Extremal Significant Wave Height Analysis (page 1-3 of ACES
# User's Guide). Provide significant wave height estimates for various
# return periods.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: May 13, 2011
# Date Verified: June 18, 2012

# Requires the following functions:
# ERRWAVBRK1

# MAIN VARIABLE LIST:
#   INPUT
#   Nt: estimated total number of events from the population during the
#       length of the record
#   K: length of the record in years
#   d: water depth
#   Hs: significant wave heights from long-term data source

#   OUTPUT
#   Hsr: significant wave height with return period Tr
#   sigr: standard deviation of significant wave height
#   pe: probability that a height with given return period will be equaled
#       or exceeded during some time period

#   OTHERS
#   yact: probability as estimated by the plotting forumula
#   yest: probability as estimated by the distribution
#   signr: normalized standard deviation of significant wave height with
#       return period Tr
#-------------------------------------------------------------

class ExtHsAnalysis(BaseDriver):
    def __init__(self, Nt = None, K = None, d = None,\
        Hs = None, option = None):
        self.isSingleCase = True

        if Nt != None:
            self.defaultValueNt = Nt
        if K != None:
            self.defaultValueK = K
        if d != None:
            self.defaultValue_d = d
        if Hs != None:
            self.defaultValueHs = Hs
        if option != None:
            self.defaultValue_option = option

        super(ExtHsAnalysis, self).__init__()
    # end __init__

    def userInput(self):
        super(ExtHsAnalysis, self).userInput()

        if not hasattr(self, "defaultValueHs"):
            hsCount = USER_INPUT.DATA_VALUE(\
                "the number of significant wave heights", 1, 200)
            hsCount = int(hsCount)

            self.Hs = []
            for i in range(hsCount):
                self.Hs.append(USER_INPUT.DATA_VALUE(\
                    "significant wave height [%s] #%d" %\
                    (self.labelUnitDist, (i + 1)),\
                    0.0, 100.0))
        else:
            self.Hs = self.defaultValueHs

        if not hasattr(self, "defaultValue_option"):
            self.option = USER_INPUT.FINITE_CHOICE(\
                "Confidence intervals:\n[1] 80%\n[2] 85%\n[3] 90%\n[4] 95%\n[5] 99%\nSelect option: ",\
                ["1", "2", "3", "4", "5"])
            self.option = int(self.option)
        else:
            self.option = self.defaultValue_option
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueNt"):
            self.inputList.append(BaseField(\
                "Nt: estimated total number of events",  0.0, 10000.0))

        if not hasattr(self, "defaultValueK"):
            self.inputList.append(BaseField(\
                "K: length of the record in years", 0.0, 999.9))

        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField(\
                "d: water depth [%s]" % (self.labelUnitDist), 0.0, 1000.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "ext_Hs_analysis")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueNt"):
            Nt = self.defaultValueNt
        else:
            Nt = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueK"):
            K = self.defaultValueK
        else:
            K = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_d"):
            d = self.defaultValue_d
        else:
            d = caseInputList[currIndex]

        return Nt, K, d
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Nt, K, d = self.getCalcValues(caseInputList)

        N = len(self.Hs)
        lambdaVal = Nt / K
        nu = N / Nt

        self.Hs = [i / 0.3048 for i in self.Hs]
        d = d / 0.3048

        Hb = ERRWAVBRK1(d, 0.78)
        for j in self.Hs:
            if not (j < Hb):
                print("Error: Input wave broken (Hb = %6.2f %s)" %\
                    (Hb, self.labelUnitDist))
                return

        ret = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,\
            2.0, 5.0, 10.0, 25.0, 50.0, 100.0]

        #Coefficients
        k_W = [0.75, 1.00, 1.40, 2.00]
        a1 = [0.64, 1.65, 1.92, 2.05, 2.24]
        a2 = [9.0, 11.4, 11.4, 11.4, 11.4]
        kappa = [0.93, -0.63, 0.00, 0.69, 1.34]
        c = [0.0, 0.0, 0.3, 0.4, 0.5]
        epsi = [1.33, 1.15, 0.90, 0.72, 0.54]

        pret = [1.0, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0]
        plen = pret

        self.Hs.sort()
        self.Hs.reverse()

        yact = [[0.0 for j in range(5)] for i in range(N)]
        ym = [[0.0 for j in range(5)] for i in range(N)]
        for j in range(N):
            yact[j][0] = 1.0 - ((j + 1) - 0.44)/(Nt + 0.12) #FT-I
            ym[j][0] = -math.log(-math.log(yact[j][0]))

            for m in range(1, 5):
                k = k_W[m - 1] #Weibull
                yact[j][m] = 1.0 - ((j + 1) - 0.2 - 0.27/math.sqrt(k))/\
                    (Nt + 0.2 + 0.23/math.sqrt(k))
                ym[j][m] = (-math.log(1.0 - yact[j][m]))**(1.0/k)
        # end for loop

        Sx = sum(self.Hs)
        Sy = [sum([yact[j][m] for j in range(N)]) for m in range(5)]
        Sxx = sum([i**2 for i in self.Hs])
        Slly = [sum([ym[j][m] for j in range(N)]) for m in range(5)]
        Syy = [sum([ym[j][m]**2 for j in range(N)]) for m in range(5)]

        Sxy = [[0.0 for j in range(5)] for i in range(N)]
        for j in range(N):
            for m in range(5):
                Sxy[j][m] = self.Hs[j]*ym[j][m]
        Sxy = [sum([Sxy[j][m] for j in range(N)]) for m in range(5)]

        alpha = []
        beta = []
        for m in range(5):
            alpha.append((N*Sxy[m] - Sx*Slly[m])/(N*Syy[m] - Slly[m]**2))
            beta.append((1.0/N)*(Sx - alpha[m]*Slly[m]))

        print("--------------")

        yest = []
        for j in range(N):
            yest.append([])
            yest[j].append(\
                math.exp(-math.exp(-(self.Hs[j] - beta[0])/alpha[0]))) #FT-I

            for m in range(1, 5):
                k = k_W[m - 1] #Weibull
                if (self.Hs[j] - beta[m])/alpha[m] >= 0.0:
                    yest[j].append(\
                        1.0 - math.exp(-((self.Hs[j] - beta[m])/alpha[m])**k))
                else:
                    yest[j].append(0.0)

        st = []
        for j in range(N):
            st.append([])
            for m in range(5):
                st[j].append((yact[j][m] - yest[j][m])**2)

        # sumresid = sum(st)/0.3048
        sumresid = [sum([st[j][m] for j in range(N)]) for m in range(5)]
        sumresid = [i/0.3048 for i in sumresid] #sum square of residuals

        rxy = []
        for m in range(5):
            numer = N*Sxy[m] - Sx*Slly[m]
            term1d = N*Sxx - Sx**2
            term2d = N*Syy[m] - Slly[m]**2
            rxy.append(numer/(math.sqrt(term1d*term2d))) #correlation coefficient

        yr = [[0.0 for m in range(5)] for j in range(len(ret))]
        Hsr = [[0.0 for m in range(5)] for j in range(len(ret))]
        for j in range(len(ret)):
            prob1 = 1.0 - 1.0/(lambdaVal*ret[j])

            if prob1 <= 0.0:
                prob1 = 1.0*10**(-7)

            yr[j][0] = -math.log(-math.log(prob1)) #FT-I
            Hsr[j][0] = alpha[0]*yr[j][0] + beta[0]

            for m in range(1, 5):
                prob2 = lambdaVal*ret[j]
                if prob2 <= 0.0:
                    prob2 = 1.0*10**(-7)

                k = k_W[m - 1] #Weibull
                yr[j][m] = math.log(prob2)**(1.0/k)
                Hsr[j][m] = alpha[m]*yr[j][m] + beta[m]
        # end for loop

        rtp = []
        for j in range(N):
            rtp.append([])
            rtp[j].append(\
                1.0/((1.0 - math.exp(-math.exp(-ym[j][0])))*lambdaVal)) #FT-I

            for m in range(1, 5):
                k = k_W[m - 1] #Weibull
                rtp[j].append(math.exp(ym[j][m]**k)/lambdaVal)
        # end for loop

        standev = np.std(self.Hs, ddof=1) #standard deviation

        #Calculate confidence intervals
        sigr = [[0.0 for m in range(5)] for j in range(len(ret))]
        for m in range(5):
            coeff = a1[m]*math.exp(a2[m]*N**(-1.3) + kappa[m]*math.sqrt(-math.log(nu)))

            for j in range(len(ret)):
                signr = (1.0/math.sqrt(N))*(1.0 + coeff*(yr[j][m] - c[m] + epsi[m]*math.log(nu))**2)**(0.5)
                sigr[j][m] = signr*standev
        # end for loop

        if self.option == 1: #80%
            bounds = [[j*1.28 for j in i] for i in sigr]
            conf = 80
        elif self.option == 2: #85%
            bounds = [[j*1.44 for j in i] for i in sigr]
            conf = 85
        elif self.option == 3: #90%
            bounds = [[j*1.65 for j in i] for i in sigr]
            conf = 90
        elif self.option == 4: #95%
            bounds = [[j*1.96 for j in i] for i in sigr]
            conf = 95
        elif self.option == 5: #99%
            bounds = [[j*2.58 for j in i] for i in sigr]
            conf = 99

        lowbound = []
        highbound = []
        for j in range(len(Hsr)):
            lowbound.append([])
            highbound.append([])

            for m in range(5):
                lowbound[j].append(Hsr[j][m] - bounds[j][m])
                highbound[j].append(Hsr[j][m] + bounds[j][m])

        #Calculated percent chance for significant wave height
        #equaling or exceeding the return period
        pe = [[0.0 for j in range(7)] for i in range(7)]
        for i in range(7):
            for j in range(7):
                pe[j][i] = 100.0*(1.0 - (1.0 - 1.0/pret[j])**plen[i])

        xxr = []
        for i in range(N):
            xxr.append([])

            for m in range(5):
                xxr[i].append(ym[i][m]*alpha[m] + beta[m])

        print(pe)
        printpe = [[j for j in i] for i in pe]
        printside = [2, 5, 10, 25, 50, 100]
        printpe[0][0] = 999
        for i in range(1, len(printpe)):
            printpe[i][0] = printside[i - 1]
        for j in range(1, len(printpe[0])):
            printpe[0][j] = printside[j - 1]

        indexList = [ret.index(2.0), ret.index(5.0), ret.index(10.0),\
            ret.index(25.0), ret.index(50.0), ret.index(100.0)]

        print("N = %-i NU = %-3.2f NT = %-i K = %-3.2f lambda = %-3.2f\n" %\
            (N, nu, Nt, K, lambdaVal))
        print("\t\tFT-I\tW (k=0.75)  W (k=1.00)  W (k=1.40)  W (k=2.00)")
        print("Corr. coeff.\t%-12.4f%-12.4f%-12.4f%-12.4f%-12.4f" %\
            (rxy[0], rxy[1], rxy[2], rxy[3], rxy[4]))
        print("Sq. of Resid.\t%-12.4f%-12.4f%-12.4f%-12.4f%-12.4f\n" %\
            (sumresid[0], sumresid[1], sumresid[2], sumresid[3], sumresid[4]))

        print("Return period\tHs [%s]   Hs [%s]   Hs [%s]   Hs [%s]   Hs [%s]" %\
            (self.labelUnitDist, self.labelUnitDist, self.labelUnitDist, self.labelUnitDist, self.labelUnitDist))
        for m in range(6):
            print("%-i\t\t%-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" %\
                (ret[indexList[m]], Hsr[indexList[m]][0], Hsr[indexList[m]][1],\
                Hsr[indexList[m]][2], Hsr[indexList[m]][3], Hsr[indexList[m]][4]))

        val = max(rxy)
        C = rxy.index(val)
        if C == 0:
            print("\nBest fit distribution function: Fisher-Tippett Type I\n")
        elif C == 1:
            print("\nBest fit distribution function: Weibull Distribution (k=0.75)\n")
        elif C == 2:
            print("\nBest fit distribution function: Weibull Distribution (k=1.00)\n")
        elif C == 3:
            print("\nBest fit distribution function: Weibull Distribution (k=1.40)\n")
        elif C == 4:
            print("\nBest fit distribution function: Weibull Distribution (k=2.00)\n")

        print("%i%% Confidence Interval, (Lower Bound - Upper Bound)\nReturn period" % conf)
        print("\tFT-I          W (k=0.75)    W (k=1.00)    W (k=1.40)    W (k=2.00)")

        for m in range(6):
            print("%-i\t%-3.1f - %-3.1f   %-3.1f - %-3.1f   %-3.1f - %-3.1f   %-3.1f - %-3.1f   %-3.1f - %-3.1f" %\
                (ret[indexList[m]], lowbound[indexList[m]][0], highbound[indexList[m]][0],\
                lowbound[indexList[m]][1], highbound[indexList[m]][1],
                lowbound[indexList[m]][2], highbound[indexList[m]][2],
                lowbound[indexList[m]][3], highbound[indexList[m]][3],
                lowbound[indexList[m]][4], highbound[indexList[m]][4]))

        print("\nPercent Chance for Significant Height Equaling or Exceeding Return Period Hs")
        for i in range(len(printpe)):
            printLine = ""

            for j in range(len(printpe[0])):
                if i == 0 and j == 0:
                    printLine += "      "
                elif i == 0:
                    printLine += "%6d" % printpe[i][j]
                else:
                    printLine += "%6d" % round(printpe[i][j])

            print(printLine)
        # end for loop

        dataDict = {"Nt": Nt, "K": K, "d": d, "N": N, "nu": nu,\
            "lambdaVal": lambdaVal, "Sx": Sx, "standev": standev,\
            "alpha": alpha, "beta": beta, "rxy": rxy,\
            "sumresid": sumresid, "yact": yact, "ym": ym,\
            "xxr": xxr, "conf": conf, "Hsr": Hsr, "sigr": sigr,\
            "printside": printside, "indexList": indexList}
        self.fileOutputWriteMain(dataDict)

        self.plotDict = {"ret": ret, "Hsr": Hsr, "rtp": rtp,\
            "highbound": highbound, "lowbound": lowbound}
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        distList = ["FISHER-TIPPETT TYPE (FT-I) DISTRIBUTION",\
            "WEIBULL DISTRIBUTION k = 0.75",\
            "WEIBULL DISTRIBUTION k = 1.00",\
            "WEIBULL DISTRIBUTION k = 1.40",\
            "WEIBULL DISTRIBUTION k = 2.00"]

        self.fileRef.write("EXTREMAL SIGNIFICANT WAVE HEIGHT ANALYSIS\n")
        self.fileRef.write("DELFT Data\n\n")

        self.fileRef.write("N = %d STORMS\n" % dataDict["N"])
        self.fileRef.write("NT = %d STORMS\n" % dataDict["Nt"])
        self.fileRef.write("NU = %-6.2f\n" % dataDict["nu"])
        self.fileRef.write("K = %-6.2f YEARS\n" % dataDict["K"])
        self.fileRef.write("LAMBDA = %-6.2f STORMS PER YEAR\n" % dataDict["lambdaVal"])
        self.fileRef.write("MEAN OF SAMPLE DATA = %-6.3f FEET\n" % (dataDict["Sx"]/dataDict["N"]))
        self.fileRef.write("STANDARD DEVIATION OF SAMPLE = %-6.3f FEET\n" % dataDict["standev"])

        for distIndex in range(len(distList)):
            self.fileRef.write("\n%s\n" % distList[distIndex])
            self.fileRef.write("F(Hs) = EXP(-EXP(-(Hs-B)/A)) - Equation 1\n")
            self.fileRef.write("A = %-6.3f %s\n" % (dataDict["alpha"][distIndex], self.labelUnitDist))
            self.fileRef.write("B = %-6.3f %s\n" % (dataDict["beta"][distIndex], self.labelUnitDist))
            self.fileRef.write("CORRELATION = %-6.4f\n" % dataDict["rxy"][distIndex])
            self.fileRef.write("SUM SQUARE OF RESIDUALS = %-6.4f %s\n" %\
                (dataDict["sumresid"][distIndex], self.labelUnitDist))

            self.fileRef.write("\nRANK\tHsm\tF(Hs<=Hsm)\tYm\tA*Ym+B\t\tHsm-(A*Ym+B)\n")
            self.fileRef.write("\t(Ft)\tEq. 3\t\tEq. 5\tEq. 4 (%s)\t(%s)\n" %\
                (self.labelUnitDist, self.labelUnitDist))

            for loopIndex in range(len(self.Hs)):
                self.fileRef.write("%d\t%-6.2f\t%-6.4f\t\t%-6.3f\t%-6.4f\t\t%-6.4f\n" %\
                    ((loopIndex + 1),\
                    self.Hs[loopIndex],\
                    dataDict["yact"][loopIndex][distIndex],\
                    dataDict["ym"][loopIndex][distIndex],\
                    dataDict["xxr"][loopIndex][distIndex],\
                    (self.Hs[loopIndex] - dataDict["xxr"][loopIndex][distIndex])))

            self.fileRef.write("\nRETURN PERIOD TABLE with %d%% CONFIDENCE INTERVAL\n" % dataDict["conf"])

            self.fileRef.write("\nRETURN\tHs\tSIGR\tHs-1.28*SIGR\tHs+1.28*SIGR\n")
            self.fileRef.write("PERIOD\t(%s)\t(%s)\t(%s)\t\t(%s)\n" %\
                (self.labelUnitDist, self.labelUnitDist, self.labelUnitDist, self.labelUnitDist))
            self.fileRef.write("(Yr)\tEq. 6\tEq. 10\n")

            for loopIndex in range(len(dataDict["indexList"])):
                self.fileRef.write("%-6.2f\t%-6.2f\t%-6.2f\t%-6.2f\t\t%-6.2f\n" %\
                    (dataDict["printside"][loopIndex],\
                    dataDict["Hsr"][dataDict["indexList"][loopIndex]][distIndex],\
                    dataDict["sigr"][dataDict["indexList"][loopIndex]][distIndex],\
                    dataDict["Hsr"][dataDict["indexList"][loopIndex]][distIndex] - 1.28*dataDict["sigr"][dataDict["indexList"][loopIndex]][distIndex],\
                    dataDict["Hsr"][dataDict["indexList"][loopIndex]][distIndex] + 1.28*dataDict["sigr"][dataDict["indexList"][loopIndex]][distIndex]))
    # end fileOutputWrite

    def hasPlot(self):
        return True

    def performPlot(self):
        for i in range(5):
            plt.figure((i + 1), figsize = self.plotConfigDict["figSize"],\
                dpi = self.plotConfigDict["dpi"])

            plotDataHsr = [j[i] for j in self.plotDict["Hsr"]]
            plotDataRtp = [j[i] for j in self.plotDict["rtp"]]
            plotDataHighbound = [j[i] for j in self.plotDict["highbound"]]
            plotDataLowbound = [j[i] for j in self.plotDict["lowbound"]]
            plt.semilogx(\
                self.plotDict["ret"], plotDataHsr, ":",\
                plotDataRtp, self.Hs,\
                self.plotDict["ret"], plotDataHighbound, "r--",\
                self.plotDict["ret"], plotDataLowbound, "r--")

            if i == 0:
                plotTitle = "FT-I"
                plotLegend = "FT-I Distribution"
            elif i == 1:
                plotTitle = "Weibull (k=0.75)"
                plotLegend = "Weibull (k=0.75)"
            elif i == 2:
                plotTitle = "Weibull (k=1.00)"
                plotLegend = "Weibull (k=1.00)"
            elif i == 3:
                plotTitle = "Weibull (k=1.40)"
                plotLegend = "Weibull (k=1.40)"
            elif i == 4:
                plotTitle = "Weibull (k=2.00)"
                plotLegend = "Weibull (k=2.00)"

            plt.title(plotTitle,\
                fontsize = self.plotConfigDict["titleFontSize"])
            plt.xlabel("Return period [yr]",\
                fontsize = self.plotConfigDict["axisLabelFontSize"])
            plt.ylabel(r"H$_s$",\
                fontsize = self.plotConfigDict["axisLabelFontSize"])
            plt.legend([plotLegend, "Data", "Confidence Bounds",\
                "Location", "SouthEast"])
        # end for loop

        plt.show()
    # end performPlot

    # Override to prevent creating additional output file
    def fileOutputPlotInit(self):
        pass


driver = ExtHsAnalysis()