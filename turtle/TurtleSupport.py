import turtle

class TurtleSupport:
  """ display klass for support of turtle lib """
  def __init__(self):
    self.t = turtle.getturtle()
    self.screen = turtle.getscreen()
    turtle.tracer(0,0)
    self.screen.bgcolor("black")

  def update_board(self):
    turtle.ht()
    turtle.update()

  def enlight_led(self, i):
    pos = self.led[i].position
    self.t.pu()
    self.t.setpos(pos)
    color = "blue"
    if self.led[i].state:
      color = "yellow"
    self.t.pd()
    self.t.dot(30, color)

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
