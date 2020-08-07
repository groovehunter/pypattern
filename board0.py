
from RaspiDisplay import RaspiDisplay


class PatternControllerDisplay:
  """ make pattern of pattern controller visible """

  def __init__(self):
    self.board = RaspiDisplay()

  def init(self):
    self.board.init()

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
  pcd.board.set_pattern('SingleDarkspotCycling')
  pcd.board.pattern.initial_state()
  #pcd.test_pattern()
  pcd.board.run()
