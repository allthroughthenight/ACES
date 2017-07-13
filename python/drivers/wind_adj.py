import sys
import math
import numpy as np
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from WADJ import WADJ
from WGFET import WGFET
from WGRO import WGRO

## ACES Update to python
#-------------------------------------------------------------
# Driver for Windspeed Adjustment and Wave Growth (page 1-1 of ACES User's
# Guide). Provide estimates for wave growth over open-water and restricted
# fetches in deep and shallow water.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 28, 2011
# Date Modified:

# Requires the following functions:
# ERRWAVBRK1
# WADJ
# WAGEOS
# WAPBL
# WAPSI
# WASBL
# WASHR
# WGDL
# WGFD
# WGFET
# WGFL
# WGRO

# MAIN VARIABLE LIST:
#   INPUT
#   zobs: elevation of observed winds [m]
#   uobs: observed wind speed [m/s]
#   dtemp: air-sea temperature difference [deg C]
#   duro: duration of observed wind [hr]
#   durf: duration of final wind [hr]
#   lat: latitude of wind observation [deg]
#   windobs: wind observation type
#   fetchopt: wind fetch options
#   wgtyp: open water wave growth equation options

#   OPEN-WATER VARIABLES
#   F: length of wind fetch [m]
#   d: average depth of fetch (only for shallow water equations) [m]

#   RESTRICTED VARIABLES
#   wdir: wind direction [deg]
#   dang: radial angle increment [deg]
#   ang1: direction of first radial fetch [deg]
#   angs: fetch length [m]

#   OUTPUT
#   ue: equivalent neutral wind speed [m/s]
#   ua: adjusted wind speed [m/s]
#   Hmo: wave height [m]
#   Tp: peak wave period [s]
#   wg: type of wave-growth
#   theta: wave direction with respect to N [deg]

#   OTHERS
#-------------------------------------------------------------

class WindAdj(BaseDriver):
    def __init__(self, windobs = None, wgtyp = None, useKnots = None,\
        zobs = None, Uobs = None, dtemp = None, duro = None, durf = None,\
        lat = None, F = None, d = None, wdir = None, dang = None,\
        ang1 = None, manualOrFile = None, Nfet = None, angs = None):
        if windobs != None:
            self.isSingleCase = True
            self.defaultValue_windobs = windobs
        if wgtyp != None:
            self.isSingleCase = True
            self.defaultValue_wgtyp = wgtyp
        if useKnots != None:
            self.isSingleCase = True
            self.defaultValue_useKnots = useKnots
        if zobs != None:
            self.isSingleCase = True
            self.defaultValue_zobs = zobs
        if Uobs != None:
            self.isSingleCase = True
            self.defaultValueUobs = Uobs
        if dtemp != None:
            self.isSingleCase = True
            self.defaultValue_dtemp = dtemp
        if duro != None:
            self.isSingleCase = True
            self.defaultValue_duro = duro
        if durf != None:
            self.isSingleCase = True
            self.defaultValue_durf = durf
        if lat != None:
            self.isSingleCase = True
            self.defaultValue_lat = lat
        if F != None:
            self.isSingleCase = True
            self.defaultValueF = F
        if d != None:
            self.isSingleCase = True
            self.defaultValue_d = d
        if wdir != None:
            self.isSingleCase = True
            self.defaultValue_wdir = wdir
        if dang != None:
            self.isSingleCase = True
            self.defaultValue_dang = dang
        if ang1 != None:
            self.isSingleCase = True
            self.defaultValue_ang1 = ang1
        if manualOrFile != None:
            self.isSingleCase = True
            self.defaultValue_manualOrFile = manualOrFile
        if Nfet != None:
            self.isSingleCase = True
            self.defaultValue_useKnots = useKnots
        if angs != None:
            self.isSingleCase = True
            self.defaultValue_useKnots = useKnots

        super(WindAdj, self).__init__()
    # end __init__

    def userInput(self):
        self.windObsList = ["Overwater (shipboard)",\
            "Overwater (not shipboard)",\
            "Shore (windward - offshore to onshore)",\
            "Shore (leeward - onshore to offshore)",\
            "Over land",\
            "Geostrophic wind"]

        if not hasattr(self, "defaultValue_windobs"):
            windObsMsg = "Wind observation types:\n"
            for i in range(len(self.windObsList)):
                windObsMsg += "[%d] %s\n" % ((i + 1), self.windObsList[i])
            windObsMsg += "Select option: "

            self.windobs = USER_INPUT.FINITE_CHOICE(\
                windObsMsg, ["1", "2", "3", "4", "5", "6"])
            self.windobs = int(self.windobs)
        else:
            self.windobs = self.defaultValue_windobs

        self.wgtypList = ["Open Water - Deep",\
            "Open Water - Shallow",\
            "Restricted - Deep",\
            "Restricted - Shallow"]

        if not hasattr(self, "defaultValue_wgtyp"):
            wgtypMsg = "Wind fetch and wave growth options:\n"
            for i in range(len(self.wgtypList)):
                wgtypMsg += "[%d] %s\n" % ((i + 1), self.wgtypList[i])
            wgtypMsg += "Select option: "

            self.wgtyp = USER_INPUT.FINITE_CHOICE(\
                wgtypMsg, ["1", "2", "3", "4"])
            self.wgtyp = int(self.wgtyp)
        else:
            self.wgtyp = self.defaultValue_wgtyp

        self.isWaterOpen = self.wgtyp == 1 or self.wgtyp == 2
        self.isWaterShallow = self.wgtyp == 2 or self.wgtyp == 4

        super(WindAdj, self).userInput()

        if not self.isWaterOpen:
            if not hasattr(self, "defaultValue_dang"):
                self.dang = USER_INPUT.DATA_VALUE(\
                    "dang: radial angle increment [deg]", 1.0, 180.0)
            else:
                self.dang = self.defaultValue_dang

            if not hasattr(self, "defaultValue_ang1"):
                self.ang1 = USER_INPUT.DATA_VALUE(\
                    "ang1: direction of first radial fetch [deg]",\
                    0.0, 360.0)
            else:
                self.ang1 = self.defaultValue_ang1

            if not hasattr(self, "defaultValue_manualOrFile"):
                manualOrFile = USER_INPUT.FINITE_CHOICE(\
                    "Would you like to enter fetch length data " +\
                    "manually or load from a file?\n" +\
                    "[M] for manual entry or [F] for file loading: ",
                    ["M", "m", "F", "f"])

                if manualOrFile == "M" or manualOrFile == "m":
                    self.Nfet = USER_INPUT.DATA_VALUE(\
                        "Nfet: number of radial fetches", 2, 360)
                    self.Nfet = int(self.Nfet)

                    self.angs = []
                    for i in range(self.Nfet):
                        self.angs.append(USER_INPUT.DATA_VALUE(\
                            "angs: fetch length [%s] #%d" %\
                            (self.labelUnitDistLrg, i), 0.0, 9999.0))
                else:
                    accepted = False
                    while not accepted:
                        filename = USER_INPUT.FILE_NAME()

                        fileRef = open(filename)

                        fileData = fileRef.read()

                        self.angs = []
                        for dataLine in fileData.split("\n"):
                            if len(dataLine) > 0:
                                self.angs.append(float(dataLine))
                        self.Nfet = len(self.angs)

                        fileRef.close()

                        if self.Nfet >= 2 and self.Nfet <= 360:
                            accepted = True
                        else:
                            print("File must have between 2 and 360 fetch lengths.")
                    # end while
    # end userInput

    def defineInputDataList(self):
        if self.isMetric:
            self.labelSpeed = "m/s"
            self.labelUnitDistLrg = "km"
        else:
            self.labelSpeed = "mph"
            self.labelUnitDistLrg = "mi"

        if not hasattr(self, "defaultValue_useKnots"):
            self.useKnots = USER_INPUT.FINITE_CHOICE(\
                "Speed options:\n[M] %s\n[K] knots\nSelect option: " %\
                self.labelSpeed,\
                ["M", "m", "K", "k"])
        else:
            self.useKnots = self.defaultValue_useKnots
        if self.useKnots == "K" or self.useKnots == "k":
            self.labelSpeedFinal = "knots"
            self.useKnots = True
        else:
            self.labelSpeedFinal = self.labelSpeed
            self.useKnots = False

        self.inputList = []

        if not hasattr(self, "defaultValue_zobs"):
            self.inputList.append(BaseField(\
                "zobs: elevation of observed winds [%s]" % (self.labelUnitDist),\
                1.0, 5000.0))
        if not hasattr(self, "defaultValueUobs"):
            self.inputList.append(BaseField(\
                "uobs: observed wind speed [%s]" % self.labelSpeedFinal,\
                0.1, 200.0))
        if not hasattr(self, "defaultValue_dtemp"):
            self.inputList.append(BaseField(\
                "dtemp: air-sea temperature difference [deg C]",\
                -100.0, 100.0))
        if not hasattr(self, "defaultValue_duro"):
            self.inputList.append(BaseField(\
                "duro: duration of observed wind [hr]", 0.1, 86400.0))
        if not hasattr(self, "defaultValue_durf"):
            self.inputList.append(BaseField(\
                "durf: duration of final wind [hr]", 0.1, 86400.0))
        if not hasattr(self, "defaultValue_lat"):
            self.inputList.append(BaseField(\
                "lat: latitude of wind observation [deg]", 0.0, 180.0))

        if self.isWaterOpen and not hasattr(self, "defaultValueF"):
            self.inputList.append(BaseField(\
                "F: length of wind fetch [%s]" % self.labelUnitDistLrg,
                0.0, 9999.0))

        if self.isWaterShallow and not hasattr(self, "defaultValue_d"):
            self.inputList.append(BaseField(\
                "d: average depth of fetch [%s]" % self.labelUnitDist,
                0.1, 10000.0))

        if not self.isWaterOpen and not hasattr(self, "defaultValue_wdir"):
            self.inputList.append(BaseField(\
                "wdir: wind direction [deg]", 0.0, 360.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "wind_adj")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValue_zobs"):
            zobs = self.defaultValue_zobs
        else:
            zobs = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueUobs"):
            Uobs = self.defaultValueUobs
        else:
            Uobs = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_dtemp"):
            dtemp = self.defaultValue_dtemp
        else:
            dtemp = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_duro"):
            duro = self.defaultValue_duro
        else:
            duro = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_durf"):
            durf = self.defaultValue_durf
        else:
            durf = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_lat"):
            lat = self.defaultValue_lat
        else:
            lat = caseInputList[currIndex]
            currIndex = currIndex + 1

        if self.isWaterOpen:
            if hasattr(self, "defaultValueF"):
                F = self.defaultValueF
            else:
                F = caseInputList[currIndex]
                currIndex = currIndex + 1
        else:
            F = None

        if self.isWaterShallow:
            if hasattr(self, "defaultValue_d"):
                d = self.defaultValue_d
            else:
                d = caseInputList[currIndex]
                currIndex = currIndex + 1
        else:
            d = 0.0

        if not self.isWaterOpen:
            if hasattr(self, "defaultValue_wdir"):
                wdir = self.defaultValue_wdir
            else:
                wdir = caseInputList[currIndex]
                currIndex = currIndex + 1
        else:
            wdir = None

        if not self.isWaterOpen:
            dang = self.dang
            ang1 = self.ang1
            Nfet = self.Nfet
            angs = self.angs
        else:
            dang = None
            ang1 = None
            Nfet = None
            angs = None

        return zobs, Uobs, dtemp, duro, durf, lat, F, d, wdir,\
            dang, ang1, Nfet, angs
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        zobs, Uobs, dtemp, duro, durf, lat, F, d, wdir,\
            dang, ang1, Nfet, angs = self.getCalcValues(caseInputList)

        # Constant for convertions
        ft2m = 0.3048
        mph2mps = 0.44704
        hr2s = 3600.0
        min2s = 60.0
        deg2rad = math.pi/180.0
        mi2m = 1609.344
        km2m = 0.001
        F2C = 5.0/9.0
        knots2mps = 0.5144

        if not self.isMetric:
            conversionDist = ft2m
            conversionDistLrg = mi2m
        else:
            conversionDist = 1.0
            conversionDistLrg = km2m

        if self.useKnots:
            conversionSpeed = knots2mps
        elif not self.isMetric:
            conversionSpeed = mph2mps
        else:
            conversionSpeed = 1.0

        if self.isWaterOpen:
            phi = 0.0
        else:
            F, phi, theta = WGFET(ang1, dang, wdir, angs)

        if np.isclose(lat, 0.0):
            print("Error: Latitude must be a non-zero value.")
            return

        # Check WDIR vs Fetch data. WDIR must meet this criterion:
        # ang1 -45 degrees <= WDIR <= anglast + 45 degrees
        if not self.isWaterOpen:
            if not (ang1 - 45 <= wdir):
                print("Error: wdir must be at least 45 degrees less than the first fetch angle.")
                return
            if not (wdir <= (ang1 + (Nfet - 1)*dang)):
                print("Error: wdir must be at most 45 degrees more than the final fetch angle.")
                return

        ue = WADJ(Uobs*conversionSpeed,\
            zobs*conversionDist,\
            dtemp,\
            F*conversionDistLrg,\
            duro*hr2s,\
            durf*hr2s,\
            lat*deg2rad,\
            self.windobs)

        ua, Hmo, Tp, wgmsg = WGRO(d*conversionDist,\
            F*conversionDistLrg,\
            phi,
            durf*hr2s,\
            ue,\
            self.wgtyp)

        dataDict = {"zobs": zobs, "Uobs": Uobs, "dtemp": dtemp,\
            "duro": duro, "durf": durf, "lat": lat, "F": F,\
            "d": d, "wdir": wdir, "dang": dang, "ang1": ang1}
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("zobs\t%6.2f %s\n" % (dataDict["zobs"], self.labelUnitDist))
        self.fileRef.write("uobs\t%6.2f %s\n" % (dataDict["Uobs"], self.labelSpeedFinal))
        self.fileRef.write("dtemp\t%6.2f deg\n" % dataDict["dtemp"])
        self.fileRef.write("duro\t%6.2f hr\n" % dataDict["duro"])
        self.fileRef.write("durf\t%6.2f hr\n" % dataDict["durf"])
        self.fileRef.write("lat\t%6.2f deg\n" % dataDict["lat"])

        if self.isWaterOpen:
            self.fileRef.write("F\t%6.2f %s\n" % (dataDict["F"], self.labelUnitDistLrg))

        if self.isWaterShallow:
            self.fileRef.write("d\t%6.2f %s\n" % (dataDict["d"], self.labelUnitDist))

        if not self.isWaterOpen:
            self.fileRef.write("wdir\t%6.2f deg\n" % dataDict["wdir"])

        self.fileRef.write("\nOutput\n")
    # end fileOutputWriteData


driver = WindAdj(zobs = 30.0, Uobs = 45.0, dtemp = -3.0, duro = 5.0,\
    durf = 5.0, lat = 47.0, wdir = 125.0, dang = 12.0, ang1 = 0.0)