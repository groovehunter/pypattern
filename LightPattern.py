from time import sleep
from Panel import Panel
# edge =
# panels: Top, Left, Botton, Right
# panels = {

### define a pattern
# example: cycling middles and edges
# number of states!

class LightPattern(object):
  def __init__(self, board, states_count=4):
    self.states_count = states_count
    self.states = []
    self.board = board
    self.count = 1

  def initial_state(self):
    self.state_0()

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

class PatternController:

  def __init__(self):
    # init as a list  - (of lists, appending later)
    self.pattern = []

  def loop(self):
    for p in self.pattern:
      self.current = p
      self.show()
      sleep(1)

  def show(self):
    print(self.current)

  def load(self, fn):
    """ load pattern sequence from a graphical file representation """
    f = open(fn, 'r')
    for line in f:
      if line.startswith('#') or line.startswith('_'):
        continue
      self.pattern.append(line)
