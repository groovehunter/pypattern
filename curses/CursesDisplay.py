from curses.BoardCanvasNC import GameBoard
from time import sleep
from curses.textpad import rectangle, Textbox
from lib.DisplayBase import DisplayBase

class CursesDisplay(DisplayBase, GameBoard):
    def __init__(self):
        self.lights = {}
        stdscr = curses.initscr()
        curses.start_color()
        GameBoard.__init__(self, stdscr)
        curses.noecho()

    def main(self):
        stdscr = self.stdscr
        stdscr.addstr(1, 1, "Enter command")
        self.editwin = curses.newwin(45, 60)
        rectangle(self.editwin, 1, 1, 40, 59)
        for row in range(2, 20):
            for col in range(2, 20):
                self.editwin.addstr(row, col, 'X')
        stdscr.refresh()
        box = Textbox(self.editwin)
        self.editwin.move(2, 2)
        box.edit()

    def test_pattern(self):
        while True:
            self.pattern.next_state()
            self.enlighten()
            sleep(1)

    def run(self):
        while True:
            for ww in range(10):
                self.set_random_pat()
                for one in range(50):
                    pass
