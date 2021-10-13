from lib.LightPattern import LightPattern


class FixedStateNumberPattern(LightPattern):
  type = 'FixedStateNumberPattern'
  def subclass_init(self):
    self.init_panels_array()
    self.init_pattern_panels()

  def initial_state(self):
    pass
  def next_state(self):
    #print("state count", self.count)
    self.count += 1
    if self.count > self.states_count:
      self.count = 1


class AlternatingPanels(FixedStateNumberPattern):
  states_count = 2
  def next_state(self):
    super().next_state()
    # ein state is, alle ungeraden werden aktiviert
    if self.count == 1:
      for i in range(1, self.board.num_panels, 2):
        print(i)
        self.panels[i].full()
        self.panels[i+1].clear()
    else:
      for i in range(1, self.board.num_panels, 2):
        self.panels[i+1].full()
        self.panels[i].clear()


class AllOnOffPattern(FixedStateNumberPattern):
  states_count = 2
  def next_state(self):
    super().next_state()
    for i, panel in self.panels.items():
      panel.set_all_lights(self.count-1)
