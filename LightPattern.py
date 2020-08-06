from time import sleep
from Panel0 import Panel


class LightPattern(object):
  states_count = 4
  def __init__(self, board):
#    self.states_count = states_count
    self.states = []
    self.board = board
    self.count = 1

  def initial_state(self):
    self.state_0()

### maybe remove this
# or raise NotImplementedEexception
  def next_state(self):
    if self.count == self.states_count:
      self.count = 0

    self.count += 1
    print("next: state %i" %self.count)
    exec('self.state_'+str(self.count)+'()')


  def set_all_panels(self, pat):
    for i, panel in self.board.panels.items():
        panel.set_pat(pat)

  def set_panels_to_pat(self, panel_indexes, pat):
    for i in panel_indexes:
      self.board.panels[i].set_pat(pat)

  def all_panels_execute_method(self, method):
    """ run ie. 'clear' or 'full' on all panels """
    for i, panel in self.board.panels.items():
        getattr(panel, method)()
