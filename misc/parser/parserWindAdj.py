from baseParser import BaseParser

class ParserWindAdj(BaseParser):
    def __init__(self):
        self.parseFilename = "wind_adjust/W_IS_11"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsWindAdj2.csv"

        isWaterOpen = True
        isWaterShallow = False

        self.varNameInputList = ["Zobs", "Uobs", "delT", "DurO", "DurF", "LAT"]
        self.varNameOutputList = []
        
        if isWaterOpen:
            self.varNameInputList.append("F")
        if isWaterShallow:
            self.varNameInputList.append("d")
        if not isWaterOpen:
            self.varNameInputList.append("wdir")
            self.varNameOutputList.append("F")
        
        self.varNameOutputList = self.varNameOutputList + ["Ue", "Ua"]
        if not isWaterOpen:
            self.varNameOutputList.append("theta")
        self.varNameOutputList = self.varNameOutputList + ["Hm0", "Tp"]

        super(ParserWindAdj, self).__init__()
    # end __init__

parser = ParserWindAdj()