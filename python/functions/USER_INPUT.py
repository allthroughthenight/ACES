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
            fileOutputData.filename = "%s.txt" % (response)

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