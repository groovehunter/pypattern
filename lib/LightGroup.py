from lib.Light import LocatedLight
from lib.Panel import Panel

GSIZE = 2

class LightGroup:

  def __init__(self, pid, orientation=None, rev=False):
    """ orientation:
        (H)orizontal l2r / or reverse
        (V)ertical t2b / or reverse
    """
    Panel.__init__(self, pid, size=GSIZE)
    self.orientation = orientation
    self.reverse = rev
    self.lights = {}
    #self.state = 1


  def __repr__(self):
    for key, light in self.items():
      print(light,)


  def init_lights(self):
    """ calc light row+col positions relative to their panels,
        depending on orientation and if reverse
    """
    (row, col) = self.offset
    add = 1
    if self.reverse:
      add = -1
    if self.orientation == 'H':
      self.lights[0] = LocatedLight(0, (row, col))
      self.lights[1] = LocatedLight(1, (row, col + add))
    if self.orientation == 'V':
      self.lights[0] = LocatedLight(0, (row, col))
      self.lights[1] = LocatedLight(1, (row + add, col))
