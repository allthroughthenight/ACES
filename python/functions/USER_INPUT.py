import sys
import os.path
from helper_objects import FileOutputData
import numpy as np

# TODO: Move to helper functions
def GET_INPUT_FUNC():
    if sys.version_info.major == 2:
        return raw_input
    else:
        return input
# end GET_INPUT_FUNC

def DATA_VALUE(inputPrompt, valueMin, valueMax):
    inputFunc = GET_INPUT_FUNC()

    while True:
        response = inputFunc("Enter %s: " % (inputPrompt))
        dataValue = float(response)

        if dataValue >= valueMin and dataValue <= valueMax:
            return dataValue
        else:
            print("Must be between %6.2f and %6.2f." % (valueMin, valueMax))
# end DATA_VALUE

def FILE_NAME():
    inputFunc = GET_INPUT_FUNC()

    while True:
        response = inputFunc("Enter the file name to load: ")

        if os.path.isfile(response):
            return response
        else:
            print("'File not found. Please enter a valid file name in a valid folder.")
# end FILE_NAME

def FILE_OUTPUT(enterFilename = False, enterFileDesc = False):
    inputFunc = GET_INPUT_FUNC()
    fileOutputData = FileOutputData()

    accepted = False
    while not accepted:
        response = inputFunc("Would you like to save the results to a file? (Y or N): ")

        if response == "Y" or response == "y":
            accepted = True
            fileOutputData.saveOutput = True
        elif response == "N" or response == "n":
            accepted = True
            fileOutputData.saveOutput = False
        else:
            print("Must enter Y or N.")

    if fileOutputData.saveOutput:
        if enterFilename:
            response = inputFunc("Enter the filename (no extension): ")
            fileOutputData.filename = response

        if enterFileDesc:
            response = inputFunc("Enter the description for this file: ")
            fileOutputData.fileDesc = response

    return fileOutputData
# end FILE_OUTPUT

def FINITE_CHOICE(promptMsg, choiceList):
    inputFunc = GET_INPUT_FUNC()
    while True:
        choiceValue = inputFunc(promptMsg)

        if choiceValue in choiceList:
            return choiceValue
        else:
            print("Must be one of the choices specified.")
# end FINITE_CHOICE

def METRIC_IMPERIAL():
    inputFunc = GET_INPUT_FUNC()

    while True:
        response = inputFunc("Input in imperial or SI units? (I or S): ")

        if response == "I" or response == "i":
            return False, 32.17, "ft", "lb"
        elif response == "S" or response == "s":
            return True, 9.81, "m", "N"
        else:
            print("I or S only")
# end METRIC_IMPERIAL

def MULTI_FILE():
    filename = FILE_NAME()

    dataOutputList = []
    with open(filename) as fileData:
        for line in fileData:
            dataOutputList.append([float(i) for i in line[:-1].split(",")])

    return dataOutputList
# end MULTI_FILE

def MULTI_INCR(inputList):
    inputFunc = GET_INPUT_FUNC()

    dataTempList = []
    for field in inputList:
        fieldMin = DATA_VALUE("minimum " + field.desc,\
            field.min, field.max)

        if fieldMin == field.max:
            fieldMax = fieldMin
            print("Maximum %s automatically set to %.2f" % (field.desc, field.max))
        else:
            fieldMax = DATA_VALUE("maximum " + field.desc,\
                field.min, field.max)

        dataTempList.append([fieldMin, fieldMax])

    numCases = DATA_VALUE("the number of cases", 2, 200)
    numCases = int(numCases)

    dataOutputList = []
    for dataInfo in dataTempList:
        varMin = dataInfo[0]
        varMax = dataInfo[1]

        dataOutputList.append(np.linspace(varMin, varMax, numCases))
    dataOutputList = zip(*dataOutputList)

    return dataOutputList
# end MULTI_INCR

def MULTI_MODE(inputList):
    inputFunc = GET_INPUT_FUNC()

    while True:
        response = inputFunc("Enter File mode, Random mode or Increment mode (F, R, or I): ")

        if response == "F" or response == "f":
            return MULTI_FILE()
        elif response == "R" or response == "r":
            return MULTI_RANDOM(inputList)
        elif response == "I" or response == "i":
            return MULTI_INCR(inputList)
        else:
            print("Must be F, R or I")
    # end while loop
# end MULTI_MODE

def MULTI_RANDOM(inputList):
    inputFunc = GET_INPUT_FUNC()

    numCases = DATA_VALUE("the number of cases (1 - 20)", 1, 20)
    numCases = int(numCases)

    dataOutputList = []
    for caseIndex in range(numCases):
        print("-- Data Set #%d -------------------------------" % (caseIndex + 1))

        dataTempList = []
        for field in inputList:
            dataTempList.append(DATA_VALUE(field.desc, field.min, field.max))

        dataOutputList.append(dataTempList)

    return dataOutputList
# end MULTI_RANDOM

def ROUGH_SLOPE_COEFFICIENTS(\
    has_rough_slope,\
    has_overtopping,\
    has_runup,\
    inputDict):
#   Required input arguments:
#       numCases: the number of cases for multi-case runs (1 for single
#       case)
#
#   Optional input arguments:
#       R_default: the default value for R
#
#   Output arguments:
#       numConsts: the number of constants being returned
#       a:
#       b:
#       alpha:
#       Qstar0:
#       U:
#       R:
    inputFunc = GET_INPUT_FUNC()

    conversionKnots2mph = 1.15077945 #1 knots = 1.15077945 mph
    outputDict = {"numConsts": 0}

    if has_rough_slope:
        outputDict["numConsts"] += 2
    if has_overtopping:
        outputDict["numConsts"] += 3
    if not has_runup:
        outputDict["numConsts"] += 1

    if has_rough_slope:
        #Empirical coefficients for rough slope runup
        outputDict["a"] = 0.956
        outputDict["b"] = 0.398
        
        print("a = %-6.4f" % outputDict["a"])
        print("b = %-6.4f" % outputDict["b"])
    # end if

    if has_overtopping:
        #Empirical coefficients and values for overtopping
        outputDict["alpha"] = 0.076463
        outputDict["Qstar0"] = 0.025
        outputDict["U"] = 35.0*conversionKnots2mph
        
        print("alpha = %-6.4f" % outputDict["alpha"])
        print("Qstar0 = %-6.4f" % outputDict["Qstar0"])
        print("U = %-6.4f knots" % (outputDict["U"]/conversionKnots2mph))

        if not has_runup and "R_default" in inputDict:
            outputDict["R"] = inputDict["R_default"]
    # end if

    custom_const = FINITE_CHOICE(\
        "Use default constant values or load from file? (D or F): ",\
        ["D", "d", "F", "f"])
    custom_const = custom_const == "F" or custom_const == "f"

    if custom_const:
        accepted = False
        while not accepted:
            fileData = MULTI_FILE()
            print(fileData)

            optVarNum = 0
            if len(fileData[0]) == outputDict["numConsts"]:
                if len(fileData) == 1:
                    accepted = True

                    if has_rough_slope:
                        outputDict["a"] = fileData[0][optVarNum]
                        outputDict["b"] = fileData[0][optVarNum + 1]

                        optVarNum += 2

                    if has_overtopping:
                        outputDict["alpha"] = fileData[0][optVarNum]
                        outputDict["Qstar0"] = fileData[0][optVarNum + 1]
                        outputDict["U"] =\
                            fileData[0][optVarNum + 2]*conversionKnots2mph

                        optVarNum += 3

                    if not has_runup:
                        outputDict["R"] = fileData[0][optVarNum]
                elif len(fileData) == inputDict["numCases"]:
                    accepted = True

                    for key in ["a", "b", "alpha", "Qstar0", "U", "R"]:
                        if key in outputDict:
                            del outputDict[key]

                    if has_rough_slope:
                        outputDict["aList"] =\
                            [caseData[optVarNum] for caseData in fileData]
                        outputDict["bList"] =\
                            [caseData[optVarNum + 1] for caseData in fileData]

                        optVarNum += 2
                    # end if

                    if has_overtopping:
                        outputDict["alphaList"] =\
                            [caseData[optVarNum] for caseData in fileData]
                        outputDict["Qstar0List"] =\
                            [caseData[optVarNum + 1] for caseData in fileData]
                        outputDict["UList"] =\
                            [caseData[optVarNum + 2]*conversionKnots2mph for caseData in fileData]

                        optVarNum += 3

                    if not has_runup:
                        outputDict["RList"] =\
                            [caseData[optVarNum] for caseData in fileData]
                else:
                    print("Wrong number of cases. Expected either 1 or %d, found %d" %\
                        (inputDict["numCases"], len(fileData)))
                # end if
            else:
                print("Wrong number of constants. Expected %d, found %d." %\
                    (outputDict["numConsts"], len(fileData[0])))
            # end if
        # end while
    # end if

    return outputDict
# end ROUGH_SLOPE_COEFFICIENTS

def SALT_FRESH_WATER(isMetric):
    inputFunc = GET_INPUT_FUNC()

    waterType = FINITE_CHOICE(\
        "Fresh or Salt water? (F or S): ",\
        ["F", "f", "S", "s"])

    if waterType == "S" or waterType == "s":
        if isMetric:
            rho = 1025.09 # kg/m^3, (sea water)
        else:
            rho = 1.989 # rho/g = 63.99/32.17 lb sec^2/ft^4 (sea water)
    else:
        if isMetric:
            rho = 999.8 # kg/m^3 ( fresh water)
        else:
            rho = 1.940 # rho/g = 62.415475/32.17 lb sec^2/ft^4 (fresh water)

    return waterType, rho
# end SALT_FRESH_WATER

def SINGLE_MULTI_CASE():
    inputFunc = GET_INPUT_FUNC()

    # Ask user for single or multi-input
    while True:
        response = inputFunc("Single or Multi-case? (s or m): ")

        if response == "S" or response == "s":
            return True
        elif response == "M" or response == "m":
            return False
        else:
            print("s or m only\n")
# end SINGLE_MULTI_CASE