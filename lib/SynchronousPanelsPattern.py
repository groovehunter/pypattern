from lib.LightPattern import LightPattern


class SynchronousPanelsPattern(LightPattern):
  """ pattern where all panels show the same at a time """

  type = 'SynchronousPanelsPattern'

  def next_state(self):
    self.count += 1
    if self.count > self.states_count:
      self.count = 1
    #print("count", self.count)

  def subclass_init(self):
    self.init_panels_array()
    self.init_pattern_panels()
    #self.count = 0
    self.states_count = self.board.num_lights_in_group
    #print(self.panels)

class Windmill(SynchronousPanelsPattern):
  panel_states = {}

  def initial_state(self):
    pc = 0
    nlig = self.board.num_lights_in_group
    for i in range(nlig):
      p = '-' * i
      p += 'o'
      p += '-' * (nlig-i-1)
      pc += 1
      self.panel_states[pc] = p

  def next_state(self):
    super().next_state()
    self.set_all_panels(self.panel_states[self.count])

class MiddleEdgeSynchronousPattern(SynchronousPanelsPattern):
  panel_states = {}

  def initial_state(self):
    nlig = self.board.num_lights_in_group
    #pc = 0
    loops = int(nlig/2)
    #print(loops)
    #p = {}
    for i in range(1, loops):
      t1 = 'o' * (i*2)
      p1 = '-' + t1 + '-'
      t2 = '-' * (i*2)
      p2 = 'o' + t2 + 'o'
      #pc += 1
    # not useful!! legacy o--o -oo- stuff onlyfor square
    self.panel_states[1] = p1
    self.panel_states[2] = p2
    print(self.panel_states)

  def next_state(self):
    super().next_state()
    self.set_all_panels(self.panel_states[self.count])
