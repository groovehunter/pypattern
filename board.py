
import tkinter as tk
from time import sleep
import inspect
from LightPattern import PatternController
from CyclingPattern import *
import CyclingPattern
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
    self.board.ctrl=self
    self.gui_setup()

  def get_pattern_classes(self):
    pattern_list = []
    for name, obj in inspect.getmembers(CyclingPattern):
      if inspect.isclass(obj):
        pattern_list.append(obj.__name__)
    pattern_list.remove('LightPattern')
    return pattern_list

  def gui_setup(self):

    def set_pattern():
      pat_name = variable.get()
      constructor = globals()[pat_name]
      self.pattern = constructor(self.board)

    OPTIONS = ['Choose Pattern !'] + self.get_pattern_classes()
    variable = tk.StringVar(self.root)
    variable.set(OPTIONS[0]) # default value
    l1 = tk.Label(text="Pattern", fg="black", bg="white")
    l1.pack()

    w = tk.OptionMenu(self.root, variable, *OPTIONS)
    w.pack()

    button = tk.Button(self.root, text="OK", command=set_pattern)
    button.pack()
    button = tk.Button(self.root, text="RUN", command=self.repeater)
    button.pack()

  def init(self):
    self.msecs = 800
    self.board.init_keys()
    self.board.init()

  def repeater(self):
    self.pattern.next_state()
    self.board.enlighten()
    self.board.after(self.msecs, self.repeater)    # reschedule handler

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
