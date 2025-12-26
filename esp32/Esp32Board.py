from lib.GenericGeometry import GenericGeometry
from lib.BoardBase import BoardBase
from lib.DisplayBase_uP import DisplayBase

try:
    from Esp32Light import Esp32Light
except ImportError:
    from esp32.Esp32Light import Esp32Light

try:
    from ucollections import OrderedDict  # MicroPython
except ImportError:
    from collections import OrderedDict   # CPython


class Esp32Board(DisplayBase, GenericGeometry, BoardBase):
    def __init__(self):
        print("init board")

    def subclass_init(self):
        pass

    def enlight_led(self, i):
        """ accessing the hardware pins """
        self.led[i].pin.value(self.led[i].state)
        #print(self.led[i].pin, self.led[i].state)

    def change_board(self):
        super().enlighten()
        #self.enlighten()

    # stub XXX del
    def update_board(self):
        pass

    def init_leds(self):
        led = OrderedDict()
        for i in range(1, self.num_lights_total+1):
            led[i] = Esp32Light(i)
        self.led = led
        print("Esp32Board - init_leds")
        #print(self.led)
