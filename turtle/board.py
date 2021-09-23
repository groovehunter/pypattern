#!/usr/bin/python3


import sys
from os import getcwd, pardir
from os.path import join, dirname, abspath
parent = dirname(dirname(abspath(__file__)))
sys.path.append(parent)
print(sys.path)


import time
import turtle
import inspect
#from PatternController import PatternController
from lib.LogicPattern import *
from lib.ExplicitStatesPattern import *
from lib.PanelPattern import *
from lib.NextStatePattern import *

from lib.DisplayBase import DisplayBase
from CoordBasedBoard import HexagonBoard


class PatternControllerDisplay(DisplayBase):
  """ make pattern of pattern controller visible """

  def __init__(self):
    self.board = HexagonBoard()
    self.board.ctrl=self

  def set_pattern(self):
#    pat_name = 'PairedLightsCycling'
    pat_name =  'RotationPanelPattern'
    constructor = globals()[pat_name]
    self.pattern = constructor(self.board)
    self.pattern.initial_state()
    self.board.pattern = self.pattern


  def init(self):
    self.msecs = 2000
    self.board.init()


  def change_board(self):
    self.board.enlighten()
    #self.pattern.state_cur.__repr__()

  def run(self):
    while True:
      self.pattern.next_state()
      self.change_board()
      time.sleep(0.5)



if __name__ == "__main__":
  pcd = PatternControllerDisplay()

#  t = turtle.getturtle()
  #screen = turtle.getscreen()
  # WARNINGG urtle.tracer(0,0)
#  turtle.update()
  pcd.init()
  pcd.set_pattern()
  pcd.run()
  time.sleep(30)
