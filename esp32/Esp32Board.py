from GenericGeometry import GenericGeometry
from BoardBase import BoardBase
from DisplayBase_uP import DisplayBase
from Esp32Light import Esp32Light
from ucollections import OrderedDict


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
#    print("Esp32Board - init_leds")
#    print(self.led)
