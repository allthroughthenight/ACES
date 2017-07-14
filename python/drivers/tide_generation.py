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

def TideGeneration():

        'year simulation starts (YYYY)', 1900, 2050;...
        'month simulation starts (MM)', 1, 12;...
        'day simulation starts (DD)', 1, 31;...
        'hour simulation starts (HH.H)', 0, 24;...
        'length of record (tlhrs) (HH.H)', 0, 744;...
        'output time interval (min)', 1, 60;...
        ['mean water level height above datum [' labelUnitDist ']'], -100, 100;...
        'gauge longitude (deg)', -180, 180};

    # MIGHT CHANGE IT AFTER CONFIRMATION

class TideGeneration(BaseDriver):
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
            self.defaultValuemon = mon
        if day != None:
            self.isSingleCase = True
            self.defaultValue_day = day
        if hr != None:
            self.isSingleCase = True
            self.defaultValue_hr = hr
        if tlhrs != None:
            self.isSingleCase = True
            self.defaultValuetlhrs = tlhrs
        if delt != None:
            self.isSingleCase = True
            self.defaultValue_delt = delt
        if gauge0 != None:
            self.isSingleCase = True
            self.defaultValue_gauge0 = gauge0
        if glong != None:
            self.isSingleCase = True
            self.defaultValue_glong = glong

        super(TideGeneration, self).__init__()
    # end __init__

    def userInput(self):
        super(TideGeneration, self).userInput()

    # end userInput

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
                "gauge0: mean water level height above datum", -100, 100))
        if not hasattr(self, "defaultValue_glong"):
            self.inputList.append(BaseField(\
                "glong: gauge longitude (deg)", -180, 180))
    # end defineInputDataList

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
            glong = caseInputList[currIndex]

        return year, mon, day, hr, tlhrs, delt, gauge0, glong
    # end getCalcValues

    def performCalculations(self, caseInputList, caseIndex = 0):
        year, mon, day, hr, tlhrs, delt, gauge0, glong = self.getCalcValues(caseInputList)

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

    # end performCalculations

driver = TideGeneration()
