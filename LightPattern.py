from time import sleep
from Panel import Panel


class LightPattern(object):
  states_count = 4
  def __init__(self, board):
#    self.states_count = states_count
    self.states = []
    self.count = 1
    self.board = board
    self.subclass_init()

  def subclass_init(self):
    raise NotImplementedError

  def next_state(self):
    raise NotImplementedError

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
