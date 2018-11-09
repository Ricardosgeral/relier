#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com


import RPi.GPIO as GPIO
from time import sleep
redPin = 16    # GPIO16 pin 36
greenPin = 21  # GPIO21 pin 40
bluePin = 12   # GPIO12 pin 32

def blink(pin):
    GPIO.setmode(GPIO.BCM   )
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

def blueOn():
    blink(bluePin)

def blueOff():
    turnOff(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)

def shutdown_led(): #10 fast red flashes
    for i in range(10):
        redOn()
        sleep(0.1)
        redOff()
        sleep(0.1)

def reboot_led(): #10 fast blue flashes
    for i in range(10):
        blueOn()
        sleep(0.1)
        blueOff()
        sleep(0.1)

def main():
#print("""Ensure the  GPIO connections are correct
#Colors: Red, Green, Blue, Yellow, Cyan, Magenta, and White
#Use the format: color on/color off""")
    while True:
        cmd = input("-->")

        if cmd == "red on":
            redOn()
        elif cmd == "red off":
            redOff()
        elif cmd == "green on":
            greenOn()
        elif cmd == "green off":
            greenOff()
        elif cmd == "blue on":
            blueOn()
        elif cmd == "blue off":
            blueOff()
        elif cmd == "yellow on":
            yellowOn()
        elif cmd == "yellow off":
            yellowOff()
        elif cmd == "cyan on":
            cyanOn()
        elif cmd == "cyan off":
            cyanOff()
        elif cmd == "magenta on":
            magentaOn()
        elif cmd == "magenta off":
            magentaOff()
        elif cmd == "white on":
            whiteOn()
        elif cmd == "white off":
            whiteOff()
        else:
            print("Not a valid command")