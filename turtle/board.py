#!/usr/bin/python3
# CLI start script for turtle model of pypattern

import sys
from os import getcwd, pardir, getenv
from os.path import join, dirname, abspath
parent = dirname(dirname(abspath(__file__)))
sys.path.append(parent)
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
from lib.ComboPattern import *
from lib.Track import Track
import yaml

from lib.DisplayBase import DisplayBase
from CoordBasedBoard import *
from lib.GenericBoard import GenericBoard
from flowpy.utils import setup_logger
logger = setup_logger(__name__, __name__+'.log')

class PatternControllerDisplay(DisplayBase):
    """ make pattern of pattern controller visible """

    def set_pattern(self, pat_name=''):
        constructor = globals()[pat_name]
        self.board.pattern = constructor(self.board)
        self.board.pattern.subclass_init()


    def set_board(self):
        # self.board = GenericBoard()
        self.board = CoordTurtleBoard()
        self.board.boardname = boardname
        self.board.load_yaml_conf()
        # self.board.load_yaml_conf()
        self.board.load_py_conf()
        logger.debug('board_cfg', self.board.cfg)
        self.speed = self.board.cfg['speed']

    # XXX remove?
    def change_board(self):
        self.board.enlighten()
        self.board.update_board()

    def run(self):
        logger.debug('cfg', self.board.cfg)
        while True:
            pat_name = self.board.track.next_pattern()
            self.set_pattern(pat_name)
            num_steps = self.board.track.get_current_repeats() * self.board.pattern.states_count
            speed = self.board.track.get_current_speed()
            speed_step = self.board.track.get_speed_tend() / num_steps
            logger.debug('speed %d', int(speed))
            logger.debug('speed_step %d', speed_step)
            logger.debug('num_steps: %d', num_steps)
            for i in range(num_steps):
                self.board.pattern.next_state()
                self.change_board()
                ts = speed + i * speed_step
                # logger.debug('ts %f', ts)
                waitt = int(100 / ts)
                # logger.debug('waitt %d', waitt)
                time.sleep(waitt)


if __name__ == "__main__":
    pcd = PatternControllerDisplay()
    pcd.set_board()
    pcd.board.init()
    pcd.board.track = Track()
    # pcd.set_pattern()
    pcd.run()

    time.sleep(10)
