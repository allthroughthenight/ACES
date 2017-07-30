from baseParser import BaseParser

class ParserSnellsLaw(BaseParser):
    def __init__(self):
        self.parseFilename = "snells/S_IF"
        self.parseSplitToken = "________________________________________________________________________________"
        self.outputFilename = "resultsSnellsLaw.csv"

        self.varNameInputList = ["H1", "T", "d1", "Alpha1",\
            "COTAN NS Slope", "d2"]
        self.varNameOutputList = ["H1", "H0", "H2", "Alpha1", "Alpha0", "Alpha2",\
            "L1", " L0", "L2", "C1", "C0", "C2", "Cg1", "Cg0", "Cg2",\
            "E1", "E0", "E2", "P1", "P0", "P2", "U1", "U2",\
            "H0/L0", "Hb", "db"]

        super(ParserSnellsLaw, self).__init__()
    # end __init__

parser = ParserSnellsLaw()