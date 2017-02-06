# from snells_law import *
from linear_wave_theory import *

def main():
    # temp = SnellOutput()
    # temp = snellsLaw(6, 10, 18, 6, 100, 13)
    # temp.toString()
    temp = LinearWaveTheoryOutput()
    temp = linearWaveTheory(6.30, 8, 20.0, -12.0, 0.75)
    temp.toString()

main()

# temporarily placing here
class SnellOutput:
    # input
    H1 = 0
    T = 0
    d1 = 0
    alpha1 = 0
    cotphi = 0
    d2 = 0
    # output
    H0 = 0
    H2 = 0
    alpha0 = 0
    alpha2 = 0
    L0 = 0
    L1 = 0
    L2 = 0
    c1 = 0
    c0 = 0
    c2 = 0
    cg1 = 0
    cg0 = 0
    cg2 = 0
    E1 = 0
    E0 = 0
    E2 = 0
    P1 = 0
    P0 = 0
    P2 = 0
    HL = 0
    Ur1 = 0
    Ur2 = 0
    Hb = 0
    db = 0

    def __init__(self): pass

    def toString(self):
        print("\t\t\t %s \t\t %s \t\t %s \n" % ("Known", "Deepwater", "Subject"));
        print("%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \n" % ("Wave height", self.H1, self.H0, self.H2))
        print("%s \t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \n" % ("Wave crest angle", self.alpha1, self.alpha0, self.alpha2))
        print("%s \t\t %-5.2f \t\t %-5.2f \t\t %-5.2f \n" % ("Wavelength", self.L1, self.L0, self.L2))
        print("%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \n" % ("Celerity", self.c1, self.c0, self.c2))
        print("%s \t\t %-5.2f \t\t %-5.2f \t\t\t %-5.2f \n" % ("Group speed", self.cg1, self.cg0, self.cg2))
        print("%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \n" % ("Energy density", self.E1, self.E0, self.E2))
        print("%s \t\t %-8.2f \t %-8.2f \t\t %-8.2f \n" % ("Energy flux", self.P1, self.P0, self.P2))
        print("%s \t\t %-5.2f \t\t %-5.2f \n" % ("Ursell number", self.Ur1, self.Ur2))
        print("%s \t\t\t\t\t %-5.2f \n" % ("Wave steepness", self.HL))
        print("\n")
        print("%s \n" % ("Breaking parameters"))
        print("%s \t %-5.2f \n" % ("Breaking height", self.Hb))
        print("%s \t %-5.2f \n" % ("Breaking depth", self.db))
