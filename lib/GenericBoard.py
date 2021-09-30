from BoardBase import BoardBase
from GenericGeometry import GenericGeometry
from DisplayBase import DisplayBase


class GenericBoard(BoardBase, GenericGeometry, DisplayBase):
  pass

  def subclass_init(self):
    pass

  def enlight_led(self, i):
    #pass
    raise NotImplementedError

#  def init_leds(self):
#    pass
