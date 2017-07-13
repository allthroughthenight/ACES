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

## ACES Update to MATLAB
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

def tide_generation():

    metric, g, labelUnitDist, labelUnitWt = USER_INPUT_METRIC_IMPERIAL();

    inputDataList = {...
        'year simulation starts (YYYY)', 1900, 2050;...
        'month simulation starts (MM)', 1, 12;...
        'day simulation starts (DD)', 1, 31;...
        'hour simulation starts (HH.H)', 0, 24;...
        'length of record (tlhrs) (HH.H)', 0, 744;...
        'output time interval (min)', 1, 60;...
        ['mean water level height above datum [' labelUnitDist ']'], -100, 100;...
        'gauge longitude (deg)', -180, 180};
    [outputDataList] = USER_INPUT_FILE_INPUT_SINGLE(inputDataList);


    # MIGHT CHANGE IT AFTER CONFIRMATION
    m2ft = 3.28084
    if metric
        gauge0 = gauge0 * m2ft

    delthr=delt/60

    nogauge = 1 # one gauge is examined.

    acst=[28.9841042,30.0,28.4397295,15.0410686,57.9682084,13.9430356,86.9523127,44.0251729,60.0,57.4238337,28.5125831,90.0,27.9682084,27.8953548,16.1391017,29.4556253,15.0,14.4966939,15.5854433,0.5443747,0.0821373,0.0410686,1.0158958,1.0980331,13.4715145,13.3986609,29.9589333,30.0410667,12.8542862,14.9589314,31.0158958,43.4761563,29.5284789,42.9271398,30.0821373,115.9364169,58.9841042]

    pcst=[2,2,2,1,4,1,6,3,4,4,2,6,2,2,1,2,1,1,1,0,0,0,0,0,1,1,2,2,1,1,2,3,2,3,2,8,4]

    ## Intialize gage-specific info relevant to harmonic constituents
    alpha,fndcst=GAGINI(nogauge,year,mon,day,hr,tlhrs,glong,ep,acst,pcst)

    ntid=floor(tlhrs/delthr)+1

    tidelv = []
    xtim = []
    for i in ntid
        xtim[i]=(i-1)*delthr
        tidelv[i]=TIDELV(nogauge,xtim[i],amp,alpha,fndcst,acst)

    ytide=gauge0+tidelv

    plt.xlabel('Time [hr]')
    plt.ylabel(['Elevation [' labelUnitDist ']'])
    plt.title('Tide Elevations [from constituents]')
    plt.plot(xtim,ytide)
    plt.show()

class ToeDesign(BaseDriver):
    def __init__(self, year = None, mon = None, day = None, hr = None,\
        tlhrs = None, delt = None, gauge0 = None, glong = None):
    year
#   Hi: wave height (m)
    mon
#   T: wave period (sec)
    day
#   ds: water depth at structure (m)
    hr
#   cotphi: cotangent of nearshore slope
    tlhrs
#   Kp: passive earth pressure coefficient
    delt
#   de: sheet - pile penetration depth (m)
    gauge0
#   ht: height of toe protection layer above mudline
    glong
#   unitwt: unit weight of rock (N / m^3)
        if year != None:
            self.isSingleCase = True
            self.defaultValue_year = year
        if mon != None:
            self.isSingleCase = True
            self.defaultValue_mon = mon
        if day != None:
            self.isSingleCase = True
            self.defaultValue_day = day
        if cotphi != None:
            self.isSingleCase = True
            self.defaultValue_cotphi = cotphi
        if Kp != None:
            self.isSingleCase = True
            self.defaultValueKp = Kp
        if de != None:
            self.isSingleCase = True
            self.defaultValue_de = de
        if ht != None:
            self.isSingleCase = True
            self.defaultValue_ht = ht
        if unitwt != None:
            self.isSingleCase = True
            self.defaultValue_unitwt = unitwt

        super(ToeDesign, self).__init__()
    # end __init__

    def userInput(self):
        super(ToeDesign, self).userInput()

        self.water, self.rho = USER_INPUT.SALT_FRESH_WATER(self.isMetric)
    # end userInput

    def defineInputDataList(self):
        self.inputList = []

        if not hasattr(self, "defaultValue_year"):
            self.inputList.append(BaseField(\
                "Hi: wave height (%s)" % (self.labelUnitDist), 0.1, 100.0))
        if not hasattr(self, "defaultValueT"):
            self.inputList.append(BaseField(\
                "T: wave period (sec)", 1.0, 1000.0))
        if not hasattr(self, "defaultValue_ds"):
            self.inputList.append(BaseField(\
                "ds: water depth at structure (%s)" % (self.labelUnitDist), 0.1, 200.0))
        if not hasattr(self, "defaultValue_cotphi"):
            self.inputList.append(BaseField(\
                "cotphi: cotangent of nearshore slope", 5.0, 10000.0))
        if not hasattr(self, "defaultValueKp"):
            self.inputList.append(BaseField(\
                "Kp: passive earth pressure coefficient", 0.0, 50.0))
        if not hasattr(self, "defaultValue_de"):
            self.inputList.append(BaseField(\
                "de: sheet-pile penetration depth (%s)" % (self.labelUnitDist), 0.0, 200.0))
        if not hasattr(self, "defaultValue_ht"):
            self.inputList.append(BaseField(\
                "ht: height of toe protection layer above mudline (%s)" % (self.labelUnitDist), 0.1, 200.0))
        if not hasattr(self, "defaultValue_unitwt"):
            self.inputList.append(BaseField(\
                "unitwt: unit weight of rock (%s/%s^3)" % (self.labelUnitWt, self.labelUnitDist), 1.0, 99999.0))
    # end defineInputDataList

    def fileOutputRequestInit(self):
        self.fileOutputRequestMain(defaultFilename = "toe_design")

    def getCalcValues(self, caseInputList):
        currIndex = 0

        if hasattr(self, "defaultValue_year"):
            year = self.defaultValue_year
        else:
            year = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueT"):
            T = self.defaultValueT
        else:
            T = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ds"):
            ds = self.defaultValue_ds
        else:
            ds = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_cotphi"):
            cotphi = self.defaultValue_cotphi
        else:
            cotphi = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValueKp"):
            Kp = self.defaultValueKp
        else:
            Kp = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_de"):
            de = self.defaultValue_de
        else:
            de = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_ht"):
            ht = self.defaultValue_ht
        else:
            ht = caseInputList[currIndex]
            currIndex = currIndex + 1

        if hasattr(self, "defaultValue_unitwt"):
            unitwt = self.defaultValue_unitwt
        else:
            unitwt = caseInputList[currIndex]

        return year, T, ds, cotphi, Kp, de, ht, unitwt
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        H, T, ds, cotphi, Kp, de, ht, unitwt =\
            self.getCalcValues(caseInputList)

        H20weight = self.g * self.rho

        specgrav = unitwt / H20weight

        dl = ds - ht
        m = 1.0 / cotphi

        if not (ds / (T**2) > 0.0037424):
            print("Error: Limiting value detected...Hbs cannot be solved.")
            return

        Hbs = ERRWAVBRK2(T, m, ds)
        if not (H < Hbs):
            print("Error: Wave broken at structure (Hbs = %6.2f %s" %\
                (Hbs, self.labelUnitDist))

        L, k = WAVELEN(dl, T, 50, self.g)

        steep, maxstp = ERRSTP(H, dl, L)
        if not (steep < maxstp):
            print("Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f" % (maxstp, steeps))

        b1 = de*Kp
        b2 = 2.0*H
        b3 = 0.4*ds
        b = [1.0, b1, b2, b3]
        b = max(b)

        arg1 = (4.0*math.pi*dl/L)
        kappa = (arg1/math.sinh(arg1))*((math.sin(2.0*math.pi*b/L))**2)
        arg2 = ((1.0 - kappa)/(kappa**(1.0/3.0)))*(dl/H)
        Ns = 1.3*arg2 + 1.8*math.exp(-1.5*(1.0 - kappa)*arg2)

        Ns = max(Ns, 1.8)

        w = (unitwt*(H**3))/((Ns**3)*((specgrav - 1.0)**3))

        print("\nWidth of toe apron\t\t%6.2f %s" %\
            (b, self.labelUnitDist))
        print("Weight of individual armor unit\t%6.2f %s" %\
            (w, self.labelUnitWt))
        print("Water depth at top of tow\t%6.2f %s" %\
            (dl, self.labelUnitDist))

        dataDict = {"H": H, "T": T, "ds": ds, "cotphi": cotphi,\
            "Kp": Kp, "de": de, "ht": ht, "unitwt": unitwt,\
            "b": b, "w": w, "dl": dl}
        self.fileOutputWriteMain(dataDict, caseIndex)
    # end performCalculations

    def fileOutputWriteData(self, dataDict):
        self.fileRef.write("Input\n")
        self.fileRef.write("H\t\t\t\t%6.2f %s\n" %\
            (dataDict["H"], self.labelUnitDist))
        self.fileRef.write("T\t\t\t\t%6.2f s\n" % dataDict["T"])
        self.fileRef.write("ds\t\t\t\t%6.2f %s\n" %\
            (dataDict["ds"], self.labelUnitDist))
        self.fileRef.write("cotphi\t\t\t\t%6.2f\n" % dataDict["cotphi"])
        self.fileRef.write("Kp\t\t\t\t%6.2f\n" % dataDict["Kp"])
        self.fileRef.write("de\t\t\t\t%6.2f %s\n" %\
            (dataDict["de"], self.labelUnitDist))
        self.fileRef.write("ht\t\t\t\t%6.2f %s\n" %\
            (dataDict["ht"], self.labelUnitDist))
        self.fileRef.write("unitwt\t\t\t\t%6.2f %s/%s^3\n" %\
            (dataDict["unitwt"], self.labelUnitWt, self.labelUnitDist))

        self.fileRef.write("\nWidth of toe apron\t\t%6.2f %s\n" %\
            (dataDict["b"], self.labelUnitDist))
        self.fileRef.write("Weight of individual armor unit\t%6.2f %s\n" %\
            (dataDict["w"], self.labelUnitWt))
        self.fileRef.write("Water depth at top of tow\t%6.2f %s\n" %\
            (dataDict["dl"], self.labelUnitDist))
    # end fileOutputWriteData


driver = ToeDesign()

tide_generation()
