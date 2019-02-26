import os
import threading
import subprocess
import datetime
import re

class makemovie(threading.Thread):

    def __init__(self, picsLocation, testname, control, freq, max_vid_dur, elapsed, interval, delImages):
        # initialize the inherited Thread object
        threading.Thread.__init__(self)
        self.daemon = True
        self.picsLocation = picsLocation
        self.testname = testname
        self.control=control
        self.freq = freq
        self.max_vid_dur=max_vid_dur
        self.elapsed=elapsed
        self.interval=interval
        self.delImages = delImages
        # create a data lock
        self.my_lock = threading.Lock()

    def getDateTime(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))

    def MovieMaker(self):
        os.chdir(self.picsLocation)
        if self.control ==1:  ## selected a maximum duration for the video
            self.freq = (int(self.elapsed)/60)/(int(self.interval)*int(self.max_vid_dur))
        else:
            self.freq = int(self.freq)
        command = "ffmpeg -r {} -pattern_type glob -i '*.jpg' -c:v libx264 -s 1280x960 {}/{}_{}.mp4".format(self.freq, self.picsLocation, self.testname, self.getDateTime())
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # make video

        # delete images if desired
        while True:
            poll = process.poll()
            if poll != None:  # A None value indicates that the process hasn't terminated yet.
                print('time-lapse movie done')
                if self.delImages == 1:   # delete the photos
                    for f in os.listdir(self.picsLocation):
                        if re.search(".jpg", f):  # if the file has the extension .jpg
                            os.remove(os.path.join(self.picsLocation, f))  # remove the file
                    print('time-lapse images deleted')
                break

    def run(self):
        self.MovieMaker()
