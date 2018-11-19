#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import threading
import time
from statistics import mean
from ringbuffer import RingBuffer #This version uses a circular buffer to avoid unwanted zero readings
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


    def __init__(self, sleep, records):
          threading.Thread.__init__(self)
          self.sleep = sleep
          self.records = records

    def run(self):

        self.A0 = RingBuffer(self.records)  # creates a buffer with maximum numbers equal to the number of records /reading
        self.A1 = RingBuffer(self.records)
        self.A2 = RingBuffer(self.records)
        self.A3 = RingBuffer(self.records)

        while True:
            # Adds measures and keep track of num of measurements
            self.A0.append(adc.read_adc(0, gain=GAIN,data_rate=DATA_RATE)) # pin gain and data_rate
            self.A1.append(adc.read_adc(1, gain=GAIN, data_rate=DATA_RATE))  # pin gain and data_rate
            self.A2.append(adc.read_adc(2, gain=GAIN, data_rate=DATA_RATE))  # pin gain and data_rate
            self.A3.append(adc.read_adc(3, gain=GAIN, data_rate=DATA_RATE))  # pin gain and data_rate

            time.sleep(self.sleep-0.01*4) #each reading takes about 0.01s. this time is compensated during sleep

    def read_analog(self):
        """reads the channels as a rounded mean"""
        # Compute the mean
        analog=[0]*4
        #for channel in range(4):
        analog[0] = mean(self.A0.get())
        analog[1] = mean(self.A1.get())
        analog[2] = mean(self.A2.get())
        analog[3] = mean(self.A3.get())
        return analog
