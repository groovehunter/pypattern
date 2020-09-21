from lib.Light import Light

PSIZE = 4

class Panel:

  def __init__(self, pid, size=PSIZE):
    self.lights = {}
    self.pid = pid
    self.size = size

  def init_lights(self):
    for i in range(0, self.size):
      self.lights[i] = Light(i)

  def clear(self):
    for key, val in self.lights.items():
      val.state = 0
  def full(self):
    for key, val in self.lights.items():
      val.state = 1

  def set_middle(self):
    self.lights[0].state = 0
    self.lights[1].state = 1
    self.lights[2].state = 1
    self.lights[3].state = 0

  def viceversa(self):
    for key, light in self.lights.items():
      light.viceversa()
#      if light.state == 0: light.state = 1
#      if light.state == 1: light.state = 0

  def __repr__(self):
    s = "Panel " + str(self.pid) + " "
    for i, light in self.lights.items():
      s += str(light.state)
      #s+= light.__repr__()
    #s += str(self.lights)
    return s

  def set_pat(self, pat):
    """ set light state according to a graphical representation
        i.e. 'oooo' and '--oo'
    """
    for i, char in enumerate(pat):
      if char=='o':
        self.lights[i].state = 1
      if char=='-':
        self.lights[i].state = 0
