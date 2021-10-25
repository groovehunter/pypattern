from lib.LightPattern import LightPattern
from lib.PatternHelper import PatternHelper

# self.panels ist ein attribut nur von lightpattern
# damit sind changes nicht beim board registriert.
# werden daher bei enlight nicht umgesetzt

class FixedStateNumberPattern(LightPattern):
  type = 'FixedStateNumberPattern'

  def subclass_init(self):
    print("FixedStateNumberPattern - subclass_init")
    self.init_panels_array()
    self.init_pattern_panels()

  def initial_state(self):
    pass
  def next_state(self):
#    print("state count", self.count)
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


class FiftyFiftyPattern(FixedStateNumberPattern):
  states_count = 2

  def next_state(self):
    super().next_state()
    np = self.board.num_panels

    # change panels - all with index=odd to full and even to clear
    # and vice versa on second step and back again
    if self.count == 1:
      for i in range(1, np, 2):
        self.panels[i].full()
      for i in range(2, self.board.num_panels+1, 2):
        self.panels[i].clear()

    if self.count == 2:
      for i in range(1, self.board.num_panels, 2):
        self.panels[i].clear()
      for i in range(2, self.board.num_panels+1, 2):
        self.panels[i].full()


class OppositePanelsSwitching(FixedStateNumberPattern, PatternHelper):
  states_count = 2
  start = 1
  i = 1
  def subclass_init(self):
    super().subclass_init()
    self.calc_opp()

  def initial_state(self):
    print("OPS _ start pos", self.i)

  def next_state(self):
    super().next_state()
    i = self.i
    opp = self.opp
    if self.count == 1:
      self.panels[i].full()
      self.panels[opp].clear()
    if self.count == 2:
      self.panels[i].clear()
      self.panels[opp].full()

class OppositePanelsBlinking(FixedStateNumberPattern, PatternHelper):
  states_count = 2
  start = 1
  i = 1
  def subclass_init(self):
    super().subclass_init()
    self.calc_opp()
    self.all_panels_execute_method('clear') # necessary??

  def next_state(self):
    super().next_state()
    opp = self.opp
    i = self.i

    if self.count == 1:
      if i >1:
        self.panels[i-1].clear()
      self.panels[i].full()
      if opp >1:
        self.panels[opp-1].clear()
      self.panels[opp].full()

    if self.count == 2:
      self.panels[i].clear()
      self.panels[opp].clear()
