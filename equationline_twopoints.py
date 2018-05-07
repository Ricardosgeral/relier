from numpy import ones, vstack
from numpy.linalg import lstsq

psi_to_bar = 0.0689476

def line2(x1,y1,x2,y2):  #x = volts ; y = psi
    points_pu = [(x1, y1), (x2, y2)]
    x_coords_pu, y_coords_pi = zip(*points_pu)
    A = vstack([x_coords_pu, ones(len(x_coords_pu))]).T
    m, c = lstsq(A, y_coords_pi)[0] * psi_to_bar
    #print("Line Solution is y = {m}x + {c}".format(m=m, c=c))
    return round(m,4), round(c,4)

pu= line2(0.501,0,  4.5,5)
print(pu)
pi= line2(0.5,0,  4.5,5)
print(pi)
pd= line2(0.538,0,  4.5,15)
print(pd)
turb= line2(32767,100,  800,20000)  #analog, #NTU
print(turb)
