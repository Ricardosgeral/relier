#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com
# Used to take timelapse pictures of endoscope camera. Works as a wrapper for fswebcam.
# External dependency on apt install fswebcam   ---- $ apt install fswebcam ntpdate screen
# requires
# adduser timelapse

import datetime, subprocess, os

def getDateTime():
    return (str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))

def CaptureImage(picsLocation, testname, testtype, elapsed, flowrate):
    if not os.path.exists(picsLocation):  # Create the directory if it doesn't exist.
        os.makedirs(picsLocation)
    #take the actual photo
    try:
        command = 'fswebcam -i 0 -d v4l2:/dev/video0 -r 1280x720  -fps 30 -S 2 --jpeg 95 --shadow ' \
                  '--title "Time elapsed: {}" --subtitle "Flowrate: {} liters/hour" ' \
                  '--info "Test name: {}; Test type: {}" --save {}/{}.jpg'.format(elapsed, flowrate, testname, testtype, picsLocation, getDateTime())
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=3)
    except:
        pass