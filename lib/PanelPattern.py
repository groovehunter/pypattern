from LightPattern import LightPattern


class PanelPattern(LightPattern):
  """ pattern with complete panel changes """
  states_count = 4

  def subclass_init(self):
    self.panels = {}
    for loc_index, panel in self.board.panels.items():
      print(panel.pid)
      self.panels[panel.pid] = panel

  def initial_state(self):
    pass

  def next_state(self):
    self.count += 1
    if self.count > self.states_count-1:
      self.count = 1


### Subclasses

class RotationPanelPattern(PanelPattern):
  states_count = 4
  def next_state(self):
    super().next_state()
    self.panels[self.count].full()
    self.panels[self.count+1].clear()

class SwitchingPanels(PanelPattern):
  states_count = 2
  def next_state(self):
    super().next_state()
    self.panels[self.count].full()
    self.panels[self.count+2].full()
    self.panels[self.count-1].clear()

class AddedPanels(PanelPattern):
  states_count = 4
  def next_state(self):
    super().next_state()
    self.panels[self.count].full()
