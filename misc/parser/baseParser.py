class BaseParser(object):
    def __init__(self):
        self.fileRef = open(self.parseFilename)

        fileDataRaw = self.fileRef.read()

        self.fileRef.close()

        self.fileRef = open(self.outputFilename, "w")

        dataList = []
        for token in fileDataRaw.split(self.parseSplitToken)[1:]:
            caseData = {}
            lineIndex = 0
            for line in token.split("\n"):
                caseData = self.getCaseData(caseData, line, lineIndex)
                lineIndex += 1
            # end for loop

            dataList.append(caseData)
        # end for loop

        self.writeData(dataList)

        self.fileRef.close()
    # end __init__

    def matchNameToText(self, line, varName):
        varIndex = line.find(varName + ":")
        nameLen = len(varName) + 1
        
        return varIndex, nameLen
    # end matchNameToText

    def parseVar(self, caseData, line, varName):
        varIndex, nameLen = self.matchNameToText(line, varName)
        if varIndex != -1:
            temp = line[(varIndex + nameLen):].strip()
            caseData[varName] = float(temp.split(" ")[0])

        return caseData
    # end parseVar
    
    def getCaseData(self, caseData, line, lineIndex):
        for varName in self.getVarNameList():
            caseData = self.parseVar(caseData, line, varName)

        return caseData
    # end getCaseData

    def writeData(self, dataList):
        for caseData in dataList:
            line = ""
            firstVarName = True
            for varName in self.getVarNameFileOutputList():
                if varName in caseData:
                    if not firstVarName:
                        line = line + ","
                    line = line + str(caseData[varName])

                    firstVarName = False
            # end for loop

            self.fileRef.write(line + "\n")
        # end for loop
    # end writeData
    
    def getVarNameList(self):
        return self.varNameInputList + self.varNameOutputList
    
    def getVarNameFileOutputList(self):
        return self.varNameInputList + self.varNameOutputList