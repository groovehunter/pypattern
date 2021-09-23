#!/usr/bin/python3

import sys
from os import getcwd, pardir
from os.path import join, dirname, abspath
parent = dirname(dirname(abspath(__file__)))
### entspricht root of project
# will it make sense
sys.path.append(parent)
print(sys.path)


import time

import tkinter as tk
import inspect
#from PatternController import PatternController
from lib.LogicPattern import *
from lib.ExplicitStatesPattern import *
from lib.PanelPattern import *
from lib.NextStatePattern import *

from tk.BoardCanvas import GameBoard
from tk.SquareFramePanels import SquareFramePanels
#from tk.SquareFramePanels0 import SquareFramePanels
from tk.StackedPanelsSquare import StackedPanelsSquare
from tk.LightningCrossQuadrants import LightningCrossQuadrants
from lib.DisplayBase import DisplayBase


class PatternControllerDisplay(DisplayBase):
  """ make pattern of pattern controller visible """

  def __init__(self):
#    Base.__init__(self)
    self.root = tk.Tk()
    #self.board = GameBoard(self.root)
#    self.board = StackedPanelsSquare(self.root)
    self.board = SquareFramePanels(self.root)
#    self.board = LightningCrossQuadrants(self.root)
    self.board.pack(side="top", fill="both", expand="true", padx=6, pady=6)
    self.board.ctrl=self
    self.gui_setup()
    self.update_clock()

  def update_clock(self):
    now = time.strftime("%H:%M:%S")
    self.label_clock.configure(text=now)
    self.root.after(1000, self.update_clock)


  def gui_setup(self):

    def set_pattern():
      pat_name = variable.get()
      constructor = globals()[pat_name]
      self.pattern = constructor(self.board)
      self.pattern.initial_state()
      # new # XXX:
      self.board.pattern = self.pattern

    self.total_pattern_list()
    variable = tk.StringVar(self.root)
    variable.set("CHOOSE PATTERN") # default value
    l1 = tk.Label(text="Pattern", fg="black", bg="white")
    l1.pack(padx=5, pady=10, side=tk.LEFT)

    w = tk.OptionMenu(self.root, variable, *self.total_patlist)
    w.pack(padx=5, pady=10, side=tk.LEFT)

    button = tk.Button(self.root, text="OK", command=set_pattern)
    button.pack(fill=tk.X)
    button = tk.Button(self.root, text="RUN", command=self.repeater)
    button.pack(fill=tk.X, side=tk.RIGHT)

    self.label_clock = tk.Label(text="", font=('Helvetica', 16), fg='red')
    self.label_clock.pack()
    self.root.after(1000, self.update_clock)

  def init(self):
    self.msecs = 500
    self.board.init_keys()
    self.board.init()

    self.pattern = PairedLightsCycling(self.board)
    self.pattern.initial_state()

  def repeater(self):
    self.pattern.next_state()
    self.board.enlighten()  # meta for flatarray and normal
#    self.board.enlighten_flatarray()
    self.root.after(self.msecs, self.repeater)    # reschedule handler

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
