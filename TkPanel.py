from Light import Light
from Panel0 import Panel

class TkPanel(Panel):

  def __init__(self, orientation=None, rev=False):
    """ orientation:
        (H)orizontal l2r / or reverse
        (V)ertical t2b / or reverse
    """
    Panel.__init__(self, pid)
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
      self.lights[0] = Light((row, col))
      self.lights[1] = Light((row, col + add))
      self.lights[2] = Light((row, col + 2*add))
      self.lights[3] = Light((row, col + 3*add))
    if self.orientation == 'V':
      self.lights[0] = Light((row, col))
      self.lights[1] = Light((row + add, col))
      self.lights[2] = Light((row + 2*add, col))
      self.lights[3] = Light((row + 3*add, col))
