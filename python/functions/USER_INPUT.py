import sys
from helper_objects import FileOutputData

# TODO: Move to helper functions
def GET_INPUT_FUNC():
    if sys.version_info.major == 2:
        return raw_input
    else:
        return input
# end GET_INPUT_FUNC

def DATA_VALUE(dataField):
    inputFunc = GET_INPUT_FUNC()

    while True:
        response = inputFunc("Enter %s: " % (dataField.desc))
        dataValue = float(response)

        if dataValue >= dataField.min and dataValue <= dataField.max:
            return dataValue
        else:
            print("Must be between %6.2f and %6.2f." % (dataField.min, dataField.max))
# end DATA_VALUE

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