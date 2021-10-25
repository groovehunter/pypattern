from lib.FixedStateNumberPattern import OppositePanelsSwitching
from lib.FixedStateNumberPattern import OppositePanelsBlinking

import time

class ComboPattern:
  type = 'ComboPattern'
  mod = 1 # times of subpattern repeats

  def __init__(self, board):
    self.board = board
    subpattern = {}
    self.count = 1

  def next_state(self):
    #print("----------------------")
    self.count += 1
    if self.count > self.states_count:
      self.count = 1


class CyclingOppositePanelsSwitching(ComboPattern):
  #subpattern = 'OPS'
  start = 1
  passed = 0

  def subclass_init(self):
    self.mod = 8  # number of subpattern loops per main pat step

    self.states_count = self.board.num_panels * self.mod
    print('COPS self.states_count ', self.states_count)
    self.subpattern = OppositePanelsSwitching(self.board)
    self.subpattern.subclass_init()
    print("ComboPattern - subclass_init - subpattern.panels", self.subpattern.panels)
    #for i, panel in self.subpattern.panels.items():
    self.panels = self.subpattern.panels

  def initial_state(self):
    pass

  def next_state(self):
    """ aktive on every time step! """
    super().next_state()
    subpat = self.subpattern
    cur = int(self.count / self.mod) +1
    rest = self.count % self.mod
    #print("count, cur, rest", self.count, cur, rest)
    subpat.start = cur
    if rest:
      subpat.next_state()
    else:                   # subpattern start
      subpat.start = cur
      subpat.count = 1
      #print("=== else: cur", cur)


class CyclingOppositePanelsBlinking(ComboPattern):
  def subclass_init(self):
    self.mod = 6  # number of subpattern loops per main pat step

    self.states_count = self.board.num_panels * self.mod
    print('COPS self.states_count ', self.states_count)
    self.subpattern = OppositePanelsBlinking(self.board)
    self.subpattern.subclass_init()
    self.panels = self.subpattern.panels
    #print("ComboPattern - subclass_init - subpattern.panels", self.subpattern.panels)

  def next_state(self):
    """ aktive on every time step! """
    super().next_state()
    subpat = self.subpattern
    cur = int(self.count / self.mod) +1
    rest = self.count % self.mod
    #print("count, cur, rest", self.count, cur, rest)
    #subpat.start = cur
    if rest:
      subpat.next_state()
    else:                   # subpattern start
      subpat.i = cur
      subpat.count = 1
      subpat.calc_opp()
      #print("=== else: cur", cur)
