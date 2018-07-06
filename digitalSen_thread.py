import threading
import time
#water temperature
from w1thermsensor import W1ThermSensor

#BME280
import smbus2
import bme280
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

class D_Temp(threading.Thread): # digital temperature sensors (water temp and bme280 (temp+hum+press))

    def __init__(self, sleep):
        threading.Thread.__init__(self)
        self.sleep = sleep
        self.W_temp = 0
        self.temp=0
        self.hum=0
        self.pres=0

    def run(self):
        while True:
            # reads every sleep interval >0.8 (sensor response minimum delay)
            try:
                self.W_temp = W1ThermSensor().get_temperature()
            except:
                self.W_temp = 0
            time.sleep(self.sleep)

            try:
                data = bme280.sample(bus, address, calibration_params)

                self.temp = data.temperature
                self.hum = data.humidity
                self.press = data.pressure
            except:
                self.temp = 0
                self.hum = 0
                self.pres = 0

    def read_d_temp(self): # read digital temperature sensors
        water_temp = self.W_temp
        air_temp= self.temp
        air_hum= self.hum
        air_pres=self.press
        return water_temp, air_temp, air_hum, air_pres