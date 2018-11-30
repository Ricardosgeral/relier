import serial
import re
from time import sleep
import time

def read_flowMAG(v1,v2):
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

    volume = 0.0
    sleep(.2)
    first_time = time.time()

    while 1:
        if ser == None:
            try:
                ser = serial.Serial(port='/dev/ttyACM0',
                                    baudrate=9600,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=1.09)
            except:
                pass
        else:
            flow = ser.readline().decode()
            last_time = time.time()
            intv = last_time - first_time
            first_time = last_time

            flow = re.split(r'\t+', flow.rstrip('\t'))
            flow = flow[1].replace(',', '.')
            flow = float(flow)  # in liters per hour
            volume =volume + flow/(60*60*intv)  # in liters in each second (defined by time sleep)
            v1.value=flow
            v2.value=volume
        sleep(1)
