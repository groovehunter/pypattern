
from LogicPattern import *
from CyclingPattern import *
from NextStatePattern import *
import LogicPattern
import CyclingPattern
import NextStatePattern

import random

class DisplayBase:

  pattern_list = [
    'WindmillPattern',
    'CyclingPanels',
    'PairedLightsCycling',
  ]

  # argument, which pattern styles can be used; TODO
  def total_pattern_list(self):
    self.total_patlist = self.pattern_list
    return self.total_patlist

  def set_pattern(self, pat_name):
    #print("setting pattern ", pat_name)
    constructor = globals()[pat_name]
    self.pattern = constructor(self)

  def set_random_pat(self):
    rand = random.choice(self.total_patlist)
    self.set_pattern(rand)
