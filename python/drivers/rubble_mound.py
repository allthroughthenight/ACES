import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT
from ERRWAVBRK2 import ERRWAVBRK2
from ERRSTP import ERRSTP
from RUNUPR import RUNUPR
from WAVELEN import WAVELEN

## ACES Update to python
#-------------------------------------------------------------
# Driver for Rubble-Mound Revetment Design (page 4-4 in ACES # User's Guide). 
# Provides estimates for revetment armor and bedding layer stone sizes,
# thicknesses, and gradation characteristics. Also calculated are two 
# values of runup on the revetment, an expected extreme and a conservative
# run-up value.

# Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
# Date Created: April 15, 2011
# Date Verified: June 7, 2012 

# Requires the following functions:
# ERRSTP
# ERRWAVBRK2
# RUNUPR
# WAVELEN

# MAIN VARIABLE LIST:
#   INPUT
#   Hs: significant wave height (m)
#   Ts: signficiant wave period (sec)
#   cotnsl: cotangent of nearshore slope
#   ds: water depth at toe of revetment (m)
#   cotssl: cotangent of structure slope
#   unitwt: unit weight of rock (N/m^3)
#   P: permeability coefficient
#   S: damage level

#   OUTPUT
#   w: weight of individual armor and filter stone (N)
#   at: armor/filter layer thickness (m)
#   R: runup (m)
#   ssp: surf-similarity parameter
#   ssz: surf parameter

#   OTHERS
#   ssp: surf-similarity parameter at the transition from plunging to
#   surging waves
#   ssz: surf parameter for given input date
#   rho: density of water (kg/m^3)
#   H20weight: specific weight of water
#   ztp: surf simularity parametet at transition from plunging to surging
#   waves
#   N: number of waves the structure is exposed to (conservative values)
#   CERC_NS: stability number
#-------------------------------------------------------------

class RubbleMound(BaseDriver):
    def __init__(self, Hs = None, Ts = None, cotnsl = None,\
        ds = None, cotssl = None, unitwt = None, P = None, S = None):
        if Hs != None:
            self.isSingleCase = True
            self.defaultValueHs = Hs
        if Ts != None:
            self.isSingleCase = True
            self.defaultValueTs = Ts
        if cotnsl != None:
            self.isSingleCase = True
            self.defaultValue_cotnsl = cotnsl
        if ds != None:
            self.isSingleCase = True
            self.defaultValue_ds = ds
        if cotssl != None:
            self.isSingleCase = True
            self.defaultValue_cotssl = cotssl
        if unitwt != None:
            self.isSingleCase = True
            self.defaultValue_unitwt = unitwt
        if P != None:
            self.isSingleCase = True
            self.defaultValueP = P
        if S != None:
            self.isSingleCase = True
            self.defaultValueS = S

        super(RubbleMound, self).__init__()
    # end __init__

    def userInput(self):
        super(RubbleMound, self).userInput()

        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValueHs"):
            self.inputList.append(BaseField(\
                "Hs: significant wave height (%s)" %\
                (self.labelUnitDist), 0.1, 100.0))
        if not hasattr(self, "defaultValueTs"):
            self.inputList.append(BaseField(\
                "Ts: signficiant wave period (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_cotnsl"):
            self.inputList.append(BaseField(\
                "cotnsl: cotangent of nearshore slope", 5.0, 10000.0))
        if not hasattr(self, "defaultValue_ds"):
            self.inputList.append(BaseField(\
                "ds: water depth at toe of revetment (%s)" %\
                self.labelUnitDist, 0.1, 200.0))
        if not hasattr(self, "defaultValue_cotssl"):
            self.inputList.append(BaseField(\
                "cotssl: cotangent of structure slope", 2.0, 6.0))
        if not hasattr(self, "defaultValue_unitwt"):
            self.inputList.append(BaseField(\
                "unitwt: unit weight of rock (%s/%s^3)" %\
                (self.labelUnitWt, self.labelUnitDist), 1.0, 99999.0))
        if not hasattr(self, "defaultValueP"):
            self.inputList.append(BaseField(\
                "P: permeability coefficient", 0.05, 0.6))
        if not hasattr(self, "defaultValueS"):
            self.inputList.append(BaseField("S: damage level", 2.0, 17.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "rubble_mound")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValueHs"):
            Hs = self.defaultValueHs
        else:
            Hs = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueTs"):
            Ts = self.defaultValueTs
        else:
            Ts = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotnsl"):
            cotnsl = self.defaultValue_cotnsl
        else:
            cotnsl = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ds"):
            ds = self.defaultValue_ds
        else:
            ds = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotssl"):
            cotssl = self.defaultValue_cotssl
        else:
            cotssl = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_unitwt"):
            unitwt = self.defaultValue_unitwt
        else:
            unitwt = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueP"):
            P = self.defaultValueP
        else:
            P = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueS"):
            S = self.defaultValueS
        else:
            S = caseInputList[currIndex]

        return Hs, Ts, cotnsl, ds, cotssl, unitwt, P, S
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        Hs, Ts, cotnsl, ds, cotssl, unitwt, P, S =\
            self.getCalcValues(caseInputList)

        N = 7000

        H20weight = self.g * self.rho

        m = 1.0 / cotnsl

        Hbs = ERRWAVBRK2(Ts, m, ds)
        if not (Hs < Hbs):
            print("Error: Wave broken at structure (Hbs = %6.2f %s" %\
                (Hbs, self.labelUnitDist))
            return

        L, k = WAVELEN(ds, Ts, 50, self.g)

        steep, maxstp = ERRSTP(Hs, ds, L)
        if not (steep < maxstp):
            print("Error: Wave unstable (Max: %0.4f, [H/L] = %0.4f" % (maxstp, steep))
            return

        tanssl = 1.0 / cotssl
        Tz = Ts*(0.67/0.80)
        ssz = tanssl/math.sqrt(2.0*math.pi*Hs/(self.g*Tz**2))

        arg1 = 1.0 / (P + 0.5)
        ssp = (6.2*(P**0.31)*math.sqrt(tanssl))**arg1

        CERC_NS = (1.45/1.27)*(cotssl**(1.0/6.0)) #if change to 1.14, same answer as ACES

        arg2 = (S / math.sqrt(N))**0.2
        plunge_NS = 6.2*(P**0.18)*arg2*(ssz**-0.5)
        surging_NS = 1.0*(P**-0.13)*arg2*math.sqrt(cotssl)*(ssz**P)

        if ssz <= ssp:
            Dutch_NS = plunge_NS
        else:
            Dutch_NS = surging_NS

        Dutch_NS = 1.20*Dutch_NS

        #Stability number used to calculated the mean weight of
        #armor units is the larger of the CERC vs Dutch stability numb
        NS = max(CERC_NS, Dutch_NS)

        w50 = unitwt*(Hs/(NS*((unitwt/H20weight) - 1.0)))**3

        #Minimum thickness of armor layer
        rarmor = 2.0*((w50/unitwt)**(1.0/3.0))

        #Determine bedding/filter layer thickness where %maximum
        #of either rarmor/4 or 1
        rfilter = max(rarmor/4.0, 1.0)

        #Calculate the total horizontal layer thickness (l) of the
        #armor layer and first underlayer
        rt = rarmor + rfilter
        l = rt*math.sqrt(1.0 + (cotssl**2))

        #Compare l to 2*Hs. If l<2*Hs then set L=2*Hs and solve for a new RT. Then
        #calculate a new rarmor and a new rbed.
        if l < (2*Hs):
            l = 2*Hs
            rt = l / math.sqrt(1.0 + (cotssl**2))
            rarmor = rt - rfilter
            rfilter = max(rarmor / 4.0, 1.0)

        #Armor layer weight
        alw0 = (1.0/8.0)*w50
        alw15 = 0.4*w50
        alw50 = w50
        alw85 = 1.96*w50
        alw100 = 4.0*w50

        #Armor layer dimension
        ald0 = (alw0/unitwt)**(1.0/3.0)
        ald15 = (alw15/unitwt)**(1.0/3.0)
        ald50 = (alw50/unitwt)**(1.0/3.0)
        ald85 = (alw85/unitwt)**(1.0/3.0)
        ald100 = (alw100/unitwt)**(1.0/3.0)

        #Bedding/filter layer dimensions
        bld85 = ald15/4.0

        temp1 = math.exp(0.01157*85.0 - 0.5785)
        bld50 = bld85/temp1

        temp1 = math.exp(0.01157*0.0 - 0.5785)
        bld0 = bld50*temp1

        temp1 = math.exp(0.01157*15.0 - 0.5785)
        bld15 = bld50*temp1

        temp1 = math.exp(0.01157*100.0 - 0.5785)
        bld100 = bld50*temp1

        #Filter layer weight
        blw0 = unitwt*(bld0**3)
        blw15 = unitwt*(bld15**3)
        blw50 = unitwt*(bld50**3)
        blw85 = unitwt*(bld85**3)
        blw100 = unitwt*(bld100**3)

        Tp = Ts/0.8

        Lp, k = WAVELEN(ds, Tp, 50, self.g)

        Hm01 = 0.1*Lp*math.tanh(2.0*math.pi*ds/Lp)
        Hm02 = Hs/math.exp(0.00089*((ds/(self.g*(Tp**2)))**(-0.834)))

        Hm0 = min(Hm01, Hm02)

        esp = tanssl / ((2.0*math.pi*Hm0 / (self.g*(Tp**2)))**0.5)

        runupr_max = RUNUPR(Hm0, esp, 1.022, 0.247)
        runupr_conserv = RUNUPR(Hm0, esp, 1.286, 0.247)

        print("Armor layer thickness =  %-6.2f %s" %\
            (rarmor, self.labelUnitDist))
        print("Percent less than by weight\tWeight (%s)\tDimension (%s)" %\
            (self.labelUnitWt, self.labelUnitDist))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (0.0,alw0,ald0))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (15.0,alw15,ald15))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (50.0,alw50,ald50))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (85.0,alw85,ald85))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" % (100.0,alw100,ald100))

        print("Filter layer thickness =  %-6.2f %s" %\
            (rfilter, self.labelUnitDist))
        print("Percent less than by weight\tWeight (%s)\tDimension (%s)" %\
            (self.labelUnitWt, self.labelUnitDist))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (0.0,blw0,bld0))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (15.0,blw15,bld15))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (50.0,blw50,bld50))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f" % (85.0,blw85,bld85))
        print("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" % (100.0,blw100,bld100))

        print("Irregular runup")
        print("Conservative = %-6.2f %s" %\
            (runupr_conserv, self.labelUnitDist))
        print("Expected Maximum = %-6.2f %s" %\
            (runupr_max, self.labelUnitDist))

        dataDict = {"Hs": Hs, "Ts": Ts, "cotnsl": cotnsl, "ds": ds,\
            "cotssl": cotssl, "unitwt": unitwt, "P": P, "S": S,\
            "rarmor": rarmor, "alw0": alw0, "ald0": ald0,\
            "alw15": alw15, "ald15": ald15, "alw50": alw50, "ald50": ald50,\
            "alw85": alw85, "ald85": ald85, "alw100": alw100,\
            "ald100": ald100, "rfilter": rfilter, "blw0": blw0,\
            "bld0": bld0, "blw15": blw15, "bld15": bld15,\
            "blw50": blw50, "bld50": bld50, "blw85": blw85,\
            "bld85": bld85, "blw100": blw100, "bld100": bld100,\
            "runupr_conserv": runupr_conserv, "runupr_max": runupr_max}
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("Hs\t%6.2f %s\n" %\
            (dataDict["Hs"], self.labelUnitDist))
        self.fileRef.write("Ts\t%6.2f s\n" % dataDict["Ts"])
        self.fileRef.write("cotnsl\t%6.2f\n" % dataDict["cotnsl"])
        self.fileRef.write("ds\t%6.2f %s\n" % (dataDict["ds"], self.labelUnitDist))
        self.fileRef.write("cotssl\t%6.2f\n" % dataDict["cotssl"])
        self.fileRef.write("unitwt\t%6.2f %s/%s^3\n" %\
            (dataDict["unitwt"], self.labelUnitWt, self.labelUnitDist))
        self.fileRef.write("P\t%6.2f\n" % dataDict["P"])
        self.fileRef.write("S\t%6.2f\n\n" % dataDict["S"])

        self.fileRef.write("Armor layer thickness =  %-6.2f %s\n" %\
            (dataDict["rarmor"], self.labelUnitDist))
        self.fileRef.write("Percent less than by weight\tWeight (%s)\tDimension (%s)\n" %\
            (self.labelUnitWt, self.labelUnitDist))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (0.0, dataDict["alw0"], dataDict["ald0"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (15.0, dataDict["alw15"], dataDict["ald15"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (50.0, dataDict["alw50"], dataDict["ald50"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (85.0, dataDict["alw85"], dataDict["ald85"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n\n" %\
            (100.0, dataDict["alw100"], dataDict["ald100"]))

        self.fileRef.write("Filter layer thickness =  %-6.2f %s\n" %\
            (dataDict["rfilter"], self.labelUnitDist))
        self.fileRef.write("Percent less than by weight\tWeight (%s)\tDimension (%s)\n" %\
            (self.labelUnitWt, self.labelUnitDist))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (0.0, dataDict["blw0"], dataDict["bld0"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (15.0, dataDict["blw15"], dataDict["bld15"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (50.0, dataDict["blw50"], dataDict["bld50"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n" %\
            (85.0, dataDict["blw85"], dataDict["bld85"]))
        self.fileRef.write("%-3.1f\t\t\t\t%-6.2f\t\t%-6.2f\n\n" %\
            (100.0, dataDict["blw100"], dataDict["bld100"]))

        self.fileRef.write("Irregular runup\n")
        self.fileRef.write("Conservative = %-6.2f %s\n" %\
            (dataDict["runupr_conserv"], self.labelUnitDist))
        self.fileRef.write("Expected Maximum = %-6.2f %s\n" %\
            (dataDict["runupr_max"], self.labelUnitDist))
    # end fileOutputWriteData


driver = RubbleMound()