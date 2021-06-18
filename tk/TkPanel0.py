from lib.Light import LocatedLight
from lib.Panel import Panel

class TkPanel(Panel):

  def __init__(self, pid, orientation=None, rev=False):
    """ orientation:
        (H)orizontal l2r / or reverse
        (V)ertical t2b / or reverse
    """
    #Panel.__init__(self, pid)
    self.orientation = orientation
    self.reverse = rev
    self.lights = {}

  def __repr__(self):
    for key, light in self.items():
      print(light,)
