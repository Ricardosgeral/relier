#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com
'''
This code is helpful in the analog sensors calibration
to determine the line constants m and b

for Pressures: (x,y) = (Volts, pressure_psi)
for Turbidity: (x,y) = (analog_number, NTU)

analog numbers are from 0 to 32767
'''

from numpy import ones, vstack
from numpy.linalg import lstsq

psi_to_bar = 0.0689476

def line2(x1,y1,x2,y2):  #x = volts ; y = psi 32767
    points_pu = [(x1, y1), (x2, y2)]
    x_coords_pu, y_coords_pi = zip(*points_pu)
    A = vstack([x_coords_pu, ones(len(x_coords_pu))]).T
    m, c = lstsq(A, y_coords_pi)[0] * psi_to_bar
    #print("Line Solution is y = {m}x + {c}".format(m=m, c=c))
    return round(m,4), round(c,4)

pu= line2(0.510015,0,  4.0216,4.35113)
print(pu)
pi= line2(0.495,0,  4.5,5)
print(pi)
pd= line2(0.493,0,  4.5,5)
print(pd)
turb= line2(30000,100,  3000,2000)  #analog, #NTU
print(turb)
