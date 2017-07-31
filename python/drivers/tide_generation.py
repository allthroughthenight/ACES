import numpy as np
import matplotlib.pyplot as plt
import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ANG360 import ANG360
from GAGINI import GAGINI
from GTERMS import GTERMS
from NFACS import NFACS
from ORBIT import ORBIT
from TIDELV import TIDELV

from EXPORTER import EXPORTER

## ACES Update to python
#-------------------------------------------------------------
# Driver for Constituent Tide Record Generation (page 1-4 in ACES User's Guide)
# Provides a tide elevation record at a specific time and locale using
# known amplitudes and epochs for individual harmonic constiuents

# Updated by: Mary Anderson, USACE-CyearL-Coastal Processes Branch
# Date Transferred: April 11, 2011
# Date Verified: May 30, 2012

# Requires the following functions:
# ANG360
# DAYOYR
# GAGINI
# GTERMS
# NFACS
# ORBIT
# TIDELV

# MAIN VARIABLE LIST:
#   INPUT
#   year: year simulation starts
#   mon: month simulation starts
#   day: day simulation starts
#   hr: hr simulation starts
#   tlhrs: length of record (hr)
#   nogauge: total number of gauges (default=1)
#   ng: gauge of interest (default=1)
#   glong: gauge longitude (deg)
#   delt: output time interval (min)
#   gauge0: mean water level height above datum
#   cst: constituents name (read-in from file called tides.txt)
#   amp: amplitdutes of constituents (m, read-in from file)
#   ep: epochs of constituents (read-in from file)
#   requires constituent data entry in tides.txt

#   OUTPUT
#   ytide: tidal surface elevations

#   OTHERS
#   dayj: Julian day of the year (1-365/366 if leap year)
#   alpha: angular arguments for constiuents (deg)
#   fndcst: node factors for constiuents (deg)
#   eqcst: Greenwhich equlibrium arguments for constituents (deg)
#   acst: orbital speeds of constituents (deg/hr)
#   pcst: number of tide cycles per day per constiuent
#-------------------------------------------------------------

class TideGeneration(BaseDriver):
    def __init__(self, year = None, mon = None, day = None, hr = None,\
        tlhrs = None, delt = None, gauge0 = None, glong = None):
        self.exporter = EXPORTER("output/exportTideGeneration")
        
        self.isSingleCase = True

        if year != None:
            self.defaultValue_year = year
        if mon != None:
            self.defaultValuemon = mon
        if day != None:
            self.defaultValue_day = day
        if hr != None:
            self.defaultValue_hr = hr
        if tlhrs != None:
            self.defaultValuetlhrs = tlhrs
        if delt != None:
            self.defaultValue_delt = delt
        if gauge0 != None:
            self.defaultValue_gauge0 = gauge0
        if glong != None:
            self.defaultValue_glong = glong

        super(TideGeneration, self).__init__()
        
        self.exporter.close()
    # end __init__

    def userInput(self):
        self.defineInputDataList()

        if len(self.inputList) > 0:
            self.manualOrFile = USER_INPUT.FINITE_CHOICE(\
                "Enter data manually or load from file? (M or F): ",\
                ["M", "m", "F", "f"])

            if self.manualOrFile == "F" or self.manualOrFile == "f":
                accepted = False

                while not accepted:
                    filenameData = USER_INPUT.FILE_NAME()

                    fileRef = open(filenameData)

                    fileDataTemp = fileRef.read().split("\n")
                    fileData = []
                    for i in fileDataTemp:
                        if len(i) > 0:
                            fileData.append(float(i))

                    if len(fileData) >= len(self.inputList):
                        accepted = True

                        for i in range(len(fileData)):
                            if i < len(self.inputList):
                                inputIndex = i
                            else:
                                inputIndex = len(self.inputList) - 1

                            if fileData[i] < self.inputList[inputIndex].min or\
                                fileData[i] > self.inputList[inputIndex].max:
                                accepted = False
                                print("Value #%d out of range. Please check your value and try again." %\
                                    (i + 1))
                        # end for loop

                        if accepted == True:
                            glongList = []
                            if not hasattr(self, "defaultValue_glong"):
                                mainInputListLen = len(self.inputList) - 1
                            else:
                                mainInputListLen = len(self.inputList)

                            self.dataOutputList = []

                            for i in range(len(fileData)):
                                # check if we need to add glong values
                                # and are at that point
                                if not hasattr(self, "defaultValue_glong") and\
                                    i >= len(self.inputList) - 1:
                                    glongList.append(fileData[i])
                                # else, add normally
                                else:
                                    self.dataOutputList.append(fileData[i])
                            # end for loop
                                    
                            self.dataOutputList.append(glongList)
                        # end if
                    else:
                        print("%d values are required. Please check your file and try again." %\
                            len(self.inputList))
                # end while loop
            # end if
        # end if

        super(TideGeneration, self).userInput()

        accepted = False
        while not accepted:
            print("\nConstituent Data Loading from file")
            filenameTideConstituents = USER_INPUT.FILE_NAME()
            fileRef = open(filenameTideConstituents)

            fileData = fileRef.read()
            fileRef.close()

            fileData = fileData.split("\n")

            self.cst = []
            self.amp = []
            self.ep = []
            for i in fileData:
                lineData = i.split("\t")

                if len(lineData) >= 1:
                    self.cst.append(lineData[0])
                if len(lineData) >= 2:
                    self.amp.append(float(lineData[1]))
                if len(lineData) >= 3:
                    self.ep.append(float(lineData[2]))
            # end for loop

            if len(self.amp) == 0 or len(self.ep) == 0:
                print("ERROR: Constituent Data Incomplete.")
                print("Please correct the input file and try again.")
            else:
                accepted = True
        # end while loop
    # end userInput

    def getSingleCaseInput(self):
        if not hasattr(self, "manualOrFile") or\
            (self.manualOrFile == "M" or self.manualOrFile == "m"):
            super(TideGeneration, self).getSingleCaseInput()
    # end getSingleCaseInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValue_year"):
            self.inputList.append(BaseField(\
                "year: year simulation starts (YYYY)", 1900, 2050))
        if not hasattr(self, "defaultValuemon"):
            self.inputList.append(BaseField(\
                "mon: month simulation starts (MM)", 1, 12))
        if not hasattr(self, "defaultValue_day"):
            self.inputList.append(BaseField(\
                "day: day simulation starts (DD)", 1, 31))
        if not hasattr(self, "defaultValue_hr"):
            self.inputList.append(BaseField(\
                "hr: hour simulation starts (HH.H)", 0, 24))
        if not hasattr(self, "defaultValuetlhrs"):
            self.inputList.append(BaseField(\
                "tlhrs: length of record (HH.H)", 0, 744))
        if not hasattr(self, "defaultValue_delt"):
            self.inputList.append(BaseField(\
                "delt: output time interval (min)" , 1, 60))
        if not hasattr(self, "defaultValue_gauge0"):
            self.inputList.append(BaseField(\
                "gauge0: mean water level height above datum", -100.0, 100.0))
        if not hasattr(self, "defaultValue_glong"):
            self.inputList.append(BaseField(\
                "glong: gauge longitude (deg)", -180, 180))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(\
            defaultFilename = "tide_generation",\
            requestDesc = True)

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValue_year"):
            year = self.defaultValue_year
        else:
            year = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValuemon"):
            mon = self.defaultValuemon
        else:
            mon = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_day"):
            day = self.defaultValue_day
        else:
            day = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_hr"):
            hr = self.defaultValue_hr
        else:
            hr = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValuetlhrs"):
            tlhrs = self.defaultValuetlhrs
        else:
            tlhrs = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_delt"):
            delt = self.defaultValue_delt
        else:
            delt = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_gauge0"):
            gauge0 = self.defaultValue_gauge0
        else:
            gauge0 = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_glong"):
            glong = self.defaultValue_glong
        else:
            if isinstance(caseInputList[currIndex], list):
                glong = caseInputList[currIndex]
            else:
                glong = [caseInputList[currIndex]]

        return int(year), int(mon), int(day), hr, tlhrs, delt, gauge0, glong
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        year, mon, day, hr, tlhrs, delt, gauge0, glong = self.getCalcValues(caseInputList)

        delthr = delt/60.0

        nogauge = len(glong)

        acst = [28.9841042,30.0,28.4397295,15.0410686,57.9682084,\
            13.9430356,86.9523127,44.0251729,60.0,57.4238337,28.5125831,\
            90.0,27.9682084,27.8953548,16.1391017,29.4556253,15.0,\
            14.4966939,15.5854433,0.5443747,0.0821373,0.0410686,\
            1.0158958,1.0980331,13.4715145,13.3986609,29.9589333,\
            30.0410667,12.8542862,14.9589314,31.0158958,43.4761563,\
            29.5284789,42.9271398,30.0821373,115.9364169,58.9841042]

        pcst = [2,2,2,1,4,1,6,3,4,4,2,6,2,2,1,2,1,1,1,0,0,0,0,0,1,1,2,2,1,1,2,3,2,3,2,8,4]
        pcst = [float(i) for i in pcst]

        ## Intialize gage-specific info relevant to harmonic constituents
        alpha, fndcst = GAGINI(\
            nogauge, year, mon, day, hr, tlhrs, glong, self.ep, acst, pcst)

        ntid = int(tlhrs/delthr) + 1

        tidelv = []
        xtim = []
        for i in range(ntid):
            xtim.append(i*delthr)
            tidelv.append(TIDELV(\
                nogauge, xtim[i], self.amp, alpha, fndcst, acst))

        ytide = [gauge0 + i for i in tidelv]

        self.plotDict = {"xtim": xtim, "ytide": ytide}
    # end performCalculations

    def hasPlot(self):
        return True

    def fileOutputPlotInit(self):
        self.fileRef = open(self.getFilePath() +\
            self.fileOutputData.filename + ".txt", "w")
    # end fileOutputPlotInit

    def performPlot(self):
        plt.figure(1, figsize = self.plotConfigDict["figSize"],\
            dpi = self.plotConfigDict["dpi"])
        plt.plot(self.plotDict["xtim"], self.plotDict["ytide"])
        plt.title("Tide Elevations [from constituents]", fontsize = self.plotConfigDict["titleFontSize"])
        plt.xlabel("Time [hr]",\
            fontsize = self.plotConfigDict["axisLabelFontSize"])
        #output same units as amplitude, datum input
        plt.ylabel("Elevation [%s]" % self.labelUnitDist,\
            fontsize = self.plotConfigDict["axisLabelFontSize"])

        plt.show()

        self.fileOutputPlotWriteData()
    # end performPlot

    def fileOutputPlotWriteData(self):
        self.fileRef.write("CONSTITUENT TIDE ELEVATION RECORD\n")
        self.fileRef.write("%s\n" % self.fileOutputData.fileDesc)
        self.fileRef.write("TIME\tELEVATION\n")

        for i in range(len(self.plotDict["xtim"])):
            self.fileRef.write("%-6.2f\t%-6.2f\n" %\
                (self.plotDict["xtim"][i], self.plotDict["ytide"][i]))
        
        exportData = []
        for i in range(len(self.plotDict["xtim"])):
            exportData = exportData + [self.plotDict["xtim"][i],\
                self.plotDict["ytide"][i]]
        self.exporter.writeData(exportData)
    # end fileOutputPlotWriteData


driver = TideGeneration()