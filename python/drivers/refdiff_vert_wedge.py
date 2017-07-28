import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from DRWEDG import DRWEDG
from ERRSTP import ERRSTP
from ERRWAVBRK import ERRWAVBRK
from ERRWAVBRK1 import ERRWAVBRK1
from WAVELEN import WAVELEN

## ACES Update to python
#-------------------------------------------------------------
# Driver for Combined Diffraction and Reflection by a Vertical Wedge
# (page 3-3 in ACES User's Guide). Estimates wave height modifcation due
# to combined diffraction and reflection near jettted harbor entrances,
# quay walls, and other such structures.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 12, 2011
# Date Verified: June 18, 2012

# Requires the following functions:
# DRWEDG
# ERRSTP
# ERRWAVBRK1
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   Hi: incident wave height (m)
#   T: water period (sec)
#   d: water depth (m)
#   alpha: wave angle (deg)
#   wedgang: wedge angle (deg)
#   mode: change for single (0) or uniform grid case (1)
#   xcor: x-coordinate (m) (single case only)
#   ycor: y-coordinate (m) (single case only)
#   x0: x start coordinate (m) (grid case only)
#   xend: x end coordinate (m) (grid case only)
#   dx: x spatial increment (m) (grid case only)
#   y0: y start coordinate (m) (grid case only)
#   yend: y end coordinate (m) (grid case only)
#   dy: y spatial increment (m) (grid case only)

#   OUTPUT
#   L: wave length (m)
#   phi: modification factor (H/Hi)
#   beta: wave phase (rad)
#   H: modified wave height (m)

#   OTHERS
#-------------------------------------------------------------

class RefdiffVertWedge(BaseDriver):
    def __init__(self, Hi = None, T = None, d = None,\
        alpha = None, wedgang = None, mode = None, xcor = None,\
        ycor = None, x0 = None, xend = None, dx = None, y0 = None,\
        yend = None, dy = None):
        self.exporter = EXPORTER("output/exportRefdiffVertWedge.txt")
        
        if Hi != None:
            self.isSingleCase = True
            self.defaultValueHi = Hi
        if T != None:
            self.isSingleCase = True
            self.defaultValueT = T
        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d
        if alpha != None:
            self.isSingleCase = True
            self.defaultValue_alpha = alpha
        if wedgang != None:
            self.isSingleCase = True
            self.defaultValue_wedgang = wedgang
        if mode != None:
            self.isSingleCase = True
            self.defaultValue_mode = mode
        if xcor != None:
            self.isSingleCase = True
            self.defaultValue_xcor = xcor
        if ycor != None:
            self.isSingleCase = True
            self.defaultValue_ycor = ycor
        if x0 != None:
            self.isSingleCase = True
            self.defaultValue_x0 = x0
        if xend != None:
            self.isSingleCase = True
            self.defaultValue_xend = xend
        if dx != None:
            self.isSingleCase = True
            self.defaultValue_dx = dx
        if y0 != None:
            self.isSingleCase = True
            self.defaultValue_y0 = y0
        if yend != None:
            self.isSingleCase = True
            self.defaultValue_yend = yend
        if dy != None:
            self.isSingleCase = True
            self.defaultValue_dy = dy

        super(RefdiffVertWedge, self).__init__()

        self.exporter.close()
    # end __init__

    def userInput(self):
        if not hasattr(self, "defaultValue_mode"):
            self.mode = USER_INPUT.FINITE_CHOICE(\
                "Mode 1 Single Case or Mode 2 Grid Case (1 or 2): ",\
                ["1", "2"])
            if self.mode == "1":
                self.mode = 0
            else:
                self.mode = 1
        else:
            self.mode = self.defaultValue_mode

        super(RefdiffVertWedge, self).userInput()

        if self.mode == 1:
            if not hasattr(self, "defaultValue_x0"):
                self.x0 = USER_INPUT.DATA_VALUE(\
                    "x0: x start coordinate (%s)" % self.labelUnitDist,\
                    -5280.0, 5280.0)
            else:
                self.x0 = self.defaultValue_x0

            if not hasattr(self, "defaultValue_xend"):
                self.xend = USER_INPUT.DATA_VALUE(\
                    "xend: x end coordinate (%s)" % self.labelUnitDist,\
                    -5280.0, 5280.0)
            else:
                self.xend = self.defaultValue_xend

            if not hasattr(self, "defaultValue_dx"):
                self.dx = USER_INPUT.DATA_VALUE(\
                    "dx: x spatial increment (%s)" % self.labelUnitDist,\
                    0.1, 5280.0)
            else:
                self.dx = self.defaultValue_dx

            if not hasattr(self, "defaultValue_y0"):
                self.y0 = USER_INPUT.DATA_VALUE(\
                    "y0: y start coordinate (%s)" % self.labelUnitDist,\
                    -5280.0, 5280.0)
            else:
                self.y0 = self.defaultValue_y0

            if not hasattr(self, "defaultValue_yend"):
                self.yend = USER_INPUT.DATA_VALUE(\
                    "yend: y end coordinate (%s)" % self.labelUnitDist,\
                    -5280.0, 5280.0)
            else:
                self.yend = self.defaultValue_yend

            if not hasattr(self, "defaultValue_dy"):
                self.dy = USER_INPUT.DATA_VALUE(\
                    "dy: y spatial increment (%s)" % self.labelUnitDist,\
                    0.1, 5280.0)
            else:
                self.dy = self.defaultValue_dy
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueHi"):
            self.inputList.append(BaseField(\
                "Hi: incident wave height (%s)" % (self.labelUnitDist), 0.1, 200.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField(\
                "T: water period (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField(\
                "d: water depth (%s)" % (self.labelUnitDist), 0.01, 5000.0))
        if not hasattr(self, "defaultValue_alpha"):
            self.inputList.append(BaseField(\
                "alpha: wave angle (deg)", 0.0, 180.0))
        if not hasattr(self, "defaultValue_wedgang"):
            self.inputList.append(BaseField(\
                "wedgang: wedge angle (deg)", 0.0, 180.0))

        if self.mode == 0:
            if not hasattr(self, "defaultValue_xcor"):
                self.inputList.append(BaseField(\
                    "xcor: x-coordinate (%s)" %\
                    (self.labelUnitDist), -5280.0, 5280.0))
            if not hasattr(self, "defaultValue_ycor"):
                self.inputList.append(BaseField(\
                    "ycor: y-coordinate (%s)" %\
                    (self.labelUnitDist), -5280.0, 5280.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        if self.mode == 0:
            fileSuffix = "single_point"
        else:
            fileSuffix = "uniform_grid"

        self.fileOutputRequestMain(\
            defaultFilename = "refdiff_vert_wedge_%s" % fileSuffix)

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueHi"):
            Hi = self.defaultValueHi
        else:
            Hi = caseInputList[currIndex]
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

        if hasattr(self, "defaultValue_alpha"):
            alpha = self.defaultValue_alpha
        else:
            alpha = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_wedgang"):
            wedgang = self.defaultValue_wedgang
        else:
            wedgang = caseInputList[currIndex]
            currIndex = currIndex + 1

        if self.mode == 0:
            if hasattr(self, "defaultValue_xcor"):
                xcor = self.defaultValue_xcor
            else:
                xcor = caseInputList[currIndex]
                currIndex = currIndex + 1

            if hasattr(self, "defaultValue_ycor"):
                ycor = self.defaultValue_ycor
            else:
                ycor = caseInputList[currIndex]
        else:
            xcor = None
            ycor = None

        return Hi, T, d, alpha, wedgang, xcor, ycor
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Hi, T, d, alpha, wedgang, xcor, ycor =\
            self.getCalcValues(caseInputList)
        dataDict = {"Hi": Hi, "T": T, "d": d,\
            "alpha": alpha, "wedgang": wedgang}

        if self.mode == 0:
            dataDict["xcor"] = xcor
            dataDict["ycor"] = ycor
        else:
            dataDict["x0"] = self.x0
            dataDict["xend"] = self.xend
            dataDict["dx"] = self.dx
            dataDict["y0"] = self.y0
            dataDict["yend"] = self.yend
            dataDict["dy"] = self.dy

        # Single Point Case
        if self.mode == 0:
            L, k = WAVELEN(d, T, 50, self.g)

            steep, maxstp = ERRSTP(Hi, d, L)
            if not (steep < maxstp):
                self.errorMsg = "Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f" %\
                    (maxstp, steep)
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            Hb = ERRWAVBRK1(d, 0.78)
            if not (Hi < Hb):
                self.errorMsg = "Error: Input wave broken (Hb = %6.2f %s" %\
                    (Hb, self.labelUnitDist)
                    
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            phi, beta, H, error = DRWEDG(xcor, ycor, Hi, alpha, wedgang, L)
            if error == 1:
                self.errorMsg = "Error: (x,y) location inside structure."
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            print("Wavelength\t\t%6.2f\t%s" % (L, self.labelUnitDist))
            print("Mod factor (phi)\t%6.2f" % phi)
            print("Wave phase\t\t%6.2f\trad" % beta)
            print("Mod wave height\t\t%6.2f\t%s" % (H, self.labelUnitDist))

            dataDict["L"] = L
            dataDict["phi"] = phi
            dataDict["beta"] = beta
            dataDict["H"] = H
        else:
            xcors = []
            nxpt = int((self.xend - self.x0 + self.dx)/self.dx)
            [xcors.append(self.x0 + i*self.dx) for i in range(nxpt)]

            ycors = []
            nypt = int((self.yend - self.y0 + self.dy)/self.dy)
            [ycors.append(self.y0 + (nypt - i - 1)*self.dy) \
                for i in range(nypt)]

            L, k = WAVELEN(d, T, 50, self.g)
            dataDict["L"] = L

            steep, maxstp = ERRSTP(Hi, d, L)
            if not (steep < maxstp):
                self.errorMsg = "Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f" %\
                    (maxstp, steep)
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            Hb = ERRWAVBRK(T, d, 0.0, 0.78, 0)
            if not (Hi < Hb):
                self.errorMsg = "error: Input wave broken (Hb = %6.2f %s" %\
                    (Hb, self.labelUnitDist)
                
                print(self.errorMsg)
                self.fileOutputWriteMain(dataDict, caseIndex)
                return

            phi = []
            beta = []
            H = []

            for i in range(nypt):
                phi.append([])
                beta.append([])
                H.append([])

                for j in range(nxpt):
                    xx = xcors[j]
                    yy = ycors[i]

                    valPhi, valBeta, valH, error = DRWEDG(xx, yy, Hi, alpha, wedgang, L)

                    phi[i].append(valPhi)
                    beta[i].append(valBeta)
                    H[i].append(valH)

                    if error == 1:
                        self.errorMsg = "Error: (x,y) location inside structure."
                        
                        print(self.errorMsg)
                        self.fileOutputWriteMain(dataDict, caseIndex)
                        return
                # end for loop
            # end for loop

            print("Wavelength\t\t%6.2f %s" % (L, self.labelUnitDist))

            print("Modification factors:")
            printMsg = ""
            for i in range(len(xcors)):
                printMsg += ("\t%6.2f" % xcors[i])
            print(printMsg)

            for i in range(len(phi)):
                printMsg = "%6.2f" % ycors[i]

                for j in range(len(phi[0])):
                    printMsg += ("\t%6.2f" % phi[i][j])
                print(printMsg)


            print("\nModified Wave Heights:")
            printMsg = ""
            for i in range(len(xcors)):
                printMsg += "\t%6.2f" % xcors[i]
            print(printMsg)

            for i in range(len(H)):
                printMsg = "%6.2f" % ycors[i]

                for j in range(len(H[0])):
                    printMsg += "\t%6.2f" % H[i][j]
                print(printMsg)

            print("\nPhase Angles (rad):")
            printMsg = ""
            for i in range(len(xcors)):
                printMsg += "\t%6.2f" % xcors[i]
            print(printMsg)

            for i in range(len(beta)):
                printMsg = "%6.2f" % ycors[i]

                for j in range(len(beta[0])):
                    printMsg += "\t%6.2f" % beta[i][j]
                print(printMsg)

            dataDict["xcors"] = xcors
            dataDict["ycors"] = ycors
            dataDict["phi"] = phi
            dataDict["beta"] = beta
            dataDict["H"] = H
        # end if

        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        if self.mode == 0:
            self.fileRef.write("Input\n")
            self.fileRef.write("Hi                  %6.2f %s\n" % (dataDict["Hi"], self.labelUnitDist))
            self.fileRef.write("T                   %6.2f s\n" % dataDict["T"])
            self.fileRef.write("d                   %6.2f %s\n" % (dataDict["d"], self.labelUnitDist))
            self.fileRef.write("alpha               %6.2f deg\n" % dataDict["alpha"])
            self.fileRef.write("wedgang             %6.2f deg\n" % dataDict["wedgang"])
            self.fileRef.write("xcor                %6.2f %s\n" % (dataDict["xcor"], self.labelUnitDist))
            self.fileRef.write("ycor                %6.2f %s\n" % (dataDict["ycor"], self.labelUnitDist))

            if self.errorMsg != None:
                self.fileRef.write("\n%s\n" % self.errorMsg)
            else:
                self.fileRef.write("\nWavelength          %6.2f %s\n" % (dataDict["L"], self.labelUnitDist))
                self.fileRef.write("Mod factor (phi)    %6.2f\n" % dataDict["phi"])
                self.fileRef.write("Wave phase          %6.2f rad\n" % dataDict["beta"])
                self.fileRef.write("Mod wave height     %6.2f %s\n" % (dataDict["H"], self.labelUnitDist))
                
            exportData = [dataDict["Hi"], dataDict["T"], dataDict["d"],\
                dataDict["alpha"], dataDict["wedgang"], dataDict["xcor"],\
                dataDict["ycor"]]
            if self.errorMsg != None:
                exportData.append("Error")
            else:
                exportData = exportData + [dataDict["L"], dataDict["phi"],\
                    dataDict["beta"], dataDict["H"]]
            self.exporter.writeData(exportData)
        else:
            self.fileRef.write("Incident Wave Height\t=\t%-6.2f\t%s\tWave Period\t=\t%-6.2f\tsec\n" %\
                (dataDict["Hi"], self.labelUnitDist, dataDict["T"]))
            self.fileRef.write("Water Depth\t\t=\t%-6.2f\t%s\tWavelength\t=\t%-6.2f\t%s\n" %\
                (dataDict["d"], self.labelUnitDist, dataDict["L"], self.labelUnitDist))
            self.fileRef.write("Wave Angle\t\t=\t%-6.2f\tdeg\tWedge Angle\t=\t%-6.2f\tdeg\n\n" % (dataDict["alpha"], dataDict["wedgang"]))

            if self.errorMsg != None:
                self.fileRef.write("%s\n" % self.errorMsg)
            else:
                # phi table
                self.fileRef.write("**** Modification Factors:\n")
                self.fileRef.write("              x=  ")
                for xcor in dataDict["xcors"]:
                    self.fileRef.write("  %8.2f" % xcor)
                self.fileRef.write("\n--------------------------------------------------------------------\n")
    
                for i in range(len(dataDict["phi"])):
                    self.fileRef.write("y=      %8.2f  " % dataDict["ycors"][i])
    
                    for j in range(len(dataDict["phi"][0])):
                        self.fileRef.write("  %8.2f" % dataDict["phi"][i][j])
    
                    self.fileRef.write("\n")
                self.fileRef.write("--------------------------------------------------------------------\n")
    
                self.fileRef.write("              x=  ")
                for xcor in dataDict["xcors"]:
                    self.fileRef.write("  %8.2f" % xcor)
                self.fileRef.write("\n--------------------------------------------------------------------\n")
                # end phi table
    
                self.fileRef.write("\n\n")
    
                # H table
                self.fileRef.write("**** Modified Wave Heights (%s):\n" % self.labelUnitDist)
    
                self.fileRef.write("              x=  ")
                for xcor in dataDict["xcors"]:
                    self.fileRef.write("  %8.2f" % xcor)
                self.fileRef.write("\n--------------------------------------------------------------------\n")
    
                for i in range(len(dataDict["H"])):
                    self.fileRef.write("y=      %8.2f  " % dataDict["ycors"][i])
    
                    for j in range(len(dataDict["H"][0])):
                        self.fileRef.write("  %8.2f" % dataDict["H"][i][j])
    
                    self.fileRef.write("\n")
                self.fileRef.write("--------------------------------------------------------------------\n")
    
                self.fileRef.write("              x=  ")
                for xcor in dataDict["xcors"]:
                    self.fileRef.write("  %8.2f" % xcor)
                self.fileRef.write("\n--------------------------------------------------------------------\n")
                # end H table
    
                self.fileRef.write("\n\n")
    
                # beta table
                self.fileRef.write("**** Phase Angles (rad):\n")
    
                self.fileRef.write("              x=  ")
                for xcor in dataDict["xcors"]:
                    self.fileRef.write("  %8.2f" % xcor)
                self.fileRef.write("\n--------------------------------------------------------------------\n")
    
                for i in range(len(dataDict["beta"])):
                    self.fileRef.write("y=      %8.2f  " % dataDict["ycors"][i])
    
                    for j in range(len(dataDict["beta"][0])):
                        self.fileRef.write("  %8.2f" % dataDict["beta"][i][j])
    
                    self.fileRef.write("\n")
                self.fileRef.write("--------------------------------------------------------------------\n")
    
                self.fileRef.write("              x=  ")
                for xcor in dataDict["xcors"]:
                    self.fileRef.write("  %8.2f" % xcor)
                self.fileRef.write("\n--------------------------------------------------------------------\n")
                # end beta table
            # end if
            
            exportData = [dataDict["Hi"], dataDict["T"], dataDict["d"]]
            exportData = exportData + [dataDict["alpha"], dataDict["wedgang"]]
            if self.errorMsg != None:
                exportData.append("Error")
            else:
                exportData = exportData + [dataDict["L"],\
                    dataDict["xcors"][0], dataDict["xcors"][-1],\
                    abs(dataDict["xcors"][1] - dataDict["xcors"][0]),\
                    dataDict["ycors"][0], dataDict["ycors"][-1],\
                    abs(dataDict["ycors"][1] - dataDict["ycors"][0])]
                
                for i in dataDict["phi"]:
                    for j in i:
                        exportData.append(j)
                
                for i in dataDict["H"]:
                    for j in i:
                        exportData.append(j)
                
                for i in dataDict["beta"]:
                    for j in i:
                        exportData.append(j)
                
            self.exporter.writeData(exportData)
        # end if
    # end fileOutputWriteData


driver = RefdiffVertWedge()