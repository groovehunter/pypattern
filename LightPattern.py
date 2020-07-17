from time import sleep
from Panel import Panel
# edge =
# panels: Top, Left, Botton, Right
# panels = {

### define a pattern
# example: cycling middles and edges
# number of states!

# Panels might have a property of cycling through states too
# they get informed about board state nr, so they know what state they are

"""
And cycling pattern, ie 16 step pattern, with algorithmic logic
use geometric relationships and properties
ie. around the clock numbered lights 0-15
just increase counter
enable light with number == counter
disable other lights, resp. last enabled light

"""

class LogicPattern:
  def __init__(self, board):
    self.board = board
    
class PairedLightsCycling(LogicPattern):
  def initial_state(self):
    self.board.panels['t'].set_pat('oo--')
    self.board.set_panels_to_pat('rbl', '----')
  def next_state(self):
    pass



class LightPattern(object):
  states_count = 4
  def __init__(self, board):
#    self.states_count = states_count
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
