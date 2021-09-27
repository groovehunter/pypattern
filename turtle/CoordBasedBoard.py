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
    self.init_panel_lights()
    #self.create_grid()

  def create_grid(self):
    col_outline = "grey"
    color = self.color1
    t = self.t
    t.ht()
#    size = self.boardcfg['size']
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

class SquareBoard(CoordTurtleBoard, GenericGeometry):

  def calc_prepare_coord(self):
    t = self.t
    sz = self.size / 4
    n = 1 # start as lights with 1
    dots = {}
    t.penup()
    t.goto(sz, 0)
    t.pd()
    t.setheading(270)

    for i in range(4):

      for y in range(4):
        dots[n] = t.pos()
        n += 1
        t.fd(sz)
        t.dot(10, self.color)

      t.rt(90)
      t.fd(sz)

    print(dots)
    return dots


class HexagonBoard(CoordTurtleBoard, GenericGeometry):
  """ a board based on coord./turtle """
  color1 = "blue"
  rows = 6
  columns = 6
  size = 200

  def calc_prepare_coord(self):
    t = self.t
    sz = self.size
    n = 1 # start as lights with 1
    dots = {}
    t.penup()
    t.goto(sz, 0)

    t.pd()
    t.setheading(240)
    for i in range(6):
      t.fd(sz*0.3)

      dots[n] = t.pos()
      n += 1

      t.fd(sz*0.4)

      dots[n] = t.pos()
      n += 1

      t.fd(sz*0.3)

      t.rt(60)

    #t.pd()
    return dots
