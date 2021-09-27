import turtle

class TurtleSupport:
  """ display klass for support of turtle lib """
  def __init__(self):
    self.t = turtle.getturtle()
    self.screen = turtle.getscreen()
    turtle.tracer(0,0)
    self.screen.bgcolor("black")
    self.color = "blue"

  def update_board(self):
    turtle.ht()
    turtle.update()

  def enlight_led(self, i):
    pos = self.led[i].position
    self.t.pu()
    self.t.setpos(pos)
    color = self.color
    if self.led[i].state:
      color = "yellow"
    self.t.pd()
    self.t.dot(30, color)
