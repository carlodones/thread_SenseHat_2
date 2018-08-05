import threading
import time
import mod_measure_list
import mod_sense_hat

# Classe per l'avvio dei thread
class ThreadManager(threading.Thread):

    def __init__(self, channel, delay, source, measure_list):
        threading.Thread.__init__(self)
        self.channel = channel              # Canale di acquisizione
        self.delay = delay                  # Tempo di acquisizione in ms.
        self.source = source                # Modalità di acquisizione
        self.measure_list = measure_list    # Riferimento alla lista misure
        self.exit_flag = False              # Flag per la terminazione del thread

    # Thread per la lettura dei sensori
    def acquisition_thread(self):

        while (self.exit_flag == False):

            # Rilevo il timestamp
            ts = time.time()

            # Aggiungo alla lista misure
            self.measure_list.add_details(self.channel, self.source.read_channel(self.channel), ts)

            time.sleep(self.delay)

    def stop_thread (self):
        self.exit_flag = True

    # # Thread per il processamento delle misure
    # def parse_measures(self, exit_flag, measure_list):

    #     while self.counter:

    #         # Se ho premuto il pulsante, esco e visualizzo
    #         # il segno verde
    #         if (self.exit_flag == 1):
    #             counter = 0

    #         # Genero le medie per le grandezze rilevate
    #         for ch in channels:
    #             meas = self.measure_list.avg_by_channel(ch)

    #             # Stampo il valore della media
    #             print("TS:<" + str(meas.timestamp) + ">; NUM:<" + str(meas.count)+ ">; AVG:<" + str(meas.value)+ ">")

    #             # Aggiorno il codice canale e aggiungo la media alla lista misure
    #             meas.channel = meas.channel + 10
    #             self.measure_list.add_measure(meas)

    #             # Per la temperatura, coloro il display in funzione della media rilevata
    #             if (meas.channel == 11):
    #                 self.show_temperature(meas.value)

    #         # Genero il JSON
    #         main_dic = {}
    #         main_dic[mkc.key_timestamp] = time.time()
    #         main_dic[mkc.key_qos] = "good"
    #         main_dic[mkc.key_values] = self.measure_list.json_dictionary()

    #         self.measure_list.clear_list()

    #         print("")
    #         print("************************")
    #         print(str(json.dumps(main_dic,
    #                   indent=4, sort_keys=True,
    #                   separators=(',', ': '), ensure_ascii=False)))

    #         time.sleep(self.delay)

    #         counter -= 1
