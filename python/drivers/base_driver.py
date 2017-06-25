import USER_INPUT

class BaseDriver(object):
    def __init__(self):
        self.userInput()

        self.fileOutputRequestInit()

        if self.isSingleCase:
            self.performCalculations(self.dataOutputList)
        else:
            caseIndex = 0
            for caseData in self.dataOutputList:
                self.performCalculations(caseData, caseIndex)
                caseIndex = caseIndex + 1
        # end performCalculations if

        # Close file if applicable
        if self.fileOutputData.saveOutput:
            self.fileRef.close()
    # end __init__

    def userInput(self):
        # Allow the user to override single / multicase
        # by defining it before this function
        if not hasattr(self, "isSingleCase"):
            self.isSingleCase = USER_INPUT.SINGLE_MULTI_CASE()

        self.isMetric, self.g, self.labelUnitDist, self.labelUnitWt =\
            USER_INPUT.METRIC_IMPERIAL()

        self.defineInputDataList()

        if self.isSingleCase:
            self.dataOutputList = []
            for field in self.inputList:
                self.dataOutputList.append(USER_INPUT.DATA_VALUE(\
                    field.desc, field.min, field.max))
        else:
            self.dataOutputList = USER_INPUT.MULTI_MODE(self.inputList)
    # end userInput

    def fileOutputRequestMain(self, defaultFilename = None, requestDesc = False):
        filePath = "output/"
        if defaultFilename == None:
            requestFilename = True
        else:
            requestFilename = False

        self.fileOutputData = USER_INPUT.FILE_OUTPUT(requestFilename, requestDesc)

        if requestFilename:
            self.fileOutputData.filename = filePath +\
                self.fileOutputData.filename + ".txt"
        else:
            self.fileOutputData.filename = filePath + defaultFilename + ".txt"

        if self.fileOutputData.saveOutput:
            self.fileRef = open(self.fileOutputData.filename, "w")
    # end fileOutputRequest

    def fileOutputWriteMain(self, dataDict, caseIndex = 0):
        if self.fileOutputData.saveOutput:
            if not self.isSingleCase:
                if caseIndex != 0:
                    self.fileRef.write("\n--------------------------------------\n\n")
                self.fileRef.write("Case #%d\n\n" % (caseIndex + 1))
            # end if

            self.fileOutputWriteData(dataDict)
        # end file output if
    # end fileOutputWriteBase

    # Override Methods ###################################################
    # Must be overridden by subclass
    def defineInputDataList(self):
        pass

    def fileOutputRequestInit(self):
        pass

    def performCalculations(self, caseInputList, caseIndex = 0):
        pass

    def fileOutputWriteData(self, dataDict):
        pass
# end base_driver