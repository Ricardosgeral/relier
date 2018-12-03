#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

"""Server that reads values from different sensors for lab test.

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
    flow sensor : flowrate and total liters. It is possible to choose between two different types of flowmeters:
                1- Eletro-magnetic flowmeter (Danfoss Mag) - connected via serial port
                2- 1.25" DN32 1~120L/min water Plastic Hall Turbine flow sensor industry meter (Sea brand)

It also records the time and date of the measure.

"""

# Libraries required
from time import sleep
from analogsensor_thread_buf import AnalogSensor, GAIN, DATA_RATE
from digitalSen_thread import D_Temp
import FlowMAG  # for the eletromagnetic flow meter from Danfoss
import multiprocessing  # the reading of FLOWMAG is placed in a different process
from datetime import datetime
from math import log as log
import pigpio   # needs to be installed for callback https://www.raspberrypi.org/forums/viewtopic.php?t=66445
import Adafruit_ADS1x15  # Analogic digital conversor ADS 15 bit 2^15-1=32767 (needs to be installed using pip3)
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)  # address of ADC See in -- sudo i2cdetect -y 1

# Constants
PATH_TO_MEDIA = '/media'

#Channel numbers in ads1115 analog to digital converter DAC
PRESSUP_ch = 0     # piezometric pressure in upstream chamber
PRESSINT_ch = 1    # piezometric pressure in interface
PRESSDW_ch = 2     # piezometric pressure in downstream chamber
TURB_ch = 3        # turbidity of outlet water (or downstream chamber)

# Relation Gain voltages :
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V

if GAIN == 1:
    max_VOLT = 4.096
elif GAIN == 2:
    max_VOLT = 2.048
elif GAIN == 4:
    max_VOLT = 1.024
elif GAIN == 4:
    max_VOLT = 0.512
elif GAIN == 4:
    max_VOLT = 0.256
else: # GAIN == 2/3
    max_VOLT = 6.144

#For the flowmeter
FLOW_ch = 25       #GPIO25 in raspberry pi3
pi = pigpio.pi()        # connect to Pi
if not pi.connected:
   exit()
pi.set_mode(FLOW_ch, pigpio.INPUT)
pi.set_pull_up_down(FLOW_ch, pigpio.PUD_UP)
callback = pi.callback(FLOW_ch) # default tally (contagem) callback


# Global variables
analog_sensor = None
d_temp_sensor = None
global zerou, zeroi, zerod  # to zero the piezometric pressures (datum)
tempTread_flag = False
analogTread_flag = False

def init(interval, no_reads, flowmeter):
    global analog_sensor
    global d_temp_sensor
    global pulses, flowrate
    global v1,v2,p

    pulses   = 0      #starts the counting of pulses of the turbine flowmeter
    flowrate = 0      #starts the counting of the flowrate of the eletromagnetic flowmeter

    sleep = interval / no_reads

    #create the threads ('parallel' calculations for analog sensors and temp sensors)
    global tempTread_flag
    if tempTread_flag == False:  # avoids having multiple threats d_temp_sensor running
        d_temp_sensor = D_Temp(interval - 0.1)  # the sensor takes +-0.750s to read. so it's placed in a thread)
        d_temp_sensor.name = "dig temp sensors"  #give a name to thread for better debugging
        d_temp_sensor.start()
        tempTread_flag = True

    global analogTread_flag
    if analogTread_flag == False:  # avoids having multiple threats analog_sensor running
        analog_sensor = AnalogSensor(sleep,no_reads)  # average readings in the analog sensors per measure interval for signal stability)
        analog_sensor.name = "analog_sensors"
        analog_sensor.start()
        analogTread_flag = True

    if flowmeter == "1": # 1= eletroMagnetic flowmeter; 2 = turbine flowmeter
        # create a process only to read the eletromagnetic flowmeter
        # first see if any process to read the eletromag flowmeter is running and terminates it.
        try:
            p.terminate()
        except:
            None

        v1 = multiprocessing.Value('d', 0.0)  # flow rate -> value for shared memory between parent(main)
        v2 = multiprocessing.Value('d', 0.0)  # total volume -> value for shared memory
        p = multiprocessing.Process(target=FlowMAG.read_flowMAG, args=(v1,v2,))
        p.start()


def zero_press(mu, mi, md, bu, bi, bd, testtype):
    # Transform the analog numbers in volts  # 15 bit value
    volts  = [0]*3
    zerou  = zeroi = zerod = 0 # values to zero pressure sensors - datum
    analog = [0]*3
    for ch in range(3):
        analog[ch] = adc.read_adc(ch, gain=GAIN, data_rate=DATA_RATE)
        # transformar o valor lido pelo adc em volts
        # Ratio of 15 bit value to max volts determines volts
        volts[ch] = analog[ch] / 32767.0 * max_VOLT
        #determine the value to add in order to zero pressures
        zerou = (mu * volts[PRESSUP_ch] + bu)
        if testtype == '3':  # if the test is a HET
            zeroi = 0
        else:
            zeroi = (mi * volts[PRESSINT_ch]+ bi)
        zerod = (md * volts[PRESSDW_ch] + bd)
    sleep(1)
    return zerou, zeroi, zerod

def get_data(interval, mu, mi, md, bu, bi, bd, mturb, bturb, zerou, zeroi, zerod, testtype, flowmeter, cf): #
    """Get the data from the sensors, also get the date and time.

    Data recorded:
        time (str): the time of the record in HH:MM:SS format.
        date (str): the date of the record in DD-MM-YYYY format.
        mmH2O_up (float): pressure in the upstream piezometer in mmH2O
        mmH2O_int (float): pressure in the piezometer at the interface (middle) in mmH2O
        mmH2O_dwn (float): pressure in the downstream piezometer in mmH2O
        flowrate (float): instantaneous flowrate in L/hour
        total_liters (float): Volume of fluid since start of program in Liters
        turb (int): the analog value of the turbidity (from 0 to 32768).
        water_temp (float): the temperature of the water in Celsius.
        air_temp (float): the ambient temperature in Celsius.
        air_hum (float): the ambient humidity in %
        air_pres (float): the barometric pressure in Pascal.

    Returns:
        dict: The data in the order of the fieldnames.

    """
    global analog_sensor
    global d_temp_sensor
    global pulses, flowrate
    global v1,v2,p

    # Date (DD-MM-YYY) and time (HH:MM:SS)
    d = datetime.now()
    time_ = '{:%H:%M:%S}'.format(d)
    date_ = '{:%Y-%m-%d}'.format(d)

    # (DS18B) Water temperature + BME280

    water_temp, air_temp, air_hum, air_pres = d_temp_sensor.read_d_temp()

#FLOWMETERS
    if flowmeter == "1": # eletromagnetic flowmeter was selected
        #flowmeter: MAGFLOW (eletromagnetic flowmeter). values from the multiprocessing
        flowrate = v1.value  # in liters per hour
        total_liters = v2.value  # in liters

    else:  # if a int number equal or higher than 2 is selected consider the turbine flowmeter!
        #flowmeter: turbine
        if cf == "": cf="0.45" # in case the cf variable is not set in ini file
        pulses_last = pulses
        pulses = callback.tally()
        total_liters = round((pulses) / (float(cf)*60),2)  # 1L water = 0.45 x 60 = 27 pulses (device specs)
        flowrate = ((pulses - pulses_last) / interval / float(cf))*60  # f (Hz) = cf x Q , with Q = L/min  (cf = 0.45 device specs)


    # Transform the analog numbers in volts
    volts = [0] * 3
    bar   = [0] * 3
    mmH2O = [0] * 3
    bar_to_mmH2O = 10197.162129779283
    analog = analog_sensor.read_analog()  # get the actual reading from average

    for ch in range(0,3,1):
        if analog[ch] != 32767:  # The pcb has a pull-up resister that is used to check if there is no sensor attached.
        # Ratio of 15 bit value to max volts determines volts
            volts[ch] = analog[ch] / 32767 * max_VOLT
        else:
            volts[ch] = 0  # only pull-up resistor is present

    # linear relationship between psi & voltage in the pressure sensors(from manufacturer)
    if volts[PRESSUP_ch] != 0:
        bar[PRESSUP_ch] = (mu * volts[PRESSUP_ch]  + bu) - zerou # 0 psi(bar) = 0.5v ; 15psi(*psi_to_bar) = 4.5V
    else:
        bar[PRESSUP_ch] = 0
    if volts[PRESSINT_ch] != 0:
        bar[PRESSINT_ch] = (mi * volts[PRESSINT_ch] + bi) - zeroi  # 0 psi(bar) = 0.5v ;  5psi(*psi_to_bar) = 4.5V
    else:
        bar[PRESSINT_ch] = 0
    if volts[PRESSDW_ch] != 0:
        bar[PRESSDW_ch] = (md * volts[PRESSDW_ch]  + bd) - zerod # 0 psi(bar) = 0.5v ;  5psi(*psi_to_bar) = 4.5V
    else:
        bar[PRESSDW_ch] = 0

    for ch in range(3):
        if volts[ch] != 0:
            mmH2O[ch] = bar[ch] * bar_to_mmH2O   # mmH2O conversion
        else:
            mmH2O[ch]=0
    if testtype == '3':             #HET
        volts[PRESSINT_ch]= 0
        bar[PRESSINT_ch]= 0
        mmH2O[PRESSINT_ch]= 0

    turb_analog = analog[TURB_ch]           # analog 0 to 32767

    if turb_analog != 32767:  # value given by pull-up resistor -> nothing connected
        turb = mturb*log(turb_analog) + bturb   # grams/liter  y=m.ln(x) + b     base e
    else:
        turb = 0

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
        'turb':         round(turb,2),
        'flow':         round(flowrate,2),
        'liters':       round(total_liters,2),
        'water_temp':   round(water_temp,1),
        'air_temp':     round(air_temp,1),
        'air_hum':      round(air_hum,1),
        'air_pres':     round(air_pres),

    }

#for testing
#init(5,1)
#get_data(5,.4,.4,.4,.4,.4,.4,.4,.4,0.01,0.01,0.01,1) #( dummy values )

#
#     callback.cancel()  # cancel callback
#     pi.stop() # disconnect from Pi
#
#     print("\nexiting")
#     end(RUN_TIME)
#     os._exit(0)