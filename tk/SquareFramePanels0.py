from tk.BoardCanvasGeneric import GameBoardGeneric
from tk.TkPanel0 import TkPanel
from lib.GenericGeometry import GenericGeometry
#from lib.Light import LocatedLight
import yaml
import os

class SquareFramePanels(GameBoardGeneric, GenericGeometry):
  """ geometry is here 4 bars/panels in a square """
  num_areas = 4
  num_groups_in_area = 1
  num_lights_in_group = 4
  area_names = ['t', 'r', 'b', 'l']

  def __init__(self, parent):
    GameBoardGeneric.__init__(self, parent, rows=6, columns=6)
    #self.init_areas()
    self.init_leds()
    self.num_panels = 4
    self.num_lights_total = 16

  def enlighten(self):
    super().enlighten_flatarray()

  def set_groups_in_areas(self):
    for name in self.area_names:
      #self
      pass

  def init_panels_yaml(self):
#    print(os.path.dirname((__file__)))
    cfg_file = os.path.dirname(__file__) + '/panels.yaml'
    cfg = open(cfg_file, 'r')
    panels = yaml.load(cfg) #, Loader=yaml.SafeLoader())
    i = 1
    for panel in panels:
        for num in range(1, 5):
#          self.get_coord_of_light_nr(lid, offset[pid], orientation, reverse)
          (row, col) = panel['offset']
          add = 1
          if panel['reverse']:
            add = -1
          if panel['orientation'] == 'H':
            self.led[i].position = (row, col + num*add)
          if panel['orientation'] == 'V':
            self.led[i].position = (row + num*add, col)
          i += 1

  def mark_panels(self):
    """ draw a black border around the panel """
    col_outline = 'black'
    for i, panel in self.panels.items():
      fac = 4
      (y, x) = panel.offset
      y1 = y * self.size
      x1 = x * self.size
      if panel.orientation == 'H':
        if panel.reverse:
          x1 = (x+1) * self.size
          fac = -4
        x2 = x1 + (fac * self.size)
        y2 = y1 + self.size
      if panel.orientation == 'V':
        if panel.reverse:
          y1 = (y+1) * self.size
          fac = -4
        x2 = x1 + self.size
        y2 = y1 + (fac * self.size)
      self.canvas.create_rectangle(x1, y1, x2, y2,
          outline=col_outline, fill=None, tags="square")


  def mark_light_position(self):
    """ mark all lights, and show them lighting """
    col_outline = "grey"
    color = "yellow"
    for col in range(1, 5):
      x1 = (col * self.size)
      y1 = (0 * self.size)
      x2 = x1 + self.size
      y2 = y1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2,
          outline=col_outline, fill=color, tags="square")

      y1 = (5 * self.size)
      y2 = y1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2,
          outline=col_outline, fill=color, tags="square")

    for row in range(1, 5):
      x1 = (0 * self.size)
      y1 = (row * self.size)
      y2 = y1 + self.size
      x2 = x1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2, outline=col_outline, fill=color, tags="square")

      x1 = (5 * self.size)
      x2 = x1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2, outline=col_outline, fill=color, tags="square")
