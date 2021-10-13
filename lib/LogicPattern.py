from lib.LightPattern import LightPattern
from lib.Light import Light


class LogicPattern(LightPattern):
  """ pattern superclass for pattern running
      by setting next state changes
      TODO change name LogicPattern to sth useful
  """
  type = 'LogicPattern'

  def subclass_init(self):
    """ initiate array of Lights,
        version 1 were children of panels """
    self.init_light_array()
    #self.init_light_array_2()
    self.states_count = self.board.num_lights_total
  def initial_state(self):
    pass
  def next_state(self):
    """ switching to next state by rising the leds index """
    self.count += 1

    #if self.count > self.states_count-1:
    if self.count > self.states_count:
      #print("reset counter")
      self.count = 1
    #print("super next_state, count is", self.count)

### Pattern subclasses

class PairedLightsCycling(LogicPattern):
  def next_state(self):
    super().next_state()
    self.lights[self.count].state = 0
    self.lights[self.count+1].state = 1
    self.lights[self.count+2].state = 1

class SingleDarkspotCycling(LogicPattern):
  def next_state(self):
    super().next_state()
    self.lights[self.count].state = 1
    self.lights[self.count+1].state = 0

class SingleLightCycling(LogicPattern):
  def next_state(self):
    super().next_state()
    self.lights[self.count].state = 0
    self.lights[self.count+1].state = 1
    if self.count == 1:
      self.lights[self.board.num_lights_total].state = 0
