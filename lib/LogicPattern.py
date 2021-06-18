from lib.LightPattern import LightPattern
from lib.Light import Light


class LogicPattern(LightPattern):
  """ pattern superclass for pattern running
      by setting next state changes
      TODO change name LogicPattern to sth useful
  """

  def subclass_init(self):
    self.lights = {}
    c = 0
    # init light array with auto increment index
    for p, panel in self.board.panels.items():
      for l, light in panel.lights.items():
        self.lights[c] = light
        c += 1

    """
    # tests without panels:
    for p in range(0, 4):
      for l in range(0, 4):
        self.lights[c] = Light(c)
        c += 1
    """

    self.lights[16] = self.lights[0]
    self.lights[17] = self.lights[1]
    self.lights[18] = self.lights[2]
    self.count = 0

  def next_state(self):
    self.count += 1
    print('next PLC: ', self.count)
    if self.count > self.states_count-1:
      print("reset counter")
      self.count = 0

# Pattern subclasses

class PairedLightsCycling(LogicPattern):
  states_count = 16
  def initial_state(self):
#    self.board.panels['t'].set_pat('oo--')
#    self.set_panels_to_pat('rbl', '----')
    pass

  def next_state(self):
    super().next_state()
    self.lights[self.count].state = 0
    self.lights[self.count+1].state = 1
    self.lights[self.count+2].state = 1

class SingleDarkspotCycling(LogicPattern):
  states_count = 16
  def initial_state(self):
#    self.set_panels_to_pat('trbl', 'oooo')
    pass

  def next_state(self):
    super().next_state()
    self.lights[self.count].state = 1
    self.lights[self.count+1].state = 0

class SingleLightCyclingLP(LogicPattern):
  states_count = 16
  def initial_state(self):
    #self.set_panels_to_pat('trbl', '----')
    pass

  def next_state(self):
    super().next_state()
    self.lights[self.count].state = 0
    self.lights[self.count+1].state = 1
