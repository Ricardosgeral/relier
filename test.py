#def function(var_1):
#    global var_2, flag
#    while True:
#        flag = False
#        if flag == True:
#            print(var_1 + var_2)
import threading
import time

class MyPlayer(threading.Thread):

    def __init__(self):

        # initialize the inherited Thread object
        threading.Thread.__init__(self)
        self.daemon = True

        # create a data lock
        self.my_lock = threading.Lock()

        # a variable exclusively used by thread1
        self.t1 = 0

        # a variable exclusively used by thread2
        self.t2 = 0

        # a variable shared by both threads
        self.g = 0

        # start thread 1
        self.thread1()

    def thread1(self):
        # start the 2nd thread
        # you must start the 2nd thread using the name "start"
        self.start()
        while True:
            with self.my_lock:
                self.t1 += 1
                self.g = self.t1 + self.t2
            print('thread 1  t1:{} t2:{} g:{}'.format(self.t1, self.t2, self.g))
            time.sleep(1)

    def run(self):
        """
        This the second thread's executable code. It must be called run.
        """
        while True:
            with self.my_lock:
                self.t2 += 1
                self.g = self.t1 + self.t2

            print('thread 2  t1:{} t2:{} g:{}'.format(self.t1, self.t2, self.g))
            time.sleep(2)


MyPlayer()