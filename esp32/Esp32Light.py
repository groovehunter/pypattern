from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')
try:
    from esp32_conf import pinmap
except ImportError:
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
        logger.debug(f"Esp32Light.__init__ lid={lid}")
        logger.debug(f"pinmap={pinmap}")
        logger.debug(f"boardname={boardname}")
        logger.debug(f"pinmap[boardname]={pinmap[boardname]}")
        pin_nr = pinmap[boardname][lid]
        print(f"[Esp32Light] Initialisiere LED {lid} auf Pin {pin_nr}")
        try:
            self.pin = Pin(pin_nr, Pin.OUT)
            logger.debug(f"Pin initialisiert: lid={lid}, pin_nr={pin_nr}")
            print(f"[Esp32Light] Pin-Objekt: {self.pin}, Typ: {type(self.pin)}")
        except ValueError:
            logger.error(f"INPUT pin! {pin_nr}")
            raise ValueError
        logger.debug(f"initiated esp32 light on pin: {lid}, {pin_nr}")
        print(f"[Esp32Light] LED {lid} fertig initialisiert auf Pin {pin_nr}")

    def __repr__(self):
        s = "Led %i --> %s" % (self.lid, self.pin)
        return s

    def on(self):
        if self.state != 1:
            self.state = 1
            self.pin.value(1)

    def off(self):
        if self.state != 0:
            self.state = 0
            self.pin.value(0)
