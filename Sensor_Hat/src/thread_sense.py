import threading
import time
import math
from random import randint
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()

#Define the colours red and green
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)
orange = (255, 255, 0)
white = (255,255,255)
blue = (0, 0, 255)

exit_flag = 0
max_temp = 100
min_temp = 0
calib_cycles = 5

X = [255, 0, 0]  # Red
O = [0, 0, 0]  # Black

alt_sign = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, X, O, O, O, X, X, O,
X, O, O, O, X, O, O, X,
X, O, O, X, O, O, O, X,
O, X, X, O, O, O, X, O,
O, O, X, O, O, X, O, O,
O, O, O, X, X, O, O, O
]


def pushed_middle(event):
    if event.action != ACTION_RELEASED:
        event.exit_flag = 1
        print("exit")

class TestThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):

        avg_temp = 0
        calib = 1

        print("Calibrating " + self.name)

        while (calib <= self.calib_cycles):
            avg_temp = avg_temp + sense.get_temperature()
            print ("Calibration [" + str(calib) + "]: <" + str(avg_temp / calib) + ">")
            calib = calib + 1
            time.sleep(1)

        avg_temp = avg_temp / self.calib_cycles
        print ("Avg: <" + str(avg_temp)+ ">")

        self.max_temp = avg_temp + 2
        self.min_temp = avg_temp - 2
        print ("Min: <" + str(self.min_temp)+ ">; Max: <" +str(self.max_temp)+ ">")


        print("Starting " + self.name)
        if self.threadID == 1:
            acq_sensori(self.name, 0.5, self.counter)
"""        
        if self.threadID == 2:
            print_time(self.name, 1, self.counter)

        if self.threadID == 3:
            print_counter(self.name, 1, self.counter)
"""

#  DEFINIZIONE  THREAD  ID = 1
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def acq_sensori(threadName, delay, counter):
    while counter:
        if (threadName.exit_flag == 1):
            sense.set_pixels(alt_sign)
            threadName.exit()

        time.sleep(delay)

        # Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
        t = sense.get_temperature()

        # Arrotondamento ad una cifra decimale
        t = round(t, 1)

        print ("Temp: <" + str(t)+ ">")

        # Coloro il display in funzione della T rilevata
        show_temperature(t)

        counter -= 1

""" 
#  DEFINIZIONE  THREAD  ID = 2
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def print_time(threadName, delay, counter):
    while counter:
        if exit_flag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

#  DEFINIZIONE  THREAD  ID = 3
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def print_counter(threadName, delay, counter):
    while counter:
        if exit_flag:
            threadName.exit()
        time.sleep(delay)
        print(threadName, "ciclo", str(counter))
        counter -= 1 
"""

def show_temperature(temp_value):

    X = 0

    alt_sign = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    ]
    
    pixel_light = int( (((temp_value - min_temp) / (max_temp - min_temp)) * 255) // 1)
    if (pixel_light > 255):
        pixel_light = 255
    if (pixel_light < 0):
        pixel_light = 0

    X = pixel_light

    sense.set_pixels(alt_sign)


# Create new threads
thread1 = TestThread(1, "Thread 1", 1000)
# thread2 = TestThread(2, "Thread 2", 50)
# thread3 = TestThread(3, "Thread 3", 50)

# Start new Threads
thread1.start()
# thread2.start()
# thread3.start()
thread1.join()
# thread2.join()
# thread3.join()
print("Fine del main thread")
