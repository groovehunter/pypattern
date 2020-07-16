from time import sleep
from Panel import Panel
# panel is row of [OL, IL, IR, OR] lights
# middle = IL + IR
# edge =
# panels: Top, Left, Botton, Right
# panels = {

### define a pattern
# example: cycling middles and edges
# number of states!

class LightPattern(object):
  def __init__(self, board, states_count=0):
    self.states_count = states_count
    self.states = []
    self.board = board
    self.count = 1

  def initial_state(self):
    self.state_0()

  def next_state(self):
    print " state %i" %self.count
    if self.count == self.states_count:
      self.count = 0

    self.count += 1
    #self.state_cur = self.states[self.count]
    print "next: state %i" %self.count
    exec('self.state_'+str(self.count)+'()')


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
