#!/usr/bin/python3
from time import sleep
import turtle
sz = 145

s = turtle.getscreen()
s.colormode(255)

t = turtle.getturtle()
t

def hexagon():
  n = 0
  dots = {}
  t.penup()
  t.goto(sz, 0)
  t.pendown()

  t.setheading(240)
  for i in range(6):
    t.fd(sz/4)
    t.dot(35)
    t.fd(sz/2)
    t.dot(35)
    pos = t.pos()
    dots[n] = pos
    n += 1
    t.fd(sz/4)

#    t.fd(sz)
    t.rt(60)
#    sleep(0.1)
  return dots

b = 0
bstep = 20
while True:
  dots = hexagon()
  b += bstep
  if b > 255: 
    b = 255
    bstep = -bstep
  if b <0:
    b = 0
    bstep = -bstep
   
  rgb = (0, 0, b)
  print(rgb)
  t.pencolor(rgb)
#  sleep(1)
  #t.clear()
  #print(dots)



