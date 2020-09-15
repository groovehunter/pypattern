
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


pinmap = {
1: 2,
2: 4,
3: 5,
4: 18,
5: 19,
6: 21,
7: 22,
8: 23,

9: 13,
10: 12,
11: 14,
12: 27,
13: 26,
14: 25,
15: 33,
16: 32,
}


class Light:
  def __init__(self, lid):
    self.lid = lid
    self.pin = Pin(pinmap[lid], Pin.OUT)
    self.state = False

  def viceversa(self):
    self.state = not self.state

  def __repr__(self):
    return "%i" %(self.state)
