#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com
# Used to take timelapse pictures of endoscope camera. Works as a wrapper for fswebcam.
# External dependency on apt install fswebcam   ---- $ apt install fswebcam ntpdate screen
# requires
# adduser timelapse


import threading
import datetime, subprocess, os

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
        try:   ## fswebcam --list-controls   (in the terminal)
                 command = 'fswebcam -i 0 -d v4l2:/dev/video0 -r 1600x1200 -fps 0 -S 4 --top-banner --font sans:28 --timestamp "%Y-%m-%d %H:%M"'\
                         ' -s Brightness=6 -s Contrast=14 -s Saturation=54 -s Hue=0 -s "White Balance Temperature, Auto"=False -s Gamma=182 -s "White Balance Temperature"=4000 -s Gain=8 -s Sharpness=7'\
                         ' -s "Exposure, Auto"="Aperture Priority Mode" -s "Exposure (Absolute)"=200'\
                         ' --title "{} hh:mm:ss" --subtitle "{} liters/hour"'\
                         ' --info "Test name: {} | Type: {}" --save {}/{}.jpg'.format(self.elapsed, self.flowrate ,self.testname, self.testtype, self.picsLocation, self.getDateTime())
                 process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # take snap
                 process.wait(timeout=0)
        except:
                 pass

    def run(self):
        self.CaptureImage()


