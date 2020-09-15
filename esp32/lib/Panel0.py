from Light import Light

panel_map = {
    1: [1,2,3,4],
    2: [5,6,7,8],
    3: [9,10,11,12],
    4: [13,14,15,16],
}


class Panel:

  def __init__(self, pid):
    self.lights = {}
    self.pid = pid
    print(self.pid)

  def init_lights(self):
    panel_pins = panel_map[self.pid]
    print(panel_pins)
    for i in range(0, 4):
      pin_nr = panel_pins[i]
      self.lights[i] = Light(pin_nr)


  def clear(self):
    for key, light in self.lights.items():
      light.state = 0

  def full(self):
    for key, light in self.lights.items():
      light.state = 1

  def set_middle(self):
    self.lights[0].state = 0
    self.lights[1].state = 1
    self.lights[2].state = 1
    self.lights[3].state = 0

  def viceversa(self):
    for key, light in self.lights.items():
      light.viceversa()

  def __repr__(self):
    s = "Panel " + str(self.pid) + " "
    for i, light in self.lights.items():
      s += str(light.state)
    return s

  def set_pat(self, pat):
    """ set light state according to a graphical representation
        i.e. 'oooo' and '--oo'
    """
    print(self.lights)
    for i, char in enumerate(pat):
      if char=='o':
        self.lights[i].state = 1
      if char=='-':
        self.lights[i].state = 0
