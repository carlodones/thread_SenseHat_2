import threading
import time
import math
import json
import mod_measure_list
import mod_constants
from random import randint
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()

G = [0, 127, 0]  # Green
R = [127, 0, 0]  # Red

# Array dei canali 
channels = [1, 2]

# Segno verde: visualizzato al termine del programma
green_sign = [
G, G, G, G, G, G, G, G,
G, G, G, R, R, G, G, G,
G, G, R, G, G, R, G, G,
G, R, G, G, G, G, R, G,
G, R, G, G, G, G, R, G,
G, G, R, G, G, R, G, G,
G, G, G, R, R, G, G, G,
G, G, G, G, G, G, G, G
]

exit_flag = (0)


# Alla pressione del pulsante del sense-hat il programma termina
def pushed_middle(event):
    global exit_flag
    if event.action == ACTION_PRESSED:
        print("Button pressed")
        exit_flag = 1

# Classe per eseguire la calibrazione iniziale
class Calibration(object):

    def __init__(self, sensor, pcycles=5, pmin=0, pmax=100):
        self.sensor = sensor
        self.pcycles = pcycles
        self.pmin = pmin
        self.pmax = pmax

    def calibrate(self):

        avg_temp = 0
        calib = 1

        # Avvio fase di calibrazione iniziale: la temperatura media risulta
        # da una media di 5 rilevazioni della temperatura ambiente
        print("Calibrating Sensor: <" + self.sensor + ">")

        while (calib <= self.pcycles):
            avg_temp = avg_temp + sense.get_temperature()
            print ("Calibration [" + str(calib) + "]: <" + str(avg_temp / calib) + ">")
            calib = calib + 1
            time.sleep(1)

        avg_temp = avg_temp / self.pcycles
        print ("Avg: <" + str(avg_temp)+ ">")

        # Fisso i valori di riferimento del range di temperatura
        # (+/- 1C rispetto alla temperatura di calibrazione)
        self.pmax = avg_temp + 1
        self.pmin = avg_temp - 1
        print ("Min: <" + str(self.pmin)+ ">; Max: <" +str(self.pmax)+ ">")

# Classe per l'avvio dei thread
class StartThread(threading.Thread):

    def __init__(self, threadID, name, delay, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay

    def run(self):

        # Avvio il thread di acquisizione
        print("Starting " + self.name)
        if self.threadID == 1:
            self.read_sensors(self.name, self.delay, self.counter)
        if self.threadID == 2:
            self.parse_measures(self.name, self.delay, self.counter)
        print("Started " + self.name)

    # Thread per la lettura dei sensori
    def read_sensors(self, threadName, delay, counter):

        global exit_flag
        global measure_list

        while counter:
            # Verifico se ho premuto il pulsante di stop
            sense.stick.direction_middle = pushed_middle

            # Se ho premuto il pulsante, esco e visualizzo
            # il segno verde
            if (exit_flag == 1):
                counter = 0

            # Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
            t = sense.get_temperature()
            p = sense.get_pressure()

            # Arrotondamento ad una cifra decimale
            t = round(t, 2)
            p = round(p, 2)

            # Rilevo il timestamp
            ts = time.time()

            # Aggiungo alla lista misure
            measure_list.add_details(1, t, ts)
            measure_list.add_details(2, p, ts)

            time.sleep(delay)

            counter -= 1

    # Thread per il processamento delle misure
    def parse_measures(self, threadName, delay, counter):

        global exit_flag
        global measure_list
        global mkc

        while counter:
            # Verifico se ho premuto il pulsante di stop
            sense.stick.direction_middle = pushed_middle

            # Se ho premuto il pulsante, esco e visualizzo
            # il segno verde
            if (exit_flag == 1):
                counter = 0

            # Genero le medie per le grandezze rilevate
            for ch in channels:
                meas = measure_list.avg_by_channel(ch)

                # Stampo il valore della media
                print("TS:<" + str(meas.timestamp) + ">; NUM:<" + str(meas.count)+ ">; AVG:<" + str(meas.value)+ ">")

                # Aggiorno il codice canale e aggiungo la media alla lista misure
                meas.channel = meas.channel + 10
                measure_list.add_measure(meas)

                # Per la temperatura, coloro il display in funzione della media rilevata
                if (meas.channel == 11):
                    self.show_temperature(meas.value)

            # Genero il JSON
            main_dic = {}
            main_dic[mkc.key_timestamp] = time.time()
            main_dic[mkc.key_qos] = "good"
            main_dic[mkc.key_values] = measure_list.json_dictionary()

            measure_list.clear_list()

            print("")
            print("************************")
            print(str(json.dumps(main_dic,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)))

            time.sleep(delay)

            counter -= 1

    # Metdodo per la colorazione del display del sensehat
    def show_temperature(self, temp_value):

        global calib_temp

        # Calcolo il livello di colore (tra 1 e 255) proporzionale alla temperatura rilevata
        pixel_light = int( (((temp_value - calib_temp.pmin) / (calib_temp.pmax - calib_temp.pmin)) * 255) // 1)
        if (pixel_light > 255):
            pixel_light = 255
        if (pixel_light < 0):
            pixel_light = 0

        # Creo il codice colore di riferimento:
        # Blu = freddo; Rosso = caldo
        X = [pixel_light, 0, 255 - pixel_light]

        # Matrice "tinta unita"
        one_level = [
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X
        ]
        
        # Coloro il display in tinta unita
        sense.set_pixels(one_level)

sense.set_pixels(green_sign)
mkc = mod_constants.MQTTKeysConstant()

# Eseguo la calibrazione iniziale
calib_temp = Calibration("SenseHat-Temp")
measure_list = mod_measure_list.MeasureList()

# Create new threads
th_acquisition = StartThread(1, "Acquisition", 2, 500)
th_process = StartThread(2, "Process", 20, 50)

# Start new Threads
th_acquisition.start()
th_process.start()

th_acquisition.join()
th_process.join()

sense.set_pixels(green_sign)
print("Termine programma")
