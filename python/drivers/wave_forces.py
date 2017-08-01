import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
from helper_objects import ComplexUtil
import USER_INPUT
from ERRSTP import ERRSTP
from ERRWAVBRK1 import ERRWAVBRK1
from ERRWAVBRK2 import ERRWAVBRK2
from WAVELEN import WAVELEN
from WFVW1 import WFVW1
from WFVW2 import WFVW2
from WFVW3 import WFVW3
from WFVW4 import WFVW4

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Nonbreaking Wave Forces at Vertical Walls (page 4-3 of ACES
# User's Guide). Provides pressure distribution and resultant force and
# moment loading on a vertical wall caused by normally incident,  nonbreaking,
# regular waves as proposed by Sainflou (1928),  Miche (1944),  and Rundgren
# (1958).

# Updated by: Mary Anderson,  USACE-CHL-Coastal Processes Branch
# Date Created: May 17,  2011
# Date Verified: June 1,  2012

# Requires the following functions:
# ERRSTP
# ERRWAVBRK1
# ERRWAVBRK2
# WAVELEN
# WFVW1
# WFVW2
# WFVW3
# WFVW4

# MAIN VARIABLE LIST:
#   INPUT
#   d: depth for sea water level
#   Hi: incident wave height
#   T: wave period
#   chi: wave reflection coefficient
#   cotphi: cotangent of nearshore slope

#   OUTPUT
#   MR: array containing Miche-Rundgren integrated values
#       (1) particle height above bottom at crest
#       (2) integrated force at crest
#       (3) integrated moment about base at crest
#       (4) particle height above bottom at trough
#       (5) integrate force at trough
#       (6) integrated moment about bottom at trough
#   S: array containing Sainflou integrated values
#   MRintc: array containing Miche-Rundgren incremental values at crest
#       (1) particle height
#       (2) wave pressure
#       (3) hydrostatic pressure
#       (4) wave and hydrostatic pressure
#       (5) moment
#   MRintt: array containing Miche-Rundgren incremental values at trough
#   Sintc: array containing Sainflou incremental values at crest
#   Sintt: array containing Sainflou incremental values at trough
#-------------------------------------------------------------

class WaveForces(BaseDriver):
    def __init__(self, d = None, Hi = None, T = None, chi = None, cotphi = None):
        self.exporter = EXPORTER("output/exportWaveForces")

        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d
        if Hi != None:
            self.isSingleCase = True
            self.defaultValueHi = Hi
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if chi != None:
            self.isSingleCase = True
            self.defaultValue_chi = chi
        if cotphi != None:
            self.isSingleCase = True
            self.defaultValue_cotphi = cotphi

        super(WaveForces, self).__init__()

        self.exporter.close()
    # end __init__

    def userInput(self):
        super(WaveForces, self).userInput()
        
        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField("d: depth for sea water level (%s)" %\
                self.labelUnitDist, 0.1, 200.0))
        if not hasattr(self, "defaultValueHi"):
            self.inputList.append(BaseField("Hi: incident wave height (%s)" %\
                self.labelUnitDist, 0.1, 100.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField("T: wave period (s)", 1.0, 100.0))
        if not hasattr(self, "defaultValue_chi"):
            self.inputList.append(BaseField(\
                "chi: wave reflection coefficient", 0.9, 1.0))
        if not hasattr(self, "defaultValue_cotphi"):
            self.inputList.append(BaseField(\
                "cotphi: cotangent of nearshore slope", 5.0, 10000.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "wave_forces")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValue_d"):
            d = self.defaultValue_d
        else:
            d = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueHi"):
            Hi = self.defaultValueHi
        else:
            Hi = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueT"):
            T = self.defaultValueT
        else:
            T = caseInputList[currIndex]

        if hasattr(self, "defaultValue_chi"):
            chi = self.defaultValue_chi
        else:
            chi = caseInputList[currIndex]

        if hasattr(self, "defaultValue_cotphi"):
            cotphi = self.defaultValue_cotphi
        else:
            cotphi = caseInputList[currIndex]

        return d, Hi, T, chi, cotphi
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        d, Hi, T, chi, cotphi = self.getCalcValues(caseInputList)
        dataDict = {"d": d, "Hi": Hi, "T": T, "chi": chi, "cotphi": cotphi}
        
        H20weight = self.rho * self.g
        
        m = 1.0 / cotphi
        if np.isclose(m, 0.0):
            Hbs = ERRWAVBRK1(d, 0.78)
        else:
            Hbs = ERRWAVBRK2(T, m, d)
        
        if not (Hi < Hbs):
            self.errorMsg = "Error: Wave broken at structure (Hbs = %6.2f %s)" %\
                (Hbs, self.labelUnitDist)
            
            print(self.errorMsg)
            self.fileOutputWriteMain(dataDict, caseIndex)
            return
        
        L, k = WAVELEN(d, T, 50, self.g)
        
        steep, maxstp = ERRSTP(Hi, d, L)
#        assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
        if not ComplexUtil.lessThan(steep, maxstp):
            self.errorMsg = "Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)" %\
                (maxstp.real, steep.real)
    
        MR, S, MRintc, MRintt, Sintc, Sintt = WFVW1(d, Hi, chi, L, H20weight)
        print('\n\t\t\t\t %s \t\t %s' % ('Miche-Rundgren','Sainflou'))
        print("Wave Position at Wall\t\tCrest\t\tTrough\t\tCrest\t\tTrough\t\tUnits")
        print("Hgt above bottom \t\t %-6.2f \t %6.2f \t %-6.2f \t %6.2f \t %s" %\
            (MR[0].real, MR[3].real, S[0].real, S[3].real, self.labelUnitDist))
        print("Integrated force \t\t %-6.2f \t %6.2f \t %-6.2f \t %6.2f \t %s/%s" %\
            (MR[1].real, MR[4].real, S[1].real, S[4].real, self.labelUnitWt, self.labelUnitDist))
        print("Integrated moment \t\t %-6.2f \t %6.2f \t %-6.2f \t %6.2f \t %s-%s/%s" %\
            (MR[2].real, MR[5].real, S[2].real, S[5].real, self.labelUnitWt, self.labelUnitDist, self.labelUnitDist))
        
        dataDict.update({"MR": MR, "S": S})
        self.fileOutputWriteMain(dataDict, caseIndex)
        
        if self.isSingleCase:
            self.plotDict = {"MRintc": MRintc, "MRintt": MRintt,\
                "Sintc": Sintc, "Sintt": Sintt}
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("d\t%6.2f %s\n" % (dataDict["d"], self.labelUnitDist))
        self.fileRef.write("Hi\t%6.2f %s\n" % (dataDict["Hi"], self.labelUnitDist))
        self.fileRef.write("T\t%6.2f s\n" % dataDict["T"])
        self.fileRef.write("chi\t%6.2f\n" % dataDict["chi"])
        self.fileRef.write("cotphi\t%6.2f\n" % dataDict["cotphi"])
        
        if self.errorMsg != None:
            self.fileRef.write("\n%s\n" % self.errorMsg)
        else:
            self.fileRef.write('\n\t\t\t\t %s \t\t %s \n' % ('Miche-Rundgren','Sainflou'))
            self.fileRef.write("Wave Position at Wall\t\tCrest\t\tTrough\t\tCrest\t\tTrough\t\tUnits\n")
            self.fileRef.write("Hgt above bottom \t\t %-6.2f \t %6.2f \t %-6.2f \t %6.2f \t %s \n" %\
                (dataDict["MR"][0].real, dataDict["MR"][3].real,\
                dataDict["S"][0].real, dataDict["S"][3].real, self.labelUnitDist))
            self.fileRef.write("Integrated force \t\t %-6.2f \t %6.2f \t %-6.2f \t %6.2f \t %s/%s \n" %\
                (dataDict["MR"][1].real, dataDict["MR"][4].real,\
                dataDict["S"][1].real, dataDict["S"][4].real,\
                self.labelUnitWt, self.labelUnitDist))
            self.fileRef.write("Integrated moment \t\t %-6.2f \t %6.2f \t %-6.2f \t %6.2f \t %s-%s/%s \n" %\
                (dataDict["MR"][2].real, dataDict["MR"][5].real,\
                dataDict["S"][2].real, dataDict["S"][5].real,\
                self.labelUnitWt, self.labelUnitDist, self.labelUnitDist))
        
        exportData = [dataDict["d"], dataDict["Hi"], dataDict["T"],\
            dataDict["chi"], dataDict["cotphi"]]
        if self.errorMsg != None:
            exportData.append(self.errorMsg)
        else:
            exportData = exportData + [dataDict["MR"][0], dataDict["MR"][3],\
                dataDict["S"][0], dataDict["S"][3],\
                dataDict["MR"][1], dataDict["MR"][4],\
                dataDict["S"][1], dataDict["S"][4],\
                dataDict["MR"][2], dataDict["MR"][5],\
                dataDict["S"][2], dataDict["S"][5]]
        self.exporter.writeData(exportData)
    # end fileOutputWriteData

    def hasPlot(self):
        return True

    def performPlot(self):
        plt.figure(1, figsize = self.plotConfigDict["figSize"],\
            dpi = self.plotConfigDict["dpi"])
        plt.subplot(2, 1, 1)
        plt.plot(self.plotDict["MRintc"][1],\
            self.plotDict["MRintc"][0], "g-",\
            self.plotDict["MRintc"][2],\
            self.plotDict["MRintc"][0], "c-.",\
            self.plotDict["MRintc"][3],\
            self.plotDict["MRintc"][0], "r:")
        plt.axhline(y=0.0, color="r", LineStyle="--")
        plt.legend(["Wave Pressure", "Hydrostatic Pressure",\
            "Wave and Hydrostatic Pressure"])
        plt.xlabel("Pressure [%s/%s^2]" % (self.labelUnitWt, self.labelUnitDist))
        plt.ylabel("Elevation [%s]" % self.labelUnitDist)
        plt.title("Miche-Rundgren Pressure Distribution - Crest at Wall")
        
        plt.subplot(2, 1, 2)
        plt.plot(self.plotDict["MRintt"][1],\
            self.plotDict["MRintt"][0], "g-",\
            self.plotDict["MRintt"][2],\
            self.plotDict["MRintt"][0], "c-.",\
            self.plotDict["MRintt"][3],\
            self.plotDict["MRintt"][0], "r:")
        plt.axhline(y=0.0, color="r", LineStyle="--")
#				rectangle('Position',[-50,floor(min(Sintt(:,1))),50,abs(floor(min(Sintt(:,1))))+5],'LineWidth',2)
#        plt.ylim([math.floor(min([i[0].real for i in self.plotDict["Sintt"]])),\
#            abs(math.floor(min([i[0].real for i in self.plotDict["Sintt"]]))) - 5])
        plt.ylim([math.floor(min([i.real for i in self.plotDict["Sintt"][0]])),\
            abs(math.floor(min([i.real for i in self.plotDict["Sintt"][0]]))) - 5])
        plt.legend(["Wave Pressure", "Hydrostatic Pressure",\
            "Wave and Hydrostatic Pressure"])
        plt.xlabel("Pressure [%s/%s^2]" % (self.labelUnitWt, self.labelUnitDist))
        plt.ylabel("Elevation [%s]" % self.labelUnitDist)
        plt.title("Miche-Rundgren Pressure Distribution - Trough at Wall")
        plt.tight_layout(h_pad=1.0)
        
        plt.figure(2, figsize = self.plotConfigDict["figSize"],\
            dpi = self.plotConfigDict["dpi"])
        plt.subplot(2, 1, 1)
        plt.plot(self.plotDict["Sintc"][1],\
            self.plotDict["Sintc"][0], "g-",\
            self.plotDict["Sintc"][2],\
            self.plotDict["Sintc"][0], "c-.",
            self.plotDict["Sintc"][3],\
            self.plotDict["Sintc"][0], "r:")
        plt.axhline(y=0.0, color="r", LineStyle="--")
        plt.legend(["Wave Pressure", "Hydrostatic Pressure",\
            "Wave and Hydrostatic Pressure"])
        plt.xlabel("Pressure [%s/%s^2]" % (self.labelUnitWt, self.labelUnitDist))
        plt.ylabel("Elevation [%s]" % self.labelUnitDist)
        plt.title("Sainflou Pressure Distribution - Crest at Wall")
        
        plt.subplot(2, 1, 2)
        plt.plot(self.plotDict["Sintt"][1],\
            self.plotDict["Sintt"][0], "g-",\
            self.plotDict["Sintt"][2],\
            self.plotDict["Sintt"][0], "c-.",\
            self.plotDict["Sintt"][3],\
            self.plotDict["Sintt"][0], "r:")
        plt.axhline(y=0.0, color="r", LineStyle="--")
#        plotAx.add_patch(patches.Rectangle(\
#            (-50, math.floor(min([i[0].real for i in self.plotDict["Sintt"]]))),\
#            50, abs(math.floor(min([i[0].real for i in self.plotDict["Sintt"]]))) + 5,\
#            linestyle=2))
        plt.ylim([math.floor(min([i.real for i in self.plotDict["Sintt"][0]])),\
            abs(math.floor(min([i.real for i in self.plotDict["Sintt"][0]]))) - 5])
        plt.legend(["Wave Pressure", "Hydrostatic Pressure",\
            "Wave and Hydrostatic Pressue"])
        plt.xlabel("Pressure [%s/%s^2]" % (self.labelUnitWt, self.labelUnitDist))
        plt.ylabel("Elevation [%s]" % self.labelUnitDist)
        plt.title("Sainflou Pressure Distribution - Trough at Wall")
        plt.tight_layout(h_pad=1.0)
        
        plt.show()
        
        self.fileOutputPlotWriteData()
    # end performPlot

    def fileOutputPlotWriteData(self):
        self.fileRef.write('Partial Listing of Plot Output File\n\n')
        
        self.fileRef.write('Miche-Rundgren Pressure Distribution\n')
        self.fileRef.write('Crest at Wall \n\n')
        
        self.fileRef.write('          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n')
        self.fileRef.write('          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n' %\
            (self.labelUnitDist, self.labelUnitWt, self.labelUnitDist,\
            self.labelUnitWt, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        
        for i in range(len(self.plotDict["MRintc"][0])):
            self.fileRef.write('%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n' %\
                ((i + 1), self.plotDict["MRintc"][0][i].real,\
                self.plotDict["MRintc"][1][i].real,\
                self.plotDict["MRintc"][2][i].real,\
                self.plotDict["MRintc"][3][i].real))
        
        self.fileRef.write('\n\nMiche-Rundgren Pressure Distribution\n')
        self.fileRef.write('Trough at Wall \n\n')
        
        self.fileRef.write('          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n')
        self.fileRef.write('          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n' %\
            (self.labelUnitDist, self.labelUnitWt, self.labelUnitDist,\
            self.labelUnitWt, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        
        for i in range(len(self.plotDict["MRintt"][0])):
            self.fileRef.write('%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n' %\
                ((i + 1), self.plotDict["MRintt"][0][i].real,\
                self.plotDict["MRintt"][1][i].real,\
                self.plotDict["MRintt"][2][i].real,\
                self.plotDict["MRintt"][3][i].real))
        
        self.fileRef.write('\n\nSainflou Pressure Distribution\n')
        self.fileRef.write('Crest at Wall \n\n')
        
        self.fileRef.write('          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n')
        self.fileRef.write('          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n' %\
            (self.labelUnitDist, self.labelUnitWt, self.labelUnitDist,\
            self.labelUnitWt, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        
        for i in range(len(self.plotDict["Sintc"][0])):
            self.fileRef.write('%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n' %\
                ((i + 1), self.plotDict["Sintc"][0][i].real,\
                self.plotDict["Sintc"][1][i].real,\
                self.plotDict["Sintc"][2][i].real,\
                self.plotDict["Sintc"][3][i].real))
        
        self.fileRef.write('\n\nSainflou Pressure Distribution\n')
        self.fileRef.write('Trough at Wall \n\n')
        
        self.fileRef.write('          Elevation    Wave Pressure    Hydrostatic Pressure    Wave & Hydrostatic Pressure\n')
        self.fileRef.write('          (%s)         (%s/%s^2)        (%s/%s^2)               (%s/%s^2)\n' %\
            (self.labelUnitDist, self.labelUnitWt, self.labelUnitDist,\
            self.labelUnitWt, self.labelUnitDist, self.labelUnitWt, self.labelUnitDist))
        
        for i in range(len(self.plotDict["Sintt"][0])):
            self.fileRef.write('%-6d    %-6.2f       %-6.2f           %-6.2f                  %-6.2f\n' %\
                ((i + 1), self.plotDict["Sintt"][0][i].real,\
                self.plotDict["Sintt"][1][i].real,\
                self.plotDict["Sintt"][2][i].real,\
                self.plotDict["Sintt"][3][i].real))
    # end fileOutputPlotWriteData


driver = WaveForces()