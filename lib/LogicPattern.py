from lib.LightPattern import LightPattern
from lib.Light import Light


class LogicPattern(LightPattern):
  """ pattern superclass for pattern running
      by setting next state changes
      TODO change name LogicPattern to sth useful
  """

  def subclass_init(self):
    """ initiate array of Lights,
        version 1 were children of panels """
    self.init_light_array()
    #self.init_light_array_2()

  def next_state(self):
    """ switching to next state by rising the leds index """
    self.count += 1
#    print('next PLC: ', self.count)
    self.states_count = self.board.num_lights_total
    if self.count > self.states_count-1:
      print("reset counter")
      self.count = 1

# Pattern subclasses

class PairedLightsCycling(LogicPattern):

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
