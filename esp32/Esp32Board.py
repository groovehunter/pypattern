#from time import sleep
#from Panel import Panel
from GenericGeometry import GenericGeometry
from BoardBase import BoardBase
from DisplayBase_uP import DisplayBase
from Esp32Light import Esp32Light

class Esp32Board(DisplayBase, GenericGeometry, BoardBase):
  def __init__(self):
    print("init board")

  def subclass_init(self):
    pass

  def enlight_led(self, i):
    pass

  def update_board(self):
    pass

  def init_leds(self):
    led = {}
    for i in range(1, self.num_lights_total+1):
      led[i] = Esp32Light(i)
    self.led = led
    print("Esp32Board - init_leds")
    print(self.led)
