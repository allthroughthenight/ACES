import sys
import math
sys.path.append('../functions')

from base_driver import BaseDriver
from helper_objects import BaseField
import USER_INPUT

class beach_nourishment():

    metric = input('Metric or Imperial (m or s):')

    if metric == 'm':
        metric = True
    else:
        metric = False

    if metric:
        labelUnitVolumeRate = 'm^3'
        labelUnitGrain = 'mm';
    else:
        labelUnitVolumeRate = 'yd^3'
        labelUnitGrain = 'phi'

    Vol_i = input('Enter Vol_i: Initial volume ('+ labelUnitVolumeRate+ '): ')
    M_R = input('Enter M_R: Initial volume (' + labelUnitGrain + '): ')
    ro_n = input('Enter ro_n: Native standart deviation (phi): ')
    M_b = input('Enter M_b: Borrow mean (' + labelUnitGrain + '): ')
    ro_b = input('Enter ro_b: Borrow standard deviation (phi): ')
    Vol_i = 800000
    M_R = 1.8
    ro_n = 0.45
    M_b = 2.25
    ro_b = 0.76

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
            #catg == 1
        else:
            print('Borrow material is coarser than native material')
            #catg == 2
    else:
        if M_b < M_R:
           print('Borrow material is coarser than native material')
           #catg==3
        else:
           print('Borrow material is finer than native material')
           #catg==4

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
       fn3 = ((1.0-ft1)/sigma)*math.exp(0.5*(phi_1**2-bk1**2));
       R_a = 1.0/(fn1+fn3);
    else:
        bk2 = (phi_2-delta)/sigma;
        fn2 = boverf(bk2);
        ft2 = boverf(phi_2);
        fn3 = ((ft2-ft1)/sigma)*math.exp(0.5*(phi_1**2-bk1**2));
        r_A  = 1.0/(1-fn2+fn1+fn3);

    if R_A >= 1.0:
        print('Error: Overfill ratio (R_A) < 1.0 Respecify data')

    # F = integral of standard normal curve
    #R_A = 1 / (1-(normcdf((phi_2-phi_m_diff) / ro)+ ...
    # normcdf((phi_1-phi_m_diff) / rho)+((normcdf(phi_2)-normcdf(phi_1)) / ro) * exp(0.5 * (phi_1**2-((phi_1-phi_m_diff) / ro)**2))))

    winno = 1
    R_j = math.exp(winno * ((M_b-M_R) / ro_n) - (winno**2 / 2) * ((ro_b**2 / ro_n**2) - 1))

    Vol_D = R_A  *  Vol_i

    return R_A, R_j, Vol_D

beach_nourishment()
