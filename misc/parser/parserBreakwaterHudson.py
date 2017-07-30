from baseParser import BaseParser

class ParserBreakwaterHudson(BaseParser):
    def __init__(self):
        self.parseFilename = "hudson/H_IF"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsBreakwaterHudson.csv"

        self.varNameInputList = ["(Wr)", "(H) ", "(Kd)", "(K^)", "(P) ",\
            "Cotangent of Structure Slope     ", "(n) "]
        self.varNameOutputList = ["(W) ", "(B) ", "(r) ", "(Nr)"]

        super(ParserBreakwaterHudson, self).__init__()
    # end __init__

parser = ParserBreakwaterHudson()