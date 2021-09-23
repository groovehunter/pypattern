#import turtle
from lib.GenericGeometry import GenericGeometry
from lib.Panel import Panel
from lib.Light import Light, CoordLight
from TurtleSupport import TurtleSupport
from time import sleep
import logging

logger = logging.getLogger(__name__)

class CoordSupport:
  """ a board with coordinates for lights and hardware """
  pass

class CoordTurtleBoard(TurtleSupport, CoordSupport):
  """ coordinates (x,y) support, painting with turtle """
  def __init__(self):
    TurtleSupport.__init__(self)

  def create_grid(self):
    col_outline = "grey"
    color = self.color1
    t = self.t
    t.ht()
    size = self.size
    for row in range(self.rows):
      for col in range(self.columns):
        x1 = (col * self.size)
        y1 = (row * self.size)
        x2 = x1 + self.size
        y2 = y1 + self.size
        t.penup()
        t.setx(x1)
        t.sety(y1)
        t.pendown()

        for i in range(4):
          t.fd(size)
          t.rt(90)


class HexagonBoard(CoordTurtleBoard, GenericGeometry):
  """ a board based on coord./turtle """
  num_areas = 6
  num_panels = 6
  num_lights_in_group = 2
  color1 = "blue"
  rows = 6
  columns = 6
  size = 200
  area_names = ['t', 'ru', 'rl', 'b', 'll', 'lu']
  num_lights_total = 12


  def init(self):
    self.coords = self.calc_prepare_coord()
    self.panels = {}
    logger.debug(self.coords)
    self.init_leds()
    n = 1
    for i in self.led:
      self.led[i].position = self.coords[n]
      n += 1
#    print(self.led)
    self.init_areas()
    self.init_groups()
    self.init_panels()
    #self.init_panel_lights()
    #self.create_grid()

  def init_panels(self):
    pid = 1
    for pname in self.area_names:
      self.panels[pname] = Panel(pid, size=2)
      self.panels[pname].lights[0] = CoordLight(0)
      self.panels[pname].lights[1] = CoordLight(1)
      pid += 1
      print(self.panels[pname])

#    for i,led in self.led.items():
#      pid = int(i / 2)
#      self.panels[pid].lights[li] = Light(li)


  def enlighten_flatarray(self):
    #print(self.pattern.lights)
    for i, led in self.led.items():
      self.led[i].state = self.pattern.lights[i].state
      # in display superclass
      self.enlight_led(i)

    # in display superclass
    self.update_board()

  def enlighten(self):
    self.enlighten_flatarray()
