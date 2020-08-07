
import time
import random

from LightPattern import LightPattern
from Panel0 import Panel, Light
from CyclingPattern import *
from DisplayBase import DisplayBase

import RPi.GPIO as GPIO
## mapping light id to gpio port
RaspiMap = {
0: 21,
1: 22,
2:0,
3:0,
4:0,
5:0,
6:0,
7:0,
8:0,
9:0,
10:0,
11:0,
12:0,
13:0,
14:0,
15:0,
}

class RaspiDisplay(DisplayBase):
  def __init__(self):
    self.lights = {}

  def init(self):
    p_list = self.total_pattern_list()
    self.init_panels()
    self.init_panel_lights()

  def init_panels(self):
    self.panels = {
      't' : Panel(),
      'r' : Panel(),
      'b' : Panel(),
      'l' : Panel(),
    }

  def init_panel_lights(self):
      for i, panel in self.panels.items():
          panel.init_lights()

  def enlighten(self):
      for i, panel in self.panels.items():
          for i, light in panel.lights.items():
            self.raspiPin(i)

  def raspiPin(self, i):
    GPIO.output(RaspiMape[i], light.state)



  def run(self):
    while True:
      self.pattern.next_state()
      self.enlighten()
      sleep(1)

"""
    pat_name = p_list[0]
    self.pattern = self.set_pattern(pat_name)
"""
