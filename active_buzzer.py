#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

BuzzPin = 18  # Raspberry Pi Pin 40-GPIO 24

def setup(pin):
    global BuzzerPin
    BuzzerPin = pin
    GPIO.setmode(GPIO.BOARD)  # Set GPIO Pin As Numbering
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def on():
    GPIO.output(BuzzerPin, GPIO.LOW)

def off():
    GPIO.output(BuzzerPin, GPIO.HIGH)

def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)

def loop():
    while True:
        beep(0.5)

def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()  # Release resource


def alert_end():
    setup(BuzzPin)
    for i in range(5):
        beep(0.5)
    destroy()



# if __name__ == '__main__':  # Program start from here
#     setup(BuzzPin)
# try:
#     loop()
# except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
#     destroy()