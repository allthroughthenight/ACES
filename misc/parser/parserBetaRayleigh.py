from baseParser import BaseParser

class ParserBetaRayleigh(BaseParser):
    def __init__(self):
        self.parseFilename = "B_IS"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsBetaRayleigh.csv"

        self.varNameInputList = ["Hmo", "Tp", "Depth"]
        self.varNameOutputList = ["Hrms", "Hmed", "H(1/3)", "H(1/10)", "H(1/100)"]

        super(ParserBetaRayleigh, self).__init__()
    # end __init__

parser = ParserBetaRayleigh()