## Copyright (C) 2001 David Billinghurst
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or   
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

## Compute:
##     complete elliptic integral of first K(m) 
##     complete elliptic integral of second E(m)    
##
## usage: [k,e] = ellipke(m[,tol])
## 
## m is either real array or scalar with 0 <= m <= 1
## 
## tol  Ignored. 
##      (Matlab uses this to allow faster, less accurate approximation)
##
## Ref: Abramowitz, Milton and Stegun, Irene A
##      Handbook of Mathematical Functions, Dover, 1965
##      Chapter 17
##
## See also: ellipj

## Author: David Billinghurst <David.Billinghurst@riotinto.com>
## Created: 31 January 2001
## 2001-02-01 Paul Kienzle
##   * vectorized
##   * included function name in error messages

def ellipke( m ):
    from numpy import zeros, nonzero, Inf, ones, pi, sqrt
    eps=2.2204e-16
    try:
        shp=m.shape
    except:
        m=zeros((1))+m
        shp=m.shape
    if (len(shp)<2):
        shp=shp + (1,)

    k = e = zeros(m.shape);
    m = m[:];
    if (len(m<0)>0 | len(m>1)>0):
        print("ellipke must have m in the range [0,1]");
    Nmax = 16;
    
    idx = nonzero(m == 1);
    if (len(idx)<1):
        k[idx] = Inf;
        e[idx] = 1.0;

    ## Arithmetic-Geometric Mean (AGM) algorithm
    ## ( Abramowitz and Stegun, Section 17.6 )

    idx = nonzero(m != 1);
    if (len(idx)>0):
        a = ones((len(idx),1));
        b = sqrt(1.0-m[idx]);
        c = sqrt(m[idx]);
        f = 0.5;
        sumf = f*c*c;
        for n in range(2,Nmax+1):
            t = (a+b)/2;
            c = (a-b)/2;
            b = sqrt(a*b);
            a = t;
            f = f * 2;
            sumf = sumf + f*c*c;
            if (len(c/a < eps)==len(c)):
                break
        if (n >= Nmax):
            print("ellipke: not enough workspace");
        k[idx] = 0.5*pi/a;
        e[idx] = 0.5*pi*(1.0-sumf)/a;


    return k,e


##test
if __name__=='__main__':
    
    import numpy
    from ellipke import ellipke
    m=numpy.array([0.2,0.1])
    k,e=ellipke(m)
