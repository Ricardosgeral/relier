#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file runs in a different process using multiprocessing library in sensor_server.py
ricardos.geral@gmail.com
"""

import serial
import re
from time import sleep
import time

def read_flowMAG(v1,v2):
    volume = 0.0  #initialize the total volume of water

    try:
          ser = serial.Serial(port='/dev/ttyACM0',
                          baudrate=9600,
                          parity=serial.PARITY_NONE,
                          stopbits=serial.STOPBITS_ONE,
                          bytesize=serial.EIGHTBITS,
                          timeout=1.09)
    except:
        ser = None
        print("MAG-flow not connected no USB! could not open port /dev/ttyACM0")

    sleep(.2)                   # for stability
    first_time = time.time()    # acquire time to calculate total volume


    while 1:
        if ser == None:  # if serial did not acquired initially then try again
            try:
                ser = serial.Serial(port='/dev/ttyACM0',
                                    baudrate=9600,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=1.09)    #data from flowMAG is streaming at a rate of 1s. so 9% more for safety
            except:
                pass
        else:
            flow = ser.readline().decode()  #gets flow rate in liters/hour
            last_time = time.time()         # to calculate the volume between readings
            intv = last_time - first_time
            first_time = last_time

            flow = re.split(r'\t+', flow.rstrip('\t'))
            flow = flow[1].replace(',', '.')
            flow = float(flow)  # in liters per min
            volume =volume + flow/(60*60*intv)  # in liters in each second (defined by last time sleep)
            v1.value=flow   #to pass variable using shared memory
            v2.value=volume #to pass variable using shared memory
        sleep(1)
