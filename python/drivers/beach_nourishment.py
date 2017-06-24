from helper_functions import *
import math
import sys

## ACES Update to MATLAB BEACH NOURISMENT and OVERFILL RATIO
#-------------------------------------------------------------
# Evaluates the suitable of borrow material as beach fill and give overfill
# nourishment ratios. (Aces Tech Manual Chapter 6-4-1)

# Updated by: Yaprak Onat
# Date Created: June 21, 2016
# Date Modified:

# Requires the following functions:


# MAIN VARIABLE LIST:
#   INPUT
#  Vol_i = initial volume (yd**3 or m**3) Range 1 to 10**8
#   M_R = Native mean (phi, mm) Range -5 to 5
#   ro_n = native standard deviation (phi) Range 0.01 to 5
#   M_b = borrow mean (phi, mm) Range -5 to 5
#   ro_b = borrow standard deviation (phi) Range 0.01 to 5
#
#   OUTPUT
#   R_A = Overfill Ratio
#   Rj = Renourishment factor
#   Vol_D = Design Volume (yd**3 or m**3)

#   OTHERS
#   g: gravity [32.17 ft / s**2]
#   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs / ft**3]
#   rhos: density of sediment [5.14 slugs / ft**3 in FORTRAN source code]
#-------------------------------------------------------------

def beach_nourishment():

    metric = True
    metric = input('Input in imperial or SI units? (m or s): ')

    if metric == 'm':
        metric = True
        g = 9.81
    elif metric == 'M':
        metric = True
        g = 9.81
    else:
        g = 32.17
        metric = False

    rhos = 165.508 / g #bulk density of quartz is 165.508 lb/ft^3 - 165.508/g = 5.14

    salt_water = True
    salt_water = input('Fresh or Salt water? (F or S): ')

    if salt_water == 's':
        salt_water = True
    elif salt_water == 'S':
        salt_water = True
    else:
        salt_water = False

    if metric:
        labelUnitVolumeRate = 'm^3'
        labelUnitGrain = 'mm';
        if salt_water:
            rho = 1.989
        else:
            rho = 1.94

    if metric:
        labelUnitVolumeRate = 'm^3'
        labelUnitGrain = 'mm';
    else:
        labelUnitVolumeRate = 'yd^3'
        labelUnitGrain = 'phi'

    if salt_water:
        rho = 1.989
    else:
        rho = 1.94

    Vol_i = input('Enter Vol_i: Initial volume ('+ labelUnitVolumeRate+ '): ')
    M_R = input('Enter M_R: Initial volume (' + labelUnitGrain + '): ')
    ro_n = input('Enter ro_n: Native standart deviation (phi): ')
    M_b = input('Enter M_b: Borrow mean (' + labelUnitGrain + '): ')
    ro_b = input('Enter ro_b: Borrow standard deviation (phi): ')
#    Vol_i = 800000
#    M_R = 1.8
#    ro_n = 0.45
#    M_b = 2.25
#    ro_b = 0.76

    ro_b = int(ro_b)
    ro_n = int(ro_n)
    M_b = float(M_b)
    M_R = float(M_R)

    catg = 0 # category of the material according to table 6-4-1 in Aces manual

    if metric:
        M_R = - ( math.log(M_R) / math.log(2.) )
        M_b = - ( math.log(M_b) / math.log(2.) )

    ro = ro_b / ro_n # phi sorting ratio
    phi_m_diff = (M_b - M_R) / ro_n # phi mean difference

    # Relationships of phi means and pho standard deviations
    if ro_b > ro_n:
        print('Borrow material is more poorly sorted than native material')
        if M_b > M_R:
            print('Borrow material is finer than native material')
            catg == 1
        else:
            print('Borrow material is coarser than native material')
            catg == 2
    else:
        if M_b < M_R:
           print('Borrow material is coarser than native material')
           catg==3
        else:
           print('Borrow material is finer than native material')
           catg==4

    delta = (M_b-M_R)/ro_n
    sigma = ro_b/ro_n

    # defining phi_1 and phi_2
    if catg == 1 or catg == 2:
        phi_1 = max(-1, (-phi_m_diff / (ro**2-1)))
        phi_2 = math.inf
    else:
        phi_1 = -1
        phi_2 = max(-1, (1+(2 * phi_m_diff / (1-ro**2))))

    bk1 = (phi_1-delta)/sigma
    fn1 = boverf(bk1)
    ft1 = boverf(phi_1)

    if phi_2 == math.inf:
       fn3 = ((1.0-ft1)/sigma)*math.exp(0.5*(phi_1**2-bk1**2))
       R_A = 1.0/(fn1+fn3)
    else:
        bk2 = (phi_2-delta)/sigma
        fn2 = boverf(bk2)
        ft2 = boverf(phi_2)
        fn3 = ((ft2-ft1)/sigma)*math.exp(0.5*(phi_1**2-bk1**2))
        R_A  = 1.0/(1-fn2+fn1+fn3)

    if R_A >= 1.0:
        print('Error: Overfill ratio (R_A) < 1.0 Respecify data')
        sys.exit(0)

    winno = 1
    R_j = math.exp(winno * ((M_b-M_R) / ro_n) - (winno**2 / 2) * ((ro_b**2 / ro_n**2) - 1))

    Vol_D = R_A  *  Vol_i

    print('Overfill Ratio, R_A \t\t %.2f' % R_A)
    print('Renourishment factor, R_j \t %.2f' % R_j)
    print('Design Volunm, Vol_D \t\t %.2f %s' % (Vol_D, labelUnitVolumeRate))

    return R_A, R_j, Vol_D

beach_nourishment()
