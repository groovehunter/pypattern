



class Light:
  """ has a row+col position """
  def __init__(self, position=None):
    self.position = position
    self.state = 1
  def __repr__(self):
    (x, y) = self.position
    return "Light (%i, %i): %i" %(x, y, self.state)


class Panel:

  def __init__(self, orientation=None):
    self.lights = {}
    self.orientation = orientation
    self.state = 1

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

  def reverse(self):
    for key, light in self.lights.items():
      if light.state == 0: light.state = 1
      if light.state == 1: light.state = 0

  def __repr__(self):
    for key, light in self.items():
      print light,

  def set_pat(self, pat):
    for i, char in enumerate(pat):
      if char=='o':
        self.lights[i].state = 1
      if char=='-':
        self.lights[i].state = 0

  def init_lights(self):
    (row, col) = self.offset
    if self.orientation == 'H':
      self.lights[0] = Light((row, col))
      self.lights[1] = Light((row, col+1))
      self.lights[2] = Light((row, col+2))
      self.lights[3] = Light((row, col+3))
    if self.orientation == 'V':
      self.lights[0] = Light((row, col))
      self.lights[1] = Light((row+1, col))
      self.lights[2] = Light((row+2, col))
      self.lights[3] = Light((row+3, col))
