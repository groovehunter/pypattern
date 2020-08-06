
import tkinter as tk
from time import sleep
import inspect
#from PatternController import PatternController
from LogicPattern import *
from CyclingPattern import *
from NextStatePattern import *
import LogicPattern
import CyclingPattern
import NextStatePattern
from BoardCanvas import GameBoard
from SquareFramePanels import SquareFramePanels
from StackedPanelsSquare import StackedPanelsSquare


class Base(object):
#  def __init__(self):
#    self.board = SquareFramePanels(self.root)

  def get_pattern_classes(self, module):
    pattern_list = []
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj):
        pattern_list.append(obj.__name__)
    pattern_list.remove('LightPattern')
    return pattern_list


class PatternControllerDisplay(Base):
  """ make pattern of pattern controller visible """

  def __init__(self):
    Base.__init__(self)
    self.root = tk.Tk()
    #self.board = GameBoard(self.root)
#    self.board = StackedPanelsSquare(self.root)
    self.board = SquareFramePanels(self.root)
    self.board.pack(side="top", fill="both", expand="true", padx=6, pady=6)
    self.board.ctrl=self
    self.gui_setup()


  def gui_setup(self):

    def set_pattern():
      pat_name = variable.get()
      constructor = globals()[pat_name]
      self.pattern = constructor(self.board)
      self.pattern.initial_state()
    OPTIONS = ['Choose Pattern !'] + self.get_pattern_classes(CyclingPattern)
    OPTIONS += self.get_pattern_classes(LogicPattern)
    OPTIONS += self.get_pattern_classes(NextStatePattern)
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
    self.msecs = 500
    self.board.init_keys()
    self.board.init()

    self.pattern = PairedLightsCycling(self.board)
    self.pattern.initial_state()

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
