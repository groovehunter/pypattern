import curses
from Panel0 import Panel


class GameBoard:
  def __init__(self, stdscr, rows=6, columns=6, size=10):

    self.stdscr = stdscr
    self.rows = rows
    self.columns = columns
    self.size = size

    width = columns * size
    height = rows * size


  def init(self):
    self.init_panels()
    self.init_panel_lights()

  def create_grid(self):
    #or = 2
    #oc = 2
    for row in range(self.rows):
      for col in range(self.columns):
        self.editwin.addstr(2+row, 2+col, 'o')
    self.stdscr.refresh()

  def init_panels(self):
    self.panels = {
      't' : Panel(1),
      'r' : Panel(2),
      'b' : Panel(3),
      'l' : Panel(4),
    }

  def init_panel_lights(self):
    for i, panel in self.panels.items():
      panel.init_lights()

  def enlighten(self):
    for pi, panel in self.panels.items():
      for li, light in panel.lights.items():
        pos = (panel.pid, li)
        self.set_square_color_atpos(pos, light.state)

  def set_square_color_atpos(self, pos, state):
    color = "grey"
    if state == 1:
        color = "yellow"
    if state == 0:
        color = "white"
    (y, x) = pos
    self.editwin.addstr(3, 3, 'X')
    #self.editwin.addstr(x, y, 'X')
    self.stdscr.refresh()
