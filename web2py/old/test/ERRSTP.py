from numpy import pi, tanh

def ERRSTP(H,d,L):
    steep=H/L;
    k=(2*pi)/L;
    maxstp=0.142*tanh(k*d);
    return steep,maxstp


