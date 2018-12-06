import serial
import time
import re
from time import sleep

ser = serial.Serial(port='/dev/ttyACM0',
                                    baudrate=2400,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=1)    #data from flowMAG is streaming at a rate of 1s. so 9% more for safety

ser.reset_output_buffer()

EndCom = "\xff\xff\xff"

while True:
#ser.write(EndCom.encode('latin-1'))
    flow = ser.readline().decode()  #gets flow rate in liters/hour

    flow = re.split(r'\t+', flow.rstrip('\t'))
    flow = flow[1].replace(',', '.')
    flow = float(flow)  # in liters per min


    print(flow)
    sleep(1)