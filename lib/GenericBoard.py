from BoardBase import BoardBase
from GenericGeometry import GenericGeometry
from DisplayBase import DisplayBase

# BoardBase ?
#class GenericBoard(GenericGeometry, DisplayBase):
class GenericBoard(BoardBase, GenericGeometry, DisplayBase):
  pass

  def subclass_init(self):
    raise NotImplementedError

  def enlight_led(self, i):
    raise NotImplementedError
