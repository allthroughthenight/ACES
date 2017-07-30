from baseParser import BaseParser

class ParserIrregularRunup(BaseParser):
    def __init__(self):
        self.parseFilename = "irr_runup/IR_IS"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsIrregularRunup.csv"

        self.varNameInputList = ["Hos", "Tp", "COTAN", ]
        self.varNameOutputList = ["Rmax", "R2", "R1/10", "R1/3", "Rbar"]

        super(ParserIrregularRunup, self).__init__()
    # end __init__

parser = ParserIrregularRunup()