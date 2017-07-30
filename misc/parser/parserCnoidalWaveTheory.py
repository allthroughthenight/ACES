from baseParser import BaseParser

class ParserCnoidalWaveTheory(BaseParser):
    def __init__(self):
        self.parseFilename = "cnoidal/C_IF"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsCnoidalWaveTheory.csv"

        self.varNameInputList = ["Vert Coord", "Wavelen Frac"]
        self.varNameOutputList = ["Water Surf", "Pressure"]

        super(ParserCnoidalWaveTheory, self).__init__()
    # end __init__
    
    def getCaseData(self, caseData, line, lineIndex):
        caseData = super(ParserCnoidalWaveTheory, self).getCaseData(\
            caseData, line, lineIndex)
        
        if lineIndex == 5:
            dataList = line.strip().split(" ")
            while "" in dataList:
                dataList.remove("")
            
            caseData["H"] = dataList[0]
            caseData["T"] = dataList[1]
            caseData["d"] = dataList[2]
            caseData["O"] = dataList[8]
            caseData["L"] = dataList[3]
            caseData["C"] = dataList[4]
            caseData["E"] = dataList[5]
            caseData["Ef"] = dataList[6]
            caseData["Ur"] = dataList[7]
        
        nameList = ["Velocity:", "Acceler:"]
        for i in nameList:
            lineIndex = line.find(i)
            if lineIndex != -1:
                temp = line[(lineIndex + len(i) + 1):]
                
                paramList = temp.split(" ")
                while "" in paramList:
                    paramList.remove("")
                
                if i == nameList[0]:
                    caseData["u"] = paramList[0]
                    caseData["w"] = paramList[1]
                else:
                    caseData["dudt"] = paramList[0]
                    caseData["dwdt"] = paramList[1]
        
        return caseData
    # end getCaseData
    
    def getVarNameFileOutputList(self):
        return ["H", "T", "d", "Vert Coord", "Wavelen Frac",\
            "L", "C", "E", "Ef", "Ur", "Water Surf", "u", "w",\
            "dudt", "dwdt", "Pressure"]

parser = ParserCnoidalWaveTheory()