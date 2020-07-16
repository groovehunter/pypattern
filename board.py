
import Tkinter as tk
from time import sleep

from LightPattern import PatternController
from CyclingPattern import Middle_Edge_Cycling
from BoardCanvas import GameBoard
from SquareFramePanels import SquareFramePanels
from StackedPanelsSquare import StackedPanelsSquare


class PatternControllerDisplay(object):
  """ make pattern of pattern controller visible """

  def __init__(self):
    self.pc = PatternController()
    self.root = tk.Tk()
    #self.board = GameBoard(self.root)
    self.board = SquareFramePanels(self.root)
#    self.board = StackedPanelsSquare(self.root)
    self.board.pack(side="top", fill="both", expand="true", padx=6, pady=6)

  def init(self):
    self.board.ctrl=self
    self.board.init_keys()
    self.board.init()
    self.pattern = Middle_Edge_Cycling(self.board)

  def run(self):
    self.root.mainloop()

  def next_state(self, event):
    self.pattern.next_state()
    self.change_board()

  def change_board(self):
      self.board.enlighten()
    #self.pattern.state_cur.__repr__()


if __name__ == "__main__":
  pcd = PatternControllerDisplay()
  pcd.init()
  pcd.run()
