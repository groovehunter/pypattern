from lib.LightPattern import LightPattern


class PanelPattern(LightPattern):
  """ pattern with complete panel changes """
  panels = {}
  type = 'PanelPattern'

  def subclass_init(self):
    """ special inits for PanelPattern, a flat array and the panels """
    #self.init_light_array()
    self.states_count = self.board.num_panels
    self.init_panels_array()
    self.init_pattern_panels()

  def initial_state(self):
    pass

  def next_state(self):
    """ step to next state for all PanelPatterns """
    self.count += 1
    if self.count > self.states_count:
      #print("resetting count to panel 1")
      self.count = 1


### Subclasses
# XXX rename to RotatingPanel
class RotationPanelPattern(PanelPattern):

  def next_state(self):
    super().next_state()
    if self.count > 1:
      self.panels[self.count-1].clear()
    else:
      self.panels[self.states_count].clear()

    self.panels[self.count].full()

# XXX rename to RotatingDarkPanel
class DarkPanelRotationPanelPattern(PanelPattern):

  def initial_state(self):
    for loc_index, panel in self.panels.items():
      panel.full()
  def next_state(self):
    super().next_state()
    self.panels[self.count].full()
    self.panels[self.count+1].clear()

class SwitchingPanels(PanelPattern):
  # legacy
  def next_state(self):
    super().next_state()

    #for i, panel in self.panels.items():
    #  panel.
    self.panels[self.count].full()
    self.panels[self.count+2].full()
    self.panels[self.count+1].clear()
    self.panels[self.count+3].clear()


class AddedPanels(PanelPattern):
  states_count = 4
  def next_state(self):
    super().next_state()
    self.panels[self.count].full()
#    if self.panels[self.count].is_full():
#        self.panels[self.count].clear()
