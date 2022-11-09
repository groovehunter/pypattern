#!/usr/bin/python3

import curses
from CursesDisplay import CursesDisplay
import sys
from curses.textpad import Textbox, rectangle
import logging

class PatternControllerDisplay:
  """ make pattern of pattern controller visible """

  def __init__(self):
    self.board = CursesDisplay()
    #self.lg =
    logging.basicConfig(filename='/tmp/python.log')
    logging.info("start")

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

  pcd.board.main()
  pcd.board.create_grid()

  pcd.board.set_pattern('SingleDarkspotCycling')
  pcd.board.pattern.initial_state()
  pcd.board.test_pattern()
  #pcd.board.run()
  #pcd.board.test()
  curses.endwin()
  sys.exit()
