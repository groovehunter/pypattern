import curses
from RaspiDisplay import RaspiDisplay
import sys


class PatternControllerDisplay:
  """ make pattern of pattern controller visible """

  def __init__(self):
    self.board = RaspiDisplay()

  def init(self):
    self.board.init()

  def repeater(self):
    self.pattern.next_state()
    self.board.enlighten()



if __name__ == "__main__":
  if sys.version_info.major < 3:
    print("use python 3.x")
    sys.exit()
  pcd = PatternControllerDisplay()
  pcd.init()
  #pcd.board.set_pattern('CyclingPanels')
  pcd.board.set_pattern('AllOnOff')
  #pcd.board.set_pattern('SingleDarkspotCycling')
  pcd.board.pattern.initial_state()
  pcd.board.test_pattern()
  #pcd.board.run()
  #pcd.board.test()
