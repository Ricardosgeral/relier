import RPi.GPIO as GPIO
import time
from time import sleep

LedPin = 21  # pin18 GPIO24

def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)  # Set LedPin's mode is output
    GPIO.output(LedPin, GPIO.HIGH)  # Set LedPin high(+3.3V) to turn on led

def blink(x):

    GPIO.output(LedPin, GPIO.HIGH)  # led on
    time.sleep(x)
    GPIO.output(LedPin, GPIO.LOW)  # led off
    time.sleep(x)

def destroy():
    GPIO.output(LedPin, GPIO.LOW)  # led off
    GPIO.cleanup()  # Release resource

def fast_5blinks():
    setup()
    for i in range(5):
        blink(0.05)
    destroy()

def shutdown_led():
    setup()
    for i in range(7):
        blink(0.05)

    blink(2)
    destroy()

def reboot_led():
    setup()
    for i in range(3):
        blink(0.5)
    destroy()


#if __name__ == '__main__':  # Program start from here
#setup()
#     try:
#shutdown_led()
#sleep(2)
#reboot_led()

#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#destroy()