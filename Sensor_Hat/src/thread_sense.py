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

exitFlag = 0

VertPixels = [0, 1, 2, 3, 4, 5, 6, 7]
HorzPixels = [0, 1, 2, 3, 4, 5, 6, 7]

MaxTemp = 28
MinTemp = 23

def pushed_middle(event):
    if event.action != ACTION_RELEASED:
        exitFlag = 1
        print("exit")

class TestThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        time.sleep(self.counter)
        print("Starting " + self.name)
        if self.threadID == 1:
            acq_sensori(self.name, self.counter, 2)
        
        if self.threadID == 2:
            print_time(self.name, self.counter, 50)

        if self.threadID == 3:
            print_counter(self.name, self.counter, 50)

#  DEFINIZIONE  THREAD  ID = 1
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def acq_sensori(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        
        # background
        bg = red
        
        # colore testo
        tx = white

        # Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
        t = sense.get_temperature()

        # Arrotondamento ad una cifra decimale
        t = round(t, 1)

        # str() conversione valori int in string per poterli concatenare 
        message = "Temperature: " + str(t)

        show_temperature(t)

        # Visualizzazione messaggio scorrevole SenseHat
        # sense.show_message(message, text_colour=tx, scroll_speed=0.50, back_colour=bg)

#  DEFINIZIONE  THREAD  ID = 2
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

#  DEFINIZIONE  THREAD  ID = 3
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def print_counter(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print(threadName, "ciclo", str(counter))
        counter -= 1

def show_temperature(temp_value):
    for vp in VertPixels:
        for hp in HorzPixels:
            dist_from_center = math.sqrt((vp - 3.5)*(vp - 3.5) + (hp - 3.5)*(hp - 3.5))
            pixel_temp = temp_value * (3.5 - dist_from_center)
            pixel_light = ((pixel_temp - MinTemp) / (MaxTemp - MinTemp)) * 255
            sense.set_pixel(hp, vp, pixel_light, pixel_light, pixel_light)


# Create new threads
thread1 = TestThread(1, "Thread 1", 1000)
thread2 = TestThread(2, "Thread 2", 1000)
thread3 = TestThread(3, "Thread 3", 1000)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print("Fine del main thread")
