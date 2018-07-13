import threading
import time
from random import randint
from sense_hat import SenseHat
sense = SenseHat()

# _*_ coding: utf-8 -*-

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
tempo1 = 25
tempo2 = 25
tempo3 = 25

# Creazione dei thread
thread1 = MyThread("Thread#1", tempo1)
thread2 = MyThread("Thread#2", tempo2)
thread3 = MyThread("Thread#3", tempo3)
 
# Avvio dei thread
thread1.start()

# Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidità
t = sense.get_temperature()

# Arrotondamento ad una cifra decimale
t = round(t, 1)

# str() conversione valori int in string per poterli concatenare 
message = "Temperature: " + str(t) 

# background
bg = red
      
# colore testo
tx = white
      
# Visualizzazione messaggio scorrevole SenseHat
sense.show_message(message, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
thread2.start()

# Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
p = sense.get_pressure()

# Arrotondamento ad una cifgra decimale
p = round(p, 1)

# str() conversione valori int in string per poterli concatenare 
message = " Pressure: " + str(p) 

# background
bg = green
      
# colore testo
tx = white
      
# Visualizzazione messaggio scorrevole SenseHat
sense.show_message(message, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
thread3.start()

# Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
h = sense.get_humidity()

# Arrotondamento ad una cifgra decimale
h = round(h, 1)

# str() conversione valori int in string per poterli concatenare 
message = " Humidity: " + str(h)
      
# background
bg = orange
      
# colore testo
tx = white
      
# Visualizzazione messaggio scorrevole SenseHat
sense.show_message(message, text_colour=tx, scroll_speed=0.250, back_colour=bg)
      
# Join
thread1.join()
thread2.join()
thread3.join()

#Stampa variabili int random
print ("il valore random per il primo thread è: '" + str(tempo1) + "' sec")
print ("il valore random per il primo thread e': '" + str(tempo2) + "' sec")
print ("il valore random per il primo thread e': '" + str(tempo3) + "' sec")

# Fine dello script 

message = "Fine" 

# background
bg = black
      
# colore testo
tx = red

print("Fine")

# Visualizzazione messaggio scorrevole SenseHat
while True:
      sense.show_message(message, text_colour=tx, scroll_speed=0.250, back_colour=bg)

