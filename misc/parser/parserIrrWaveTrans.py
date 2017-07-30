from baseParser import BaseParser

class ParserIrrWaveTrans(BaseParser):
    def __init__(self):
        self.parseFilename = "G_IS"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsIrrWaveTrans.csv"

        self.varNameInputList = ["PRINCIPAL DIRECTION"]
        self.varNameOutputList = ["Hrms", "Hmed", "H(1/3)", "H(1/10)", "H(1/100)"]

        super(ParserIrrWaveTrans, self).__init__()
    # end __init__
    
    def matchNameToText(self, line, varName):
        varIndex = line.find(varName + ":")
        nameLen = len(varName) + 1
        
        return varIndex, nameLen
    # end matchNameToText

parser = ParserIrrWaveTrans()