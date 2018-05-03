import RPi.GPIO as GPIO
import time

LedPin = 18  # pin18 GPIO24

def setup():
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
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

#if __name__ == '__main__':  # Program start from here
#     setup()
#     try:
#         blink(0.1)
#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#         destroy()