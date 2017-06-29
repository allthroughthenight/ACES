import math

# Initialize gage-specific information relevant to harmonic constituents

#   INPUT
#   ngag: number of gages to be intialized (1)
#   yr: year at beginning of record
#   month: month at beginning of record
#   day: day at beginnning of record
#   hr: hr at beginning of record
#   tlhrs: length of the record in hours
#   glong: array of longitudes of gage records
#   epoch: array of epochs for constituents
#   acst: orbital speeds of constituents [deg/hr]
#   pcst: number of tide cycles per day per constiuent

#   OUTPUT
#   alpha: array of alphas for constituents
#   fndcst: node factors at middle of record

def GAGINI(ngag,yr,month,day,hr,tlhrs,glong,epoch,acst,pcst):

    # determine Julian day at beginning of record
    dayj=DAYOYR(yr,month,day)

    # determine time (in hours) at middle of record
    hrmid=hr+(tlhrs/2)

    #determine node factors at middle of record
    fndcst=NFACS(yr,dayj,hrmid);

    #determine greenwich equilibrium terms at beginnong of record
    eqcst=GTERMS(yr,dayj,hr,dayj,hrmid);

    #determine alpha values
    for x in ngag:
        y=floor(glong(x)/15);
        s=15*y;

        if (glong(x) % 15)>7.5:
            s=s+15

        for y in length(eqcst):
            sum=eqcst(y)+acst(y)*(s/15)
            alpha(y,ngag)=sum-pcst(y)*glong(ngag)-epoch(y,ngag)

    return alpha,fndcst
