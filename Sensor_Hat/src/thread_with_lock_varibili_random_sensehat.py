import threading
import time
from random import randint
from sense_hat import SenseHat
sense = SenseHat()

# Define the colours red and green
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)
orange = (255, 255, 0)
white = (255,255,255)

# Definizione del lock per sincronizzazione e avvio sequenziale
threadLock = threading.Lock()
 
class MyThread (threading.Thread):
   def __init__(self, nome, durata):
      threading.Thread.__init__(self)
      self.nome = nome
      self.durata = durata
   def run(self):
      # Acquisizione del lock 
      threadLock.acquire()
      time.sleep(self.durata)
      print ("Thread '" + self.name + "' terminato")
      # Rilascio del lock
      threadLock.release()

# Definizione variabili
tempo1 = randint(1,10)
tempo2 = randint(1,10)
tempo3 = randint(1,10)

# Creazione dei thread
thread1 = MyThread("Thread#1", tempo1)
thread2 = MyThread("Thread#2", tempo2)
thread3 = MyThread("Thread#3", tempo3)
 
# Avvio dei thread
thread1.start()
while True:
      # Take readings from all three sensors
      t = sense.get_temperature()
      p = sense.get_pressure()
      h = sense.get_humidity()

      # Round the values to one decimal place
      t = round(t, 1)
      p = round(p, 1)
      h = round(h, 1)

      # str() conversione valori int in string per poterli concatenare 
      message = "Temperature: " + str(t) + " Pressure: " + str(p) + " Humidity: " + str(h)
      
      # background
      bg = red
      
      # colore testo
      tx = white
      
      # Display the scrolling message
      sense.show_message(messaggio, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
      # Display the scrolling message
      sense.show_message(messaggio, text_colour=tx, scroll_speed=0.250, back_colour=bg)
thread2.start()
while True:
      # Take readings from all three sensors
      t = sense.get_temperature()
      p = sense.get_pressure()
      h = sense.get_humidity()

      # Round the values to one decimal place
      t = round(t, 1)
      p = round(p, 1)
      h = round(h, 1)

      # str() conversione valori int in string per poterli concatenare 
      message = "Temperature: " + str(t) + " Pressure: " + str(p) + " Humidity: " + str(h)
      
      # background
      bg = red
      
      # colore testo
      tx = white
      
      # Display the scrolling message
      sense.show_message(messaggio, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
      # Display the scrolling message
      sense.show_message(messaggio, text_colour=tx, scroll_speed=0.250, back_colour=bg)

thread3.start()
while True:
      # Take readings from all three sensors
      t = sense.get_temperature()
      p = sense.get_pressure()
      h = sense.get_humidity()

      # Round the values to one decimal place
      t = round(t, 1)
      p = round(p, 1)
      h = round(h, 1)

      # str() conversione valori int in string per poterli concatenare 
      message = "Temperature: " + str(t) + " Pressure: " + str(p) + " Humidity: " + str(h)
      
      # background
      bg = red
      
      # colore testo
      tx = white
      
      # Display the scrolling message
      sense.show_message(messaggio, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
      # Display the scrolling message
      sense.show_message(messaggio, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
# Join
thread1.join()
thread2.join()
thread3.join()

#Stampa variabili int random
print ("il valore random per il primo thread e': '" + str(tempo1) + "' sec")
print ("il valore random per il primo thread e': '" + str(tempo2) + "' sec")
print ("il valore random per il primo thread e': '" + str(tempo3) + "' sec")

# Fine dello script

print("Fine")