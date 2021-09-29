from lib.Light import Light, CoordLight

PSIZE = 4

class Panel:

  def __init__(self, pid, size=PSIZE):
    self.lights = {}
    self.pid = pid
    self.size = size

  def init_lights(self):
    for i in range(1, self.size+1):
      self.lights[i] = Light(i)

  def clear(self):
    for key, val in self.lights.items():
      val.state = 0
  def full(self):
    for key, val in self.lights.items():
      val.state = 1

  def set_middle(self):
    self.lights[1].state = 0
    self.lights[2].state = 1
    self.lights[3].state = 1
    self.lights[4].state = 0

  def viceversa(self):
    for key, light in self.lights.items():
      light.viceversa()
#      if light.state == 0: light.state = 1
#      if light.state == 1: light.state = 0

  def __repr__(self):
    s = "Panel " + str(self.pid) + " "
    for i, light in self.lights.items():
      s += str(int(light.state))
      s += ' '
      #s+= light.__repr__()
    #s += str(self.lights)
    return s

  def set_pat(self, pat):
    """ set light state according to a graphical representation
        i.e. 'oooo' and '--oo'
    """
    for i, char in enumerate(pat):  # i starts from 0
      if char=='o':
        self.lights[i+1].state = 1
      if char=='-':
        self.lights[i+1].state = 0

  def is_full(self):
    assume = True
    for key, light in self.lights.items():
      print(light.state)
      if not light.state:
        return False
    return assume


class PanelCoordLights(Panel):
  def init_lights(self):
    for i in range(1, self.size+1):
      self.lights[i] = CoordLight(i)
