import threading
import time
from w1thermsensor import W1ThermSensor

class WTemp(threading.Thread):

    def __init__(self, sleep):
        threading.Thread.__init__(self)
        self.sleep = sleep
        self.W_temp = 0

    def run(self):
        while True:
            # reads every sleep interval >0.8 (sensor response minimum delay)
            try:
                self.W_temp = W1ThermSensor().get_temperature()
            except:
                self.W_temp = 0
            time.sleep(self.sleep)

    def read_temp(self):
        water_temp = self.W_temp
        return water_temp