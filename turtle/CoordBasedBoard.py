#import turtle
from lib.GenericGeometry import GenericGeometry
from lib.BoardBase import BoardBase
from lib.Panel import Panel
from lib.Light import Light, CoordLight
from TurtleSupport import TurtleSupport, TurtleBoard
from time import sleep
import logging

logger = logging.getLogger(__name__)

class CoordSupport:
  """ a board with coordinates for lights and hardware """
  pass

class CoordTurtleBoard(BoardBase, TurtleBoard, CoordSupport):
  """ coordinates (x,y) support, painting with turtle """
  def __init__(self):
    TurtleSupport.__init__(self)

  def subclass_init(self):
    print("subklass_init")
    formklassname = self.boardname.capitalize() + 'Board'
    constructor = globals()[formklassname]
    self.formklass = constructor()
    self.formklass.size = self.cfg['size']
    self.formklass.num_panels = self.num_panels
    self.formklass.num_lights_in_group = self.num_lights_in_group
    self.coords = self.formklass.calc_prepare_coord()
    print(self.coords)

    self.init_leds()

    n = 1
    for i, led in self.led.items():
      led.position = self.coords[n]
      n += 1

    #self.create_grid()

  def init_leds(self):
    """ init flat array of hardware lights """
    led = {}
    for i in range(1, self.num_lights_total+1):
      led[i] = CoordLight(i)
    self.led = led

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

class SquareBoard(TurtleSupport):
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
    return dots

class OctagonBoard(TurtleSupport):
  def calc_prepare_coord(self):
    print("Octagon")
    t = self.t
    sz = self.size
    n = 1 # start as lights with 1
    dots = {}
    t.penup()
    t.goto(sz, 0)
    t.pd()
    t.setheading(240)
    for i in range(8):

      t.fd(sz*0.3)
      dots[n] = t.pos()
      n += 1
      t.fd(sz*0.4)
      dots[n] = t.pos()
      n += 1
      t.fd(sz*0.3)

      t.rt(60)

    #t.pd()
    print(n)
    return dots

class HexagonBoard(TurtleSupport):
  """ a board based on coord./turtle """
  def calc_prepare_coord(self):
    t = self.t
    sz = self.size
    n = 1 # start as lights with 1
    dots = {}
    t.penup()
    t.goto(sz, 0)

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

class TriangleBoard(TurtleSupport):
  def calc_prepare_coord(self):
    size = self.size / 4
    dots = {}
    n = 1
    t = self.t
    t.goto(0, 2*size)
    t.setheading(300)
    for pnr in range(self.num_panels+1):
      t.dot(10, self.color1)
      t.fd(size)
      for lnr in range(self.num_lights_in_group):
        dots[n] = t.pos()
        n += 1
        t.fd(size)

      t.rt(120)

    t.fd(size)
    return dots

class Triangle3x3Board(TurtleSupport):
  def calc_prepare_coord(self):
    size = self.size / 3
    dots = {}
    n = 1
    t = self.t
    t.goto(0, 2*size)
    t.setheading(300)
    for pnr in range(self.num_panels+1):
      t.dot(10, self.color1)
      t.fd(size)
      for lnr in range(self.num_lights_in_group):
        dots[n] = t.pos()
        n += 1
        t.fd(size)

      t.rt(120)

    t.fd(size)
    return dots
