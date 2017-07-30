import math

# BOVERF error function
#   integral of standard normal curve
def BOVERF(X):
    # constants
    p = 0.3275911;
    a1 =  0.254829592;
    a2 = -0.284496736;
    a3 =  1.421413741;
    a4 = -1.453152027;
    a5 = 1.061405429;

    x1 = X/math.sqrt(2);
    t = 1/(1+p*x1);
    errf = 1.0 - (a1*t + a2*(t**2) + a3*(t**3) + a4*(t**4)\
        + a5*(t**5)) * math.exp(-(x1)*(x1));

    return 0.5 + (errf * 0.5);