
import time
import random

from LightPattern import LightPattern
from Panel import Light
from CyclingPattern import *

led_pin = 9
from board import Base


class LED(Light):
  """ verknuepft mit LIght klasse
  """
  def __init__(self, pin):
    self.pin = pin

class RaspiBoard:
  def __init__(self):
    pass
  def next_state(self, event):
    self.pattern.next_state()
    self.change_board()

  def change_board(self):
    self.board.enlighten()



class RaspiDisplay(Base):
  """ make pattern of pattern controller visible on 16 LED pins
      Das board mit 6x6 grid, die konfigur.Panel anordnungen
      etc, alles als GameBoard hier ablegen, member var?

  """

  def __init__(self):
    self.leds = {}
    self.board = RaspiBoard()


  def init(self):

    for i in range(9,10):
      self.leds[i] = LED(i)

    p_list = self.get_pattern_classes()
    rand = random.Random()
    pat_name = rand.choice(p_list)
    self.pattern = self.set_pattern(pat_name)

  def set_pattern(self, pat_name):
    constructor = globals()[pat_name]
    self.pattern = constructor(self.board)
    self.pattern.initial_state()


  def init_panel_lights(self):
      for i, panel in self.panels.items():
          panel.init_lights()

  def enlighten(self):
      for i, panel in self.panels.items():
          for i, light in panel.lights.items():
              self.set_square_color_atpos(light.position, light.state)

  def run(self):
    #self.init()

    while True:
      rand = random.Random()
      pin = rand.choice((9,10))
      space = ""
      if pin == 9:
        pin2=10
      if pin == 10:
        pin2=9
        space = "\t"
      print("RANDOM PIN: %s %i" %(space, pin))
      self.board.digital[pin].write(1)
      self.board.digital[pin2].write(0)

      time.sleep(0.05)


  def blink(self, pin):
    board.digital[pin].write(0)
    time.sleep(1)
    board.digital[pin].write(1)
    time.sleep(1)






if __name__ == "__main__":
  pcd = RaspiDisplay()
  #pcd.init()
  pcd.run()
