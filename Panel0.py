


class Light:
  def __init__(self):
    self.state = 1
  def viceversa(self):
    if self.state == 0: self.state = 1
    if self.state == 1: self.state = 0
  def __repr__(self):
    return "Light %i" %(self.state)



class Panel:

  def __init__(self):
    self.lights = {}

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
    for key, light in self.items():
      print(light,)

  def set_pat(self, pat):
    """ set light state according to a graphical representation
        i.e. 'oooo' and '--oo'
    """
    for i, char in enumerate(pat):
      if char=='o':
        self.lights[i].state = 1
      if char=='-':
        self.lights[i].state = 0

  def init_lights(self):
    """ calc light row+col positions relative to their panels,
        depending on orientation and if reverse
    """
    for i in range(15):
      self.lights[i] = Light()
