import RPi.GPIO as GPIO
import time

LedPin = 21  # pin18 GPIO24

def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)  # Set LedPin's mode is output
    GPIO.output(LedPin, GPIO.HIGH)  # Set LedPin high(+3.3V) to turn on led


def on():
    GPIO.output(LedPin, GPIO.HIGH)  # led on

def off():
    GPIO.output(LedPin, GPIO.LOW)  # led off


def blink(x):

    GPIO.output(LedPin, GPIO.HIGH)  # led on
    time.sleep(x)
    GPIO.output(LedPin, GPIO.LOW)  # led off
    time.sleep(x)

def destroy():
    GPIO.output(LedPin, GPIO.LOW)  # led off
    GPIO.cleanup()  # Release resource

def write_data():
    setup()
    blink(0.005)
    destroy()

def led_on():
    setup()
    on()

def led_off():
    off()
    destroy()


def fast_5blinks():
    setup()
    for i in range(5):
        blink(0.05)
    destroy()

def reboot_led():
    setup()
    for i in range(10):
        blink(0.05)
    destroy()

def shutdown_led():
    setup()
    for i in range(5):
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