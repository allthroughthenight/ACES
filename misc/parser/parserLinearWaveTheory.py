from baseParser import BaseParser

class ParserLinearWaveTheory(BaseParser):
    def __init__(self):
        self.parseFilename = "linear/L_IF"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsLinearWaveTheory.csv"

        self.varNameInputList = ["Vert Coord", "Wavelen Frac"]
        self.varNameOutputList = ["Water Surf", "Pressure"]

        super(ParserLinearWaveTheory, self).__init__()
    # end __init__
    
    def getCaseData(self, caseData, line, lineIndex):
        caseData = super(ParserLinearWaveTheory, self).getCaseData(\
            caseData, line, lineIndex)
        
        if lineIndex == 5:
            dataList = line.strip().split(" ")
            while "" in dataList:
                dataList.remove("")
            
            # Correct error where two values appear to be 1
            if len(dataList) == 8:
                dataList = dataList[:2] + [dataList[2][:7]] +\
                    [dataList[2][7:]] + dataList[3:]
            
            caseData["H"] = dataList[0]
            caseData["T"] = dataList[1]
            caseData["d"] = dataList[2]
            caseData["L"] = dataList[3]
            caseData["C"] = dataList[4]
            caseData["Cg"] = dataList[5]
            caseData["E"] = dataList[6]
            caseData["Ef"] = dataList[7]
            caseData["Ur"] = dataList[8]
        
        nameList = ["Displac:", "Velocity:", "Acceler:"]
        for i in nameList:
            lineIndex = line.find(i)
            if lineIndex != -1:
                temp = line[(lineIndex + len(i) + 1):]
                
                paramList = temp.split(" ")
                while "" in paramList:
                    paramList.remove("")
                
                if i == nameList[0]:
                    caseData["px"] = paramList[0]
                    caseData["py"] = paramList[1]
                if i == nameList[1]:
                    caseData["u"] = paramList[0]
                    caseData["w"] = paramList[1]
                else:
                    caseData["dudt"] = paramList[0]
                    caseData["dwdt"] = paramList[1]
        
        return caseData
    # end getCaseData
    
    def getVarNameFileOutputList(self):
        return ["H", "T", "d", "Vert Coord", "Wavelen Frac",\
            "L", "C", "Cg", "E", "Ef", "Ur", "Water Surf", "px", "py",\
            "u", "w", "dudt", "dwdt", "Pressure"]

parser = ParserLinearWaveTheory()