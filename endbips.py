#import os
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
buzzpin=12 # (GPIO18)
GPIO.setup(buzzpin,GPIO.OUT)
loop = 2 # number of morse code loops

def morsecode_bips ():
    #Dot Dot Dot
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.1)
    #Dash Dash Dash
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.2)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.2)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.2)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.2)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.2)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.2)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.2)
    #Dot Dot Dot
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.HIGH)
    sleep(.1)
    GPIO.output(buzzpin,GPIO.LOW)
    sleep(.7)

def test_end():
    for i in range(0,loop):
        morsecode_bips ()

#os.system('clear')
test_end()