import sys
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRWAVBRK1 import ERRWAVBRK1

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Cnoidal Wave Theory (page 2-2 in ACES User's Guide)
# Yields first-order and second-order approximations for various wave
# parameters of wave motion as predicted by cnoidal wave theory

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: March 18, 2011
# Date Modified:7/21/16 -yaprak

# Requires the following functions:
# ERRWAVBRK1

# MAIN VARIABLE LIST:
#   INPUT
#   H: wave height (m)
#   T: wave period (sec)
#   d: water depth (m)
#   z: vertical coordinate (m)
#   xL: horizontal coordinate as fraction of wavelength (x/L)
#   time: time-coordinate (default=0)
#   O: order approximation (1 or 2)

#   OUTPUT
#   L: wavelength (m)
#   C: wave celerity (m/s)
#   E: energy density (N-m/m^2)
#   Ef: energy flux (N-m/m-s)
#   Ur: Ursell number
#   eta: surface elevation (m)
#   u: horizontal particle velocity (m/s)
#   w: vertical particle velocity (m/s)
#   dudt: horizontal particle acceleration (m/s^2)
#   dwdt: vertical particle accleration (m/s^2)
#   pres: pressure (N/m^2)

#   OTHERS
#   K: complete elliptic intergral of the first kind
#   E: complete elliptical intergral of the second kind
#   m: optimized parameter
#   lambda: simplification term ((1-m)/m)
#   mu: simplification term (E/(K*m))git
#   epsi: perturbation parameter (H/d)
#-------------------------------------------------------------

class CnoidalWaveTheory(BaseDriver):
    def __init__(self, H = None, T = None, d = None, z = None, xL = None,\
        O = None):
        self.exporter = EXPORTER("output/exportCnoidalWaveTheory.txt")

        if H != None:
            self.isSingleCase = True
            self.defaultValueH = H
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d
        if z != None:
            self.isSingleCase = True
            self.defaultValue_z = z
        if xL != None:
            self.isSingleCase = True
            self.defaultValue_xL = xL
        if O != None:
            self.isSingleCase = True
            self.defaultValue_O = O
            
        super(CnoidalWaveTheory, self).__init__()

        self.exporter.close()
    # end __init__

    def userInput(self):
        super(CnoidalWaveTheory, self).userInput()

        self.waterType, self.rho =\
            USER_INPUT.SALT_FRESH_WATER(self.isMetric)

#        self.O = USER_INPUT.FINITE_CHOICE(\
#            "Enter O: order approximation (1 or 2): ",\
#            ["1", "2"])
#        self.O = int(self.O)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueH"):
            self.inputList.append(BaseField(\
                "H: wave height (%s)" % self.labelUnitDist, 0.1, 200.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField(\
                "T: wave period (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField(\
                "d: water depth (%s)" % self.labelUnitDist, 0.1, 5000.0))
        if not hasattr(self, "defaultValue_z"):
            self.inputList.append(BaseField(\
                "z: vertical coordinate (%s)" % self.labelUnitDist,\
                -5100.0, 100.0))
        if not hasattr(self, "defaultValue_xL"):
            self.inputList.append(BaseField(\
                "xL: horizontal coordinate as fraction of wavelength (x/L)",\
                0.0, 1.0))
        if not hasattr(self, "defaultValue_O"):
            self.inputList.append(BaseField(\
                "O: order approximation (1 or 2)",\
                1.0, 2.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(requestDesc = True)

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

        if hasattr(self, "defaultValue_d"):
            d = self.defaultValue_d
        else:
            d = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_z"):
            z = self.defaultValue_z
        else:
            z = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_xL"):
            xL = self.defaultValue_xL
        else:
            xL = caseInputList[currIndex]
            currIndex = currIndex + 1
            
        if hasattr(self, "defaultValue_O"):
            O = self.defaultValue_O
        else:
            O = caseInputList[currIndex]
            currIndex = currIndex + 1
        O = int(O)

        return H, T, d, z, xL, O
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, d, z, xL, O = self.getCalcValues(caseInputList)
        dataDict = {"H": H, "T": T, "d": d, "z": z, "xL": xL, "O": O}
        
        time = 0

        epsi = H/d

        Hb = ERRWAVBRK1(d, 0.78)
        if not (H < Hb):
            self.errorMsg = "Error: Input wave broken (Hb = %6.2f %s)" %\
                (Hb, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return

        # First Order Approximation
        if O == 1: #determining m using bisection method
            a = 1.0*10**-12
            b = 1.0-10**-12
            while (b - a)/2.0 >= 0.00001:
                xi = (a + b) / 2.0
                if self.F1(xi, H, T, d) == 0:
                    break
                else:
                    if self.F1(xi, H, T, d)*self.F1(b, H, T, d) < 0.0:
                        a = xi
                    elif self.F1(xi, H, T, d)*self.F1(a, H, T, d) < 0.0:
                        b = xi
            # end while loop

            m = xi

            K = sp.ellipk(m)
            E = sp.ellipe(m)

            lambdaVal = (1 - m) / m
            mu = E/(m*K)
            theta = 2.0*K*(xL-(time/T))

            C0 = 1.0
            C1 = (1.0 + 2.0*lambdaVal - 3.0*mu)/2.0
            C = math.sqrt(self.g*d)*(C0 + epsi*C1) # celerity

            L = C*T # wave length

            Ur = (H*(L**2))/(d**3)
            if not (Ur > 26.0):
                self.errorMsg = "Error: Ursell parameter test failed."
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            SN, CN, DN, PH = sp.ellipj(theta, m)
            CSD = CN*SN*DN

            A0 = epsi*(lambdaVal - mu)
            A1 = epsi
            eta = d*(A0 + A1*CN**2) # water surface elevation

            if not (z < eta and (z + d) > 0.0):
                self.errorMsg = "Error: Point outside waveform."
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            E0 = (-lambdaVal + 2.0*mu + 4.0*lambdaVal*mu - lambdaVal**2 - 3.0*mu**2)/3.0
            E = self.rho*self.g*H**2*E0 # average energy density

            F0 = E0
            Ef = self.rho*self.g*H**2*math.sqrt(self.g*d)*F0 # energy flux

            B00 = epsi*(lambdaVal - mu)
            B10 = epsi
            u = math.sqrt(self.g*d)*(B00 + B10*CN**2) # horizontal velocity

            w = math.sqrt(self.g*d)*(4.0*K*d*CSD/L)*((z + d)/d)*B10 # vertical velocity

            dudt = math.sqrt(self.g*d)*B10*(4.0*K/T)*CSD # horizontal acceleration

            term = math.sqrt(self.g*d)*(4*K*d/L)*((z + d)/d)*B10*(2.0*K/T)
            dwdt = term*((SN*DN)**2 - (CN*DN)**2 + (m*SN*CN)**2) # vertical acceleration

            P1 = (1.0 + 2.0*lambdaVal - 3.0*mu)/2.0
            P0 = 1.5
            Pb = self.rho*self.g*d*(P0 + epsi*P1)
            pres = Pb - (self.rho/2.0)*((u - C)**2 + w**2) - self.g*self.rho*(z + d) # pressure

            print("First Order Approximations")
        # Second Order Approximations
        else:
            a = 1.0*10**-12
            b = 1.0-10**-12

            while (b - a)/2.0 >= 0.00001:
                xi = (a + b)/2.0
                if self.F2(xi, H, T, d, epsi) == 0:
                    break
                else:
                    if self.F2(xi, H, T, d, epsi)*self.F2(b, H, T, d, epsi) < 0.0:
                        a = xi
                    elif self.F2(xi, H, T, d, epsi)*self.F2(a, H, T, d, epsi) < 0.0:
                        b = xi
            # end while loop

            m = xi

            K = sp.ellipk(m)
            E = sp.ellipe(m)

            lambdaVal = (1 - m) / m
            mu = E/(m*K)
            theta = 2.0*K*(xL-(time/T))

            SN, CN, DN, PH = sp.ellipj(theta, m)
            CSD = CN*SN*DN

            C2 = (-6.0 - 16.0*lambdaVal + 5.0*mu - 16.0*lambdaVal**2 + 10.0*lambdaVal*mu + 15.0*mu**2)/40.0
            C1 = (1.0 + 2.0*lambdaVal - 3.0*mu)/2.0
            C0 = 1.0
            C = math.sqrt(self.g*d)*(C0 + epsi*C1 + epsi**2*C2) #celerity

            L = C*T #wave length

            Ur = (H*(L**2))/(d**3)
            if not (Ur > 26.0):
                self.errorMsg = "Error: Ursell parameter test failed."
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            A2 = 0.75*epsi**2
            A1 = epsi - A2
            A0 = epsi*(lambdaVal - mu) +\
                epsi**2*((-2.0*lambdaVal + mu - 2.0*lambdaVal**2 + 2.0*lambdaVal*mu)/4.0)
            eta = d*(A0 + A1*CN**2 + A2*CN**4) #wave surface elevation

            if not (z < eta and (z + d) > 0.0):
                self.errorMsg = "Error: Point outside waveform."
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            E1 = (1.0/30.0)*(lambdaVal - 2.0*mu - 17.0*lambdaVal*mu +\
                3.0*lambdaVal**2 - 17.0*lambdaVal**2*mu +\
                2.0*lambdaVal**3 + 15.0*mu**3)
            E0 = (-lambdaVal + 2.0*mu + 4.0*lambdaVal*mu - lambdaVal**2 - 3.0*mu**2)/3.0
            E = self.rho*self.g*H**2*(E0 + epsi*E1) #average energy density

            F1 = (1.0/30.0)*(-4.0*lambdaVal + 8.0*mu +\
                53.0*lambdaVal*mu - 12*lambdaVal**2 - 60.0*mu**2 +\
                53.0*lambdaVal**2*mu - 120.0*lambdaVal*mu**2 -\
                8.0*lambdaVal**3 + 75.0*mu**3)
            F0 = E0
            Ef = self.rho*self.g*H**2*math.sqrt(self.g*d)*(F0 + epsi*F1) #energy flux

            term = (z + d)/d

            B21 = -4.5*epsi**2
            B11 = 3.0*epsi**2*(1 - lambdaVal)
            B01 = ((3.0*lambdaVal)/2.0)*epsi**2
            B20 = -(epsi**2)
            B10 = epsi + epsi**2*((1.0 - 6.0*lambdaVal + 2.0*mu)/4.0)
            B00 = epsi*(lambdaVal - mu) + epsi**2*((lambdaVal - mu - 2.0*lambdaVal**2 + 2.0*mu**2)/4.0)
            u = math.sqrt(self.g*d)*((B00 + B10*CN**2 + B20*CN**4) -\
                0.5*term**2*(B01 + B11*CN**2 + B21*CN**4)) #horizontal velocity

            w1 = term*(B10 + 2.0*B20*CN**2)
            w2 = (1.0/6.0)*term**3*(B11 + 2.0*B21*CN**2)
            w = math.sqrt(self.g*d)*(4.0*K*d*CSD/L)*(w1 - w2) #vertical velocity

            u1 = (B10 - 0.5*term**2*B11)*(4.0*K*CSD/T)
            u2 = (B20 - 0.5*term**2*B21)*(8.0*K*CN**2*CSD/T)
            dudt = math.sqrt(self.g*d)*(u1 + u2) #horizontal acceleration

            w1 = (8.0*K*CSD**2/T)*(term*B20 - (1.0/6.0)*term**3*B21)
            w2 = term*(B10 + 2.0*B20*CN**2)-(1.0/6.0)*term**3*(B11 + 2.0*B21*CN**2)
            w3 = (2.0*K/T)*((SN*DN)**2 - (CN*DN)**2 + (m*SN*CN)**2)
            dwdt = math.sqrt(self.g*d)*(4.0*K*d/L)*(w1 + w2*w3) #vertical acceleration

            P2 = (-1.0 - 16.0*lambdaVal + 15.0*mu - 16.0*lambdaVal**2 + 30*lambdaVal*mu)/40.0
            P1 = (1.0 + 2*lambdaVal - 3.0*mu)/2.0
            P0 = 1.5
            Pb = self.rho*self.g*d*(P0 + epsi*P1 + epsi**2*P2)
            pres = Pb - (self.rho/2.0)*((u - C)**2 + w**2) - self.g*self.rho*(z + d)

            print("Second Order Approximations")
        # end if

        print("Wavelength\t\t%-6.2f %s" % (L, self.labelUnitDist))
        print("Celerity\t\t%-6.2f %s/sec" % (C, self.labelUnitDist))
        print("Energy density\t\t%-8.2f %s-%s/%s^2" %\
            (E, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        print("Energy flux\t\t%-8.2f %s-%s/sec-%s" % (Ef, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        print("Ursell number\t\t%-6.2f" % Ur)
        print("Elevation\t\t%-6.2f %s" % (eta, self.labelUnitDist))
        print("Horz. velocity\t\t%-6.2f %s/sec" % (u, self.labelUnitDist))
        print("Vert. velocity\t\t%-6.2f %s/sec" % (w, self.labelUnitDist))
        print("Horz. acceleration\t%-6.2f %s/sec^2" % (dudt, self.labelUnitDist))
        print("Vert. acceleration\t%-6.2f %s/sec^2" % (dwdt, self.labelUnitDist))
        print("Pressure\t\t%-8.2f %s/%s^2" % (pres, self.labelUnitWt, self.labelUnitDist))

        dataDict["L"] = L
        dataDict["C"] = C
        dataDict["E"] = E
        dataDict["Ef"] = Ef
        dataDict["Ur"] = Ur
        dataDict["eta"] = eta
        dataDict["u"] = u
        dataDict["w"] = w
        dataDict["dudt"] = dudt
        dataDict["dwdt"] = dwdt
        dataDict["pres"] = pres
        self.fileOutputWriteMain(dataDict, caseIndex)

        if self.isSingleCase:
            self.plotDict = {"O": O, "K": K, "time": time, "T": T, "m": m,\
                "d": d, "A0": A0, "A1": A1, "B00": B00,\
                "B10": B10, \
                "z": z, "L": L}

            if O == 2:
                self.plotDict["A2"] = A2
                self.plotDict["B01"] = B01
                self.plotDict["B20"] = B20
                self.plotDict["B11"] = B11
                self.plotDict["B21"] = B21
    # end performCalculations

    def F1(self, m, H, T, d):
        return (16*m*sp.ellipk(m)**2/3)-(self.g*H*T**2/d**2)
    # end F1

    def F2(self, m, H, T, d, epsi):
        return (16*m*sp.ellipk(m)**2/3)-(self.g*H*T**2/d**2)*(1-epsi*((1.0 + 2.0*((1.0 - m)/m))/4.0))

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("Wave height\t\t\t%8.2f %s\n" %\
            (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("Wave period\t\t\t%8.2f s\n" % dataDict["T"])
        self.fileRef.write("Water depth\t\t\t%8.2f %s\n" %\
            (dataDict["d"], self.labelUnitDist))
        self.fileRef.write("Vertical coordinate\t\t%8.2f %s\n" %\
            (dataDict["z"], self.labelUnitDist))
        self.fileRef.write("Horizontal coordinate\t\t%8.2f\nas fraction of wavelength (x/L)\n" % dataDict["xL"])

        if self.errorMsg != None:
            self.fileRef.write("\n%s\n" % self.errorMsg)
        else:
            if dataDict["O"] == 1:
                self.fileRef.write("\nFirst Order Approximations\n")
            else:
                self.fileRef.write("\nSecond Order Approximations\n")
    
            self.fileRef.write("Wavelength\t\t%-6.2f %s\n" %\
                (dataDict["L"], self.labelUnitDist))
            self.fileRef.write("Celerity\t\t%-6.2f %s/sec\n" %\
                (dataDict["C"], self.labelUnitDist))
            self.fileRef.write("Energy density\t\t%-8.2f %s-%s/%s^2\n" %\
                (dataDict["E"], self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
            self.fileRef.write("Energy flux\t\t%-8.2f %s-%s/sec-%s\n" %\
                (dataDict["Ef"], self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
            self.fileRef.write("Ursell number\t\t%-6.2f\n" % dataDict["Ur"])
            self.fileRef.write("Elevation\t\t%-6.2f %s\n" %\
                (dataDict["eta"], self.labelUnitDist))
            self.fileRef.write("Horz. velocity\t\t%-6.2f %s/sec\n" %\
                (dataDict["u"], self.labelUnitDist))
            self.fileRef.write("Vert. velocity\t\t%-6.2f %s/sec\n" %\
                (dataDict["w"], self.labelUnitDist))
            self.fileRef.write("Horz. acceleration\t%-6.2f %s/sec^2\n" %\
                (dataDict["dudt"], self.labelUnitDist))
            self.fileRef.write("Vert. acceleration\t%-6.2f %s/sec^2\n" %\
                (dataDict["dwdt"], self.labelUnitDist))
            self.fileRef.write("Pressure\t\t%-8.2f %s/%s^2\n" %\
                (dataDict["pres"], self.labelUnitWt, self.labelUnitDist))
        
        
        exportData = [dataDict["H"], dataDict["T"], dataDict["d"],\
            dataDict["z"], dataDict["xL"], dataDict["O"]]
        if self.errorMsg != None:
            exportData.append("Error")
        else:
            exportData = exportData + [dataDict["L"], dataDict["C"],\
                dataDict["E"], dataDict["Ef"], dataDict["eta"],\
                dataDict["u"], dataDict["w"], dataDict["dudt"], dataDict["dwdt"],\
                dataDict["pres"]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData

    def hasPlot(self):
        return True

    def performPlot(self):
        #Plotting waveform
        plotxL = list(np.arange(-1, 1.001, 0.001))
        plottheta = [2*self.plotDict["K"]*\
            (i - (self.plotDict["time"]/self.plotDict["T"])) for i in plotxL]
        pSN, pCN, pDN, pPH = sp.ellipj(plottheta, self.plotDict["m"])
        pCSD = pSN*pCN*pDN

        if self.plotDict["O"] == 1:
            ploteta = self.plotDict["d"]*\
                (self.plotDict["A0"] + self.plotDict["A1"]*pCN**2)
            plotu = math.sqrt(self.g*self.plotDict["d"])*\
                (self.plotDict["B00"] + self.plotDict["B10"]*pCN**2)
            plotw = math.sqrt(self.g*self.plotDict["d"])*\
                (4.0*self.plotDict["K"]*self.plotDict["d"]*pCSD/self.plotDict["L"])*\
                ((self.plotDict["z"] + self.plotDict["d"])/self.plotDict["d"])*self.plotDict["B10"]
        else:
            ploteta = self.plotDict["d"]*(self.plotDict["A0"] +\
                self.plotDict["A1"]*pCN**2 + self.plotDict["A2"]*pCN**4)
            plotu = math.sqrt(self.g*self.plotDict["d"])*\
                ((self.plotDict["B00"] + self.plotDict["B10"]*pCN**2 +\
                self.plotDict["B20"]*pCN**4) -\
                0.5*((self.plotDict["z"] + self.plotDict["d"]) / self.plotDict["d"])**2 *\
                (self.plotDict["B01"] + self.plotDict["B11"]*pCN**2 + self.plotDict["B21"]*pCN**4))

            pw1 = ((self.plotDict["z"] + self.plotDict["d"])/self.plotDict["d"])*\
                (self.plotDict["B10"] + 2.0*self.plotDict["B20"]*pCN**2)
            pw2 = (1.0/6.0)*(((self.plotDict["z"] + self.plotDict["d"])/self.plotDict["d"])**3)*\
                (self.plotDict["B11"] + 2.0*self.plotDict["B21"]*pCN**2)
            plotw = math.sqrt(self.g*self.plotDict["d"])*\
                (4.0*self.plotDict["K"]*self.plotDict["d"]*pCSD/self.plotDict["L"])*(pw1 - pw2)
        # end if

        plt.figure(1, figsize=(8, 12), dpi=self.plotConfigDict["dpi"])

        plt.subplot(3, 1, 1)
        plt.plot(plotxL, ploteta)
        plt.axhline(y=0.0, color="r", LineStyle="--")
        plt.ylabel("Elevation [%s]" % self.labelUnitDist)

        plt.subplot(3, 1, 2)
        plt.plot(plotxL, plotu)
        plt.axhline(y=0.0, color="r", LineStyle="--")
        plt.ylabel("Velocity, u [%s/s]" % self.labelUnitDist)

        plt.subplot(3, 1, 3)
        plt.plot(plotxL, plotw)
        plt.axhline(y=0.0, color="r", LineStyle="--")
        plt.ylabel("Velocity, w [%s/s]" % self.labelUnitDist)
        plt.xlabel("x/L")

        plt.show()

        self.plotDict["plotxL"] = plotxL
        self.plotDict["ploteta"] = ploteta
        self.plotDict["plotu"] = plotu
        self.plotDict["plotw"] = plotw
        self.fileOutputPlotWriteData()
    # end performPlot

    def fileOutputPlotWriteData(self):
        self.fileRef.write(\
            "Partial Listing of Plot Output File 1 for %s\n\n" %\
            self.fileOutputData.fileDesc)

        self.fileRef.write(\
            "X/L\tETA (%s)\tU(%s/sec)\tW (%s/sec)\n" %\
            (self.labelUnitDist, self.labelUnitDist, self.labelUnitDist))

        for i in range(len(self.plotDict["plotxL"])):
            self.fileRef.write("%-6.3f\t%-6.3f\t\t%-6.3f\t\t%-6.3f\n" %\
                (self.plotDict["plotxL"][i],\
                self.plotDict["ploteta"][i],\
                self.plotDict["plotu"][i],\
                self.plotDict["plotw"][i]))
    # fileOutputPlotWriteData


driver = CnoidalWaveTheory()