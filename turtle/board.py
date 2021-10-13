#!/usr/bin/python3
# CLI start script for turtle model of pypattern

import sys
from os import getcwd, pardir
from os.path import join, dirname, abspath
parent = dirname(dirname(abspath(__file__)))
sys.path.append(parent)
#print(sys.path)
from settings import boardname, global_conf

import time
import turtle
import inspect
#from PatternController import PatternController
from lib.LogicPattern import *
#from lib.ExplicitStatesPattern import *
from lib.PanelPattern import *
from lib.NextStatePattern import *
from lib.SynchronousPanelsPattern import *
from lib.FixedStateNumberPattern import *
from lib.Track import Track
import yaml

from lib.DisplayBase import DisplayBase
from CoordBasedBoard import *
from lib.GenericBoard import GenericBoard
#from TurtleSupport import TurtleBoard

class PatternControllerDisplay(DisplayBase):
  """ make pattern of pattern controller visible """

  def set_pattern(self, pat_name=''):
#    pat_name = 'SingleLightCycling'
#    pat_name = 'PairedLightsCycling'
#    pat_name = 'RotationPanelPattern'
#    pat_name = 'DarkPanelRotationPanelPattern'
#    pat_name = 'SwitchingPanels'
#    pat_name = 'SingleLightCycling'
#    pat_name = 'Windmill'
#    pat_name = 'AlternatingPanels'
#    for i, s in sorted(globals().items()):
#      print(i, s)
    constructor = globals()[pat_name]
    self.board.pattern = constructor(self.board)
    self.board.pattern.initial_state()
    #self.board.pattern.init_light_array()
    #print("board - set_pattern - before pattern.subclass_init")
    self.board.pattern.subclass_init()


  def set_board(self):
#    self.board = GenericBoard()
    self.board = CoordTurtleBoard()
    self.board.boardname = boardname
    #self.board.load_yaml_conf()
    self.board.load_py_conf()
    #self.board.boardname = self.board.cfg['boardname']
    print(self.board.boardcfg)

  # remove XXX ?
  def init(self):
    self.msecs = 2000
    self.speed = global_conf['speed']

  # XXX remove?
  def change_board(self):
    #print("change_board")
    self.board.enlighten()
    self.board.update_board()

  def run(self):
    self.timer = 0
    while True:
      self.timer += 1
      pat_name = self.board.track.next_pattern()
      self.set_pattern(pat_name)
      repeats = self.board.track.get_current_repeats()
      num_steps = self.board.pattern.states_count * repeats
      print("num_steps: ", num_steps)
      for i in range(num_steps):
        self.board.pattern.next_state()
        self.change_board()
        time.sleep(self.speed/100)


  def loop_boards(self):
    pass


if __name__ == "__main__":

  pcd = PatternControllerDisplay()
  pcd.init()
  pcd.set_board()
  pcd.board.init()
  pcd.board.track = Track()
#  pcd.set_pattern()
  pcd.run()

  time.sleep(30)
