#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com
# Used to take timelapse pictures of endoscope camera. Works as a wrapper for fswebcam.
# External dependency on apt install fswebcam   ---- $ apt install fswebcam ntpdate screen
# requires
# adduser timelapse


import threading
import datetime, subprocess, os
import re
class capture(threading.Thread):

    def __init__(self, picsLocation, testname, testtype, elapsed, flowrate):
        # initialize the inherited Thread object
        threading.Thread.__init__(self)
        self.daemon = True
        self.picsLocation = picsLocation
        self.testname = testname
        self.testtype = testtype
        self.elapsed = elapsed
        self.flowrate = flowrate
        # create a data lock
        self.my_lock = threading.Lock()

    def getDateTime(self):
        return (str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))

    def CaptureImage(self):
        if not os.path.exists(self.picsLocation):  # Create the directory if it doesn't exist.
           os.makedirs(self.picsLocation)
        #take the actual photo
        try:
                 command = 'fswebcam -i 0 -d v4l2:/dev/video0 -r 1280x960 -fps 20 -S 5 --jpeg 95 --set brightness=55% --set lights=on  --top-banner --font sans:28 --timestamp "%Y-%m-%d %H:%M" ' \
                         ' --title "{} hh:mm:ss" --subtitle "{} liters/hour" ' \
                         ' --info "Test name: {} | Type: {} " --save {}/{}.jpg'.format(self.elapsed, self.flowrate ,self.testname, self.testtype, self.picsLocation, self.getDateTime())
                 process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # take snap
                 process.wait(timeout=2)
        except:
                 pass

    def run(self):
        self.CaptureImage()


