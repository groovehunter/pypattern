from esp32_conf import pinmap
from Light import Light

import sys
if sys.platform == 'linux':
  class Pin:
    OUT = None
    """ dummy pin class for posix """
    def __init__(self, pid, mode):
      pass
    def on(self): pass
    def off(self): pass
    def value(self, val): pass
else:
  from machine import Pin
  import uos



class Esp32Light(Light):
  def __init__(self, lid):
    Light.__init__(self, lid)
    self.pin = Pin(pinmap[lid], Pin.OUT)
