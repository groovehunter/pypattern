#!/usr/bin/python3

import sys
from os import getcwd, pardir
from os.path import join, dirname, abspath
parent = dirname(dirname(abspath(__file__)))
# entspricht root of project
sys.path.append(parent)
# print(sys.path)
from flowpy.utils import setup_logger
logger = setup_logger('board', 'tk.board.log')

import time
import tkinter as tk
#import inspect
# from PatternController import PatternController
from lib.LogicPattern import *
#from lib.ExplicitStatesPattern import *
#from lib.PanelPattern import *
#from lib.NextStatePattern import *

#from tk.BoardCanvas import GameBoard
from tk.SquareFramePanels import SquareFramePanels
# from tk.SquareFramePanels0 import SquareFramePanels
#from tk.StackedPanelsSquare import StackedPanelsSquare
#from tk.LightningCrossQuadrants import LightningCrossQuadrants
from lib.DisplayBase import DisplayBase, get_pattern_class_by_name
from lib.BoardBase import BoardBase
from lib.Track import Track
from settings import boardname


class PatternControllerDisplay(DisplayBase, BoardBase):
    """ make pattern of pattern controller visible """

    def __init__(self, **kwargs):
        self.root = tk.Tk()
        # self.board = GameBoard(self.root)
        # self.board = StackedPanelsSquare(self.root)
        self.board = SquareFramePanels(self.root)
        # self.board = LightningCrossQuadrants(self.root)
        self.board.pack(side="top", fill="both", expand=True, padx=6, pady=6)
        self.board.ctrl = self
        #self.mode = 'default'
        #self.boardname = 'square'
        #if 'mode' in kwargs:
        self.mode = kwargs.get('mode', 'default')
        #if 'boardname' in kwargs:
        self.boardname = kwargs.get('boardname', 'square')

        if self.mode == 'track':
            self.track = Track()
        self.load_yaml_conf()

        self.gui_setup()
        self.update_clock()
        logger.warning("=== START")
        # 2025
        self.sleep_ms = 0.5

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label_clock.configure(text=now)
        self.root.after(1000, self.update_clock)

    def gui_setup(self):
        logger.debug("gui_setup")
        """
        def set_pattern():
            pat_name = variable.get()
            #constructor = globals()[pat_name]
            constructor = get_pattern_class_by_name(pat_name)
            self.pattern = constructor(self.board)
            self.pattern.initial_state()
            self.board.pattern = self.pattern

            self.pattern.subclass_init()
        """

        self.total_pattern_list()

        self.variable = tk.StringVar(self.root)
        self.variable.set("CHOOSE PATTERN")  # default value
        l1 = tk.Label(text="Pattern", fg="black", bg="white")
        l1.pack(padx=5, pady=10, side=tk.LEFT)

        logger.debug("total_patlist: %s", self.total_patlist)
        # OptionMenu erwartet: parent, variable, value, *values
        if self.total_patlist:
            w = tk.OptionMenu(self.root, self.variable, self.total_patlist[0], *self.total_patlist)
        else:
            w = tk.OptionMenu(self.root, self.variable, '')
        w.pack(padx=5, pady=10, side=tk.LEFT)

        button = tk.Button(self.root, text="Set Pattern", command=self.set_pattern)
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
        self.board.track = Track()

        self.pattern = PairedLightsCycling(self.board)
        self.pattern.initial_state()
        logger.debug(self.pattern)

    def repeater(self):
        if self.mode == 'track':
            pat_name = self.track.next_pattern()
            self.set_pattern(pat_name=pat_name)
            repeats = self.track.get_current_repeats()
        else:
            repeats = 1

        num_steps = self.pattern.states_count * repeats
        for i in range(num_steps):
            self.pattern.next_state()
            self.change_board()
            time.sleep(self.sleep_ms)

        self.board.enlighten()  # meta for flatarray and normal
        # self.board.enlighten_flatarray()
        self.root.after(self.msecs, self.repeater)  # reschedule handler

    def run(self):
        self.root.mainloop()

    def next_state(self, event):
        logger.debug("PatternControllerDisplay - next_state - pattern %s", self.pattern.type)
        self.pattern.next_state()
        self.change_board()

    def change_board(self):
        self.board.enlighten()
        # self.pattern.state_cur.__repr__()

if __name__ == "__main__":
    argv = sys.argv
    options = {}

    if len(argv) > 1:
        options['mode'] = argv[1]
        print("mode from cmdline: ", mode)
    if len(argv) > 2:
        options['boardname'] = argv[2]
        print("boardname from cmdline: ", boardname)

    pcd = PatternControllerDisplay(**options)
    pcd.init()
    pcd.run()
