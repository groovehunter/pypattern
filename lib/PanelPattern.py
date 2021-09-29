from lib.LightPattern import LightPattern


class PanelPattern(LightPattern):
  """ pattern with complete panel changes """
  panels = {}
  
  def subclass_init(self):  # XXX TODO unused
    #self.init_light_array()
    self.init_panels_array()

    n = self.board.num_panels
    print(self.states_count)
    self.panels = {}
    for loc_index, panel in self.board.panels.items():
      #print("subclass_init: panel.pids: ", panel.pid)
      self.panels[panel.pid] = panel
      self.panels[panel.pid].clear()
    self.panels[n+1] = self.panels[1]
    self.panels[n+2] = self.panels[2]

  def initial_state(self):
    pass

  def next_state(self):
    self.count += 1
    if self.count > self.states_count:
      print("resetting count to panel 1")
      self.count = 1
    print('next_state - self.count: ', self.count)


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
  states_count = 2
  def next_state(self):
    super().next_state()
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
