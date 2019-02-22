import os
import threading
import subprocess
import datetime
class makemovie(threading.Thread):

    def __init__(self, picsLocation, testname, images_per_sec = 3):
        # initialize the inherited Thread object
        threading.Thread.__init__(self)
        self.daemon = True
        self.picsLocation = picsLocation
        self.testname = testname
        self.images_per_sec = images_per_sec
        # create a data lock
        self.my_lock = threading.Lock()

    def getDateTime(self):
        return (str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M")))

    def MovieMaker(self):
        os.chdir(self.picsLocation)
        command = "ffmpeg -r {} -pattern_type glob -i '*.jpg' -c:v libx264 -s 1280x960 {}/{}_{}.mp4".format(self.images_per_sec, self.picsLocation, self.testname, self.getDateTime())
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # make video
        process.wait(timeout=10)
        print('timelapse movie done')

    def run(self):
        self.MovieMaker()
