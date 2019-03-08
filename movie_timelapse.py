import os
import threading
import subprocess
import datetime
import re
import py3nextion_lib as nxlib
import RGBled as LED
import nextionApp as nxApp

class makemovie(threading.Thread):
    def __init__(self, picsLocation, testname, control, freq, max_vid_dur, elapsed, interval, delImages, ip):
        # initialize the inherited Thread object
        threading.Thread.__init__(self)
        self.daemon = True
        self.picsLocation = picsLocation
        self.testname = testname
        self.control=control
        self.freq = freq
        # get the ip
        self.ip = ip
        self.max_vid_dur=max_vid_dur
        self.fps = 1
        (h, m, s) = elapsed.split(':')
        self.elapsed = (int(h) * 3600 + int(m) * 60 + int(s))/60   # in minutes
        self.interval=interval
        self.delImages = delImages
        # create a data lock
        self.my_lock = threading.Lock()

    def getDateTime(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))

    def MovieMaker(self):
        os.chdir(self.picsLocation)
        if self.control ==1:  ## selected a maximum duration for the video
            self.fps = self.elapsed/(int(self.interval)*float(self.max_vid_dur))
        else:
            self.fps = int(self.freq)
        command = "ffmpeg -r {} -pattern_type glob -i '*.jpg' -c:v libx264 -s 1280x960 {}/{}_{}.mp4".format(self.fps, self.picsLocation, self.testname, self.getDateTime())
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # make video


        LED.whiteOn()
        while True:
            poll = process.poll()
            if poll != None:  # A None value indicates that the process hasn't terminated yet.
                print('time-lapse movie done')
                os.chdir('/home/pi/relier')
                ## go to credits page
                nxlib.nx_setcmd_1par(nxlib.ser, 'page', 'credits')
                nxlib.nx_setValue(nxlib.ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag
                nxlib.nx_setText(nxlib.ser, nxApp.ID_ip[0], nxApp.ID_ip[1], str(self.ip))

                try:
                    os.remove(os.path.join('/home/pi/relier', '0'))  ## fswebcam creates this temporary file
                    os.remove(os.path.join('/home/pi/relier', '10'))  ## fswebcam creates this temporary file
                    os.remove(os.path.join('/home/pi/relier', '20'))  ## fswebcam creates this temporary file
                    os.remove(os.path.join('/home/pi/relier', '30'))  ## fswebcam creates this temporary file
                except:
                    pass
                if self.delImages == 1:   # delete images if desired
                    for f in os.listdir(self.picsLocation):
                        if re.search(".jpg", f):  # if the file has the extension .jpg
                            os.remove(os.path.join(self.picsLocation, f))  # remove the file
                    print('time-lapse images deleted')
                break
        LED.whiteOff()
    def run(self):
        self.MovieMaker()