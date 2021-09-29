import turtle
from GenericBoard import GenericBoard
from DisplayBase import DisplayBase


class TurtleSupport:
  """ display klass for support of turtle lib """
  color1 = 'blue'
  def __init__(self):
    self.t = turtle.getturtle()
    self.screen = turtle.getscreen()
    turtle.tracer(0,0)
    self.screen.bgcolor("black")
    self.color = "blue"

  def update_board(self):
    #print("TS - update_board")
    turtle.ht()
    turtle.update()


class TurtleBoard(GenericBoard, TurtleSupport, DisplayBase):

  def enlight_led(self, i):
    #print("TS - enlight", i)
    pos = self.led[i].position
    self.t.pu()
    self.t.setpos(pos)
    color = self.color
    if self.led[i].state:
      #print("STATE")
      color = "yellow"
    self.t.pd()
    self.t.dot(30, color)
