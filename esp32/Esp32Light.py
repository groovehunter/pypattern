from esp32.esp32_conf import pinmap
from lib.Light import Light
from settings import boardname

import sys
if sys.platform == 'linux':
  from esp32.Pin import DummyPin as Pin
else:
  from machine import Pin
  import uos



class Esp32Light(Light):
  def __init__(self, lid):
    Light.__init__(self, lid)
    pin_nr = pinmap[boardname][lid]
    try:
        self.pin = Pin(pin_nr, Pin.OUT)
    except ValueError:
        print("INPUT pin!", pin_nr)
        raise ValueError
    print("initiated esp32 light on pin: ", lid, pin_nr)

  def __repr__(self):
    s = "Led %i --> %s" %(self.lid, self.pin)
    return s
  """
  def set_on(self):
    self.pin.value(1)
  def set_off(self):
    self.pin.value(0)
  """
