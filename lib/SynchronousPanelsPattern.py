from lib.LightPattern import LightPattern


class SynchronousPanelsPattern(LightPattern):
  """ pattern where all panels show the same at a time """
  
  type = 'SynchronousPanelsPattern'

  def next_state(self):
    self.count += 1
    if self.count > self.states_count:
      #print("resetting count to panel 1")
      self.count = 1
    #print('next_state - self.count: ', self.count)

  def subclass_init(self):
    self.states_count = self.board.num_lights_in_group


class Windmill(SynchronousPanelsPattern):
  #panel_states = ['-o', 'o-']
  #panel_states = {1:'-o', 2:'o-'}
  panel_states = {1:'o---', 2:'-o--', 3:'--o-', 4:'---o'}
  panel_states = {1:'oo--', 2:'-oo-', 3:'--oo', 4:'o--o'}
  panel_states = {1:'ooo-', 2:'-ooo', 3:'o-oo', 4:'oo-o'}
  def initial_state(self):
    self.set_all_panels('o-')
    for i, panel in self.board.panels.items():
      pass

  def next_state(self):
    super().next_state()
    pass
    self.set_all_panels(self.panel_states[self.count])
