
import inspect
from LogicPattern import *
import LogicPattern
from BoardCanvas0 import GameBoard
from SquareFramePanels0 import SquareFramePanels0


class Base(object):
#  def __init__(self):
#    self.board = SquareFramePanels(self.root)
  pass



class PatternControllerDisplay(Base):
  """ make pattern of pattern controller visible """

  def __init__(self):
    Base.__init__(self)
    self.board = SquareFramePanels0()
    self.board.ctrl=self

  def init(self):
    self.msecs = 500
    self.board.init()

    self.pattern = PairedLightsCycling(self.board)
    self.pattern.initial_state()

  def repeater(self):
    self.pattern.next_state()
    self.board.enlighten()

  def next_state(self, event):
    self.pattern.next_state()
    self.change_board()

  def change_board(self):
    self.board.enlighten()
    #self.pattern.state_cur.__repr__()


if __name__ == "__main__":
  pcd = PatternControllerDisplay()
  pcd.init()
