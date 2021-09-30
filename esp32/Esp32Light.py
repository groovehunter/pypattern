from esp32_conf import pinmap
from Light import Light

import sys
if sys.platform == 'linux':
  from esp32.Pin import DummyPin as Pin
else:
  from machine import Pin
  import uos



class Esp32Light(Light):
  def __init__(self, lid):
    Light.__init__(self, lid)
    self.pin = Pin(pinmap[lid], Pin.OUT)
  """
  def set_on(self):
    self.pin.value(1)
  def set_off(self):
    self.pin.value(0)
  """
