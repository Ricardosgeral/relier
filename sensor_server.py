#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

"""Server that reads values from differents sensors for lab test.

This script is a server that is supposed to run on a RPi with the
adequate sensors hooked to it via GPIO.
It reads the value of the sensors then store them on disk or on
the usb drive if one is plugged, it also always export local data on
the usb drive if there are local data.
The measurements are stored in csv format in "/srv/sensors/" or directly at the root of the usb.

The sensors are:
    BME280 GY-BME280 : ambient temperature humidity and barometric pressure
    DS18B20 : water temperature: Direct waterproof DS18B20 digital temperature sensor (probe)
    Turbidity Sensor (dishwasher) : turbidity of water
                                    DFRobot Gravity Analog/Digital Turbidity Sensor, 5V 40mA DC
    3 pressure sensors : 0-5psi 5V Pressure Transducer Transmitter Sensor or Sender
    flow sensor : flowrate and total liters
                 1.5" DN40 2~200L/min water Plastic Hall Turbine flow sensor industry meter

It also records the time and date of the measure.

"""

# Libraries required
from time import sleep
from analogsensor_thread import AnalogSensor
from DigitalSen_thread import WTemp
from datetime import datetime
import pigpio   # needs to be installed for callback https://www.raspberrypi.org/forums/viewtopic.php?t=66445
import bme280   # temperature/humidity/pressure sensor BME280 # github.com/rm-hull/bme280: $ sudo pip install RPi.bme280
import smbus2   # required for bme280
import Adafruit_ADS1x15  # Analogic digital conversor ADS 15 bit 2^15-1=32767 (needs to be installed using pip3)
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)  # address of ADC See in -- sudo i2cdetect -y 1

# Constants
PATH_TO_MEDIA = '/media'

#Channel numbers in ads1115 analog to digital converter DAC
PRESSUP_ch = 0     # piezometric pressure in upstream chamber
PRESSINT_ch = 1    # piezometric pressure in interface
PRESSDW_ch = 2     # piezometric pressure in downstream chamber
TURB_ch = 3        # turbidity of outlet water (or downstream chamber)

#For the flowmeter
FLOW_ch = 27       #GPIO27 in raspberry pi3
pi = pigpio.pi()        # connect to Pi
if not pi.connected:
   exit()
pi.set_mode(FLOW_ch, pigpio.INPUT)
pi.set_pull_up_down(FLOW_ch, pigpio.PUD_UP)
callback = pi.callback(FLOW_ch) # default tally (contagem) callback

# for the temp+humidity+barometric pressure (BME280)
address = 0x76
port = 1
bus = smbus2.SMBus(port) # needed for bme280
#bme280.load_calibration_params(bus, address)  # ?Don't understand this!

# Global variables
analog_sensor = None
wtemp_sensor = None
global zerou, zeroi, zerod  # to zero the piezometric pressures (datum)
tempTread_flag = False
analogTread_flag = False

def init(interval, no_reads):
    global analog_sensor
    global wtemp_sensor
    global pulses

    pulses = 0      #starts the counting of pulses of the flowmeter
    sleep = interval / no_reads

    #create the threads ('parallel' calculations for analog sensors and temp sensors)
    global tempTread_flag
    if tempTread_flag == False:  # avoids having multiple threats wtemp_sensor running
        wtemp_sensor = WTemp(interval - 0.1)  # the sensor takes +-0.750s to read. so it's placed in a thread)
        wtemp_sensor.name = "temp_sensors"  #give a name to thread for better debugging
        wtemp_sensor.start()
        tempTread_flag = True

    global analogTread_flag
    if analogTread_flag == False:  # avoids having multiple threats analog_sensor running
        analog_sensor = AnalogSensor(sleep)  # average readings in the analog sensors per measure interval for signal stability)
        analog_sensor.name = "analog_sensors"
        analog_sensor.start()
        analogTread_flag = True

def zero_press(mu, mi, md, bu, bi, bd, testtype):
    # Transform the analog numbers in volts  # 15 bit value
    volts  = [0]*3
    zerou  = zeroi = zerod = 0 # values to zero pressure sensors - datum
    analog = [0]*3
    for ch in range(3):
        analog[ch] = adc.read_adc(ch, gain=1, data_rate=860)  # check if it's equal to Analogsensor.py
        # transformar o valor lido pelo adc em volts
        # Ratio of 15 bit value to max volts determines volts
        volts[ch] = analog[ch] / 32767.0 * 2.048
        #determine the value to add in order to zero pressures
        zerou = (mu * volts[PRESSUP_ch] + bu)
        if testtype == '3':  # if the test is a HET
            zeroi = 0
        else:
            zeroi = (mi * volts[PRESSINT_ch]+ bi)
        zerod = (md * volts[PRESSDW_ch] + bd)
    sleep(1)
    return zerou, zeroi, zerod

def get_data(interval, mu, mi, md, bu, bi, bd, mturb, bturb, zerou, zeroi, zerod, testtype): #
    """Get the data from the sensors, also get the date and time.

    Data recorded:
        time (str): the time of the record in HH:MM:SS format.
        date (str): the date of the record in DD-MM-YYYY format.
        mmH2O_up (float): pressure in the upstream piezometer in mmH2O
        mmH2O_int (float): pressure in the piezometer at the interface (middle) in mmH2O
        mmH2O_dwn (float): pressure in the downstream piezometer in mmH2O
        flowrate (float): instantaneous flowrate in L/min
        total_liters (float): Volume of fluid since start of program in Liters
        turb (int): the analog value of the turbidity (from 0 to 32768).
        water_temp (float): the temperature of the water in Celsius.
        air_temp (float): the ambient temperature in Celsius.
        air_pressure (float): the barometric pressure in Pascal.
        air_humidity (float): the ambient humidity in %

    Returns:
        dict: The data in the order of the fieldnames.

    """
    global analog_sensor
    global wtemp_sensor
    global pulses

    # Date (DD-MM-YYY) and time (HH:MM:SS)
    d = datetime.now()
    time_ = '{:%H:%M:%S}'.format(d)
    date_ = '{:%Y-%m-%d}'.format(d)

    # (DS18B) Water temperature
    try:
        water_temp = wtemp_sensor.read_temp()
        if water_temp == 0: # due to the reading time of the sensor the first reading may not be possible
            water_temp = 0
    except:
        water_temp = 0

    #flowmeter
    pulses_last = pulses
    pulses = callback.tally()
    total_liters = (pulses) / 27  # 1L water = 27 pulse (device specs)
    flowrate = (pulses - pulses_last) / interval / 0.45  # F (Hz) = 0.45 Q  with Q = L/min  (device specs)

    # Transform the analog numbers in volts
    volts = [0] * 3
    bar   = [0] * 3
    mmH2O = [0] * 3
    bar_to_mmH2O = 10197.162129779283
    analog = analog_sensor.read_analog()  # get the actual reading from average

    for ch in range(0,3,1):
        # Ratio of 15 bit value to max volts determines volts
        volts[ch] = analog[ch] / 32767.0 * 2.048

    # linear relationship between psi & voltage in the pressure sensors(from manufacturer)
    bar[PRESSUP_ch]  = (mu * volts[PRESSUP_ch]  + bu) - zerou # 0 psi(bar) = 0.5v ; 15psi(*psi_to_bar) = 4.5V
    bar[PRESSINT_ch] = (mi * volts[PRESSINT_ch] + bi) - zeroi # 0 psi(bar) = 0.5v ;  5psi(*psi_to_bar) = 4.5V
    bar[PRESSDW_ch]  = (md * volts[PRESSDW_ch]  + bd) - zerod # 0 psi(bar) = 0.5v ;  5psi(*psi_to_bar) = 4.5V

    for ch in range(3):
        mmH2O[ch] = bar[ch] * bar_to_mmH2O   # mmH2O conversion

    if testtype == '3':
        volts[PRESSINT_ch]= 0
        bar[PRESSINT_ch]= 0
        mmH2O[PRESSINT_ch]= 0

    turb = analog[TURB_ch]
    ntu_turb = mturb*turb + bturb

    # (BME280) Air temperature + pressure + humidity
    try:
        b = bme280.sample(bus, address)
        air_temp     = str(b.temperature)
        air_pressure = str(b.pressure)
        air_humidity = str(b.humidity)
    except:
        air_temp = 0
        air_pressure = 0
        air_humidity = 0

    return {
        'date':         date_,
        'time':         time_,
        'v_up':         volts[PRESSUP_ch],  #V
        'v_int':        volts[PRESSINT_ch], #V
        'v_down':       volts[PRESSDW_ch],  #V
        'bar_up':       bar[PRESSUP_ch],    #bar
        'bar_int':      bar[PRESSINT_ch],   #bar
        'bar_down':     bar[PRESSDW_ch],    #bar
        'mmH2O_up':     round(mmH2O[PRESSUP_ch]),
        'mmH2O_int':    round(mmH2O[PRESSINT_ch]),
        'mmH2O_down':   round(mmH2O[PRESSDW_ch]),
        'ana_turb':     round(analog[TURB_ch]), #analog number
        'ntu_turb':     round(ntu_turb),
        'flow':         round(flowrate,2),
        'liters':       round(total_liters),
        'water_temp':   round(water_temp,1),
        'air_temp':     air_temp,
        'air_pressure': air_pressure,
        'air_humidity': air_humidity
    }

#
#     callback.cancel()  # cancel callback
#     pi.stop() # disconnect from Pi
#
#     print("\nexiting")
#     end(RUN_TIME)
#     os._exit(0)