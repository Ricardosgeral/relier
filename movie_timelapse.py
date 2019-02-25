import os
import threading
import subprocess
import datetime
class makemovie(threading.Thread):

    def __init__(self, picsLocation, testname, control, freq, max_vid_dur, elapsed, interval):
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
        # create a data lock
        self.my_lock = threading.Lock()

    def getDateTime(self):
        return (str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M")))

    def MovieMaker(self):
        os.chdir(self.picsLocation)
        if self.control ==1:  ## selected a maximum duration for the video
            self.freq = (self.elapsed/60)/(int(self.interval)*int(self.max_vid_dur))
        else:
            self.freq = int(self.freq)
        command = "ffmpeg -r {} -pattern_type glob -i '*.jpg' -c:v libx264 -s 1280x960 {}/{}_{}.mp4".format(self.freq, self.picsLocation, self.testname, self.getDateTime())
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # make video
        process.wait(timeout=10)
        print('time-lapse movie done')

    def run(self):
        self.MovieMaker()
