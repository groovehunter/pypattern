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
import yaml

from lib.DisplayBase import DisplayBase
from CoordBasedBoard import HexagonBoard, SquareBoard


class PatternControllerDisplay(DisplayBase):
  """ make pattern of pattern controller visible """

  def __init__(self, boardname=None):
    self.boardname = boardname

  def set_pattern(self):
#    pat_name = 'PairedLightsCycling'
    pat_name =  'RotationPanelPattern'
    constructor = globals()[pat_name]
    self.pattern = constructor(self.board)
    self.pattern.initial_state()
    self.board.pattern = self.pattern


  def init(self):
    cfgfile = open(parent + '/conf/settings.yaml')
    cfg = yaml.load(cfgfile)
    print(cfgfile)
#    print(cfgfile)
    self.boardcfg = cfg[self.boardname]
    constructor = globals()[self.boardcfg['klass']]
    self.board = constructor()
    self.board.ctrl=self
    self.board.cfg = cfg['global']

    self.configure()
    self.msecs = 2000
    self.board.init()

  def configure(self):
    for attr, val in self.boardcfg.items():
      setattr(self.board, attr, val)
    print(self.board.num_lights_total)
    for attr, val in self.board.cfg.items():
      setattr(self.board, attr, val)

  def change_board(self):
    self.board.enlighten()
    #self.pattern.state_cur.__repr__()

  def run(self):
    while True:
      self.pattern.next_state()
      self.change_board()
      time.sleep(0.5)



if __name__ == "__main__":
  boardname = 'square'
  if len(sys.argv) > 1:
    boardname = sys.argv[1]

  pcd = PatternControllerDisplay(boardname=boardname)
  pcd.init()
  pcd.set_pattern()
  pcd.run()
  time.sleep(30)
