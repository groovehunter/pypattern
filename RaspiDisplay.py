
from  time import sleep
import random

from LightPattern import LightPattern
from Panel0 import Panel, Light
from CyclingPattern import *
from DisplayBase import DisplayBase

import RPi.GPIO as GPIO
## mapping light id to gpio port
RaspiMap = {
1: 19,
2: 26,
3: 13,
4: 6,
5: 11,
6: 10,
7: 5,
8: 9,
9: 12,
10: 20,
11: 21,
12: 16,
13: 7,
14: 24,
15: 25,
16: 8,
}

state_map = {
    1: GPIO.HIGH,
    0: GPIO.LOW,
}

class RaspiDisplay(DisplayBase):
  def __init__(self):
    self.lights = {}
    GPIO.setmode(GPIO.BCM)
    for i, pin in RaspiMap.items():
        GPIO.setup(pin, GPIO.OUT)

  def init(self):
    p_list = self.total_pattern_list()
    self.init_panels()
    self.init_panel_lights()

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
          #print("init panel ", panel)

  def enlighten(self):
    print("pattern: ", self.pattern.__class__)
    for i, panel in self.panels.items():
      print(panel)
      for i, light in panel.lights.items():
        pin_nr = (panel.pid-1) * 4 + i
        self.raspiPin(pin_nr, light.state)

  def raspiPin(self, i, state):
    pin_lvl = state_map[state]
    pin_board = RaspiMap[i+1]
    # print("set bcm pin", pin_board, "to", pin_lvl)
    GPIO.output(pin_board, pin_lvl)

  def test(self):
    for i, panel in self.panels.items():
      panel.full()
    self.enlighten()

  def test_pattern(self):
    while True:
      self.pattern.next_state()
      self.enlighten()
      sleep(5)

  def run(self):
    """ random pattern, but only which use next_state method """
    print(self.pattern)
    while True:
      for ww in range(10):
        self.set_random_pat()
        for one in range(50):
          self.pattern.next_state()
          self.enlighten()
          sleep(1)

"""
    pat_name = p_list[0]
    self.pattern = self.set_pattern(pat_name)
"""
