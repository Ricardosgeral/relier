# get data from txt file with calibration

import numpy as np
from scipy import interpolate

calib_data = np.genfromtxt('Turb_calib.txt', dtype='float', skip_header= 1)  # get txt file (ignores 1st row)

x = calib_data[:, 0]
y = calib_data[:, 1]

turb_interpolate = interpolate.interp1d(x, y, kind= 'linear', bounds_error=False, fill_value= -1)

#for testing
#print(turb_interpolate(5000))

