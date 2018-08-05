import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

# Array dei canali 
channels = [1, 2]

G = [0, 127, 0]  # Green
R = [127, 0, 0]  # Red
X = [0, 0, 0]  # Off

# Segno verde: visualizzato all'avvio e al termine del programma
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

# Segno verde: visualizzato all'avvio e al termine del programma
display_off = [
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X
]

exit_flag = (0)
calib_temp = None
sense = None

x = 0
y = 0

class SenseManager(object):
    def __init__(self, channel):
        global sense
        self.channel = channel
        sense = SenseHat()
        self.show_green_sign()
        pass

    def read_channel(self):

        val = None
        
        # Verifico se ho premuto il pulsante di stop
        sense.stick.direction_middle = self.pushed_middle

        # Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
        if(self.channel == 1):
            val = sense.get_temperature()
        elif(self.channel == 2):
            val = sense.get_pressure()
        else:
            val = sense.get_humidity()

        self.light_up_pixel()

        # Arrotondamento ad una cifra decimale
        val = round(val, 2)

        return val

    
# ------------------------------------------------------------------------------------------------
#  METODI DEDICATI PER IL SENSE-HAT
# ------------------------------------------------------------------------------------------------

    # Alla pressione del pulsante del sense-hat il programma termina
    def pushed_middle(self, event):
        global exit_flag
        if event.action == ACTION_PRESSED:
            print("Button pressed")
            exit_flag = 1

    # Alla pressione del pulsante del sense-hat il programma termina
    def show_green_sign(self):
        sense.set_pixels(green_sign)

    # Alla pressione del pulsante del sense-hat il programma termina
    def turn_off_display(self):
        sense.set_pixels(display_off)

    def light_up_pixel (self):

        meas_color = []
        pix = []

        if(self.channel == 1):
            meas_color = [255, 0, 0]
        elif(self.channel == 2):
            meas_color = [0, 255, 0]
        else:
            meas_color = [0, 0, 255]

        pix = self.next_pixel()
        sense.set_pixel(pix[0], pix[1], meas_color)

    def next_pixel(self):

        global X
        global x
        global y

        pix = []

        while (sense.get_pixel(x, y) != X):

            x = x + 1

            if (x == 8):
                x = 0
                y = y + 1

            if (y == 8):
                self.turn_off_display()
                x = 0
                y = 0

        pix.append(x)
        pix.append(y)

        return pix
