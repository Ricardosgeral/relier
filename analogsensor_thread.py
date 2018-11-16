#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import threading
import time
import Adafruit_ADS1x15 # Analogic digital conversor ADS 15 bit 2^15-1=32767 (needs to be installed using pip3)
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1) #address of ADC See in -- sudo i2cdetect -y 1

# Choose a gain of 1 for reading voltages from 0 to 6.14V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V

# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1  #2/3, 1, 2, 4 , 6 , 8, 16
DATA_RATE = 250  # 8, 16, 32, 64, 128, 250, 475, 860 samples/second   max =860 the higher the number the higher the noise!

class AnalogSensor(threading.Thread):


    def __init__(self, sleep):
          threading.Thread.__init__(self)
          #self.pin_num = pin_num
          self.sleep = sleep
          self.count = 0
          self.total = [0]*4

    def run(self):
        while True:
            # Adds measures and keep track of num of measurements
            for channel in range(4):
                self.total[channel] += adc.read_adc(channel, gain=GAIN,data_rate=DATA_RATE) # pin gain and data_rate
            self.count += 1
            time.sleep(self.sleep)

    def read_analog(self):
        """reads the channels as a rounded mean"""
        # Compute the mean
        analog=[0]*4
        for channel in range(4):
            if self.count != 0:
                analog[channel] = self.total[channel] / self.count
            else:
                analog[channel]=0
        # Reset the counter and measurements
        self.total = [0]*4
        self.count = 0

        return analog
