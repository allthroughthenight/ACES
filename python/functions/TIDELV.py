import math

def TIDELV(ng,t,ampl,alpha,fndcst,acst):

    deg2rad=pi/180
    tidelv=0
    for nc in men(ampl):
        arg=(acst(nc)*t+alpha(nc,ng))*deg2rad
        tidelv=tidelv+fndcst(nc)*ampl(nc,ng)*cos(arg)
    return tidelv
