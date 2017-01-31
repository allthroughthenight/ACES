from helper_functions import *

def snellsLaw(H1, T, d1, alpha1, cotphi, d2):
    output = SnellOutput()
    output.H1, output.T, output.d1, output.alpha1, output.cotphi, output.d2 = H1, T, d1, alpha1, cotphi, d2
    rho = 1.989
    g = 32.17
    m = 1 / cotphi

    # is this right? wtf
    # if H1 < (d1 * 0.78):
    #    print "Error: Known wave broken"
    #    return;
    #else :
    output.Hb = d1 * 0.78

    % determine known wave properties
    output.c1, output.c0, output.cg1, output.cg0, output.k1, output.L1, output.L0, reldep1 = lwtgen(output.d1, output.T, g)
    # setdown1 not used wtf
    output.E1, output.P1, output.Ur1, setdown1 = lwttm(output.cg1, output.d1, output.H1, output.L1, reldep1, rho, g, output.k1);

    # [steep,maxstp]=ERRSTP(H1,d1,L1);
    # assert(steep<maxstp,'Error: Known wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

    %determine deepwater wave properties
    [alpha0,H0]=LWTDWS(alpha1,c1,cg1,c0,H1);

    E0=(1/8)*rho*g*(H0^2);
    P0=E0*cg0;
    HL=H0/L0;

    # assert(HL<(1/7),'Error: Deepwater wave unstable, [H0/L0] > (1/7)')

    % determine subject wave properties
    output.c2, output.c0, output.cg2, output.cg0, output.k2, output.L2, output.L0, reldep2 = lwtgen(output.d2, output.T, g)
    # kr, ks not used wtf
    output.alpha2, output.H2, kr, ks = lwttws(alpha0,c2,cg2,c0,H0);
    # setdown2 not used wtf
    [E2,P2,Ur2,setdown2]=LWTTWM(cg2, d2, H2, L2, reldep2, rho, g, k2);

    [Hb,db]=ERRWAVBRK3(H0,L0,T,m);
    #assert(H2<Hb,'Error: Subject wave broken (Hb = %6.2f m, hb = %6.2f m)',Hb,db)

    #[steep,maxstp]=ERRSTP(H2,d2,L2);
    #assert(steep<maxstp,'Error: Subject wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

    return output

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
    # syntax - self.test = test

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
