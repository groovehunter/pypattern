
from LogicPattern import *
from ExplicitStatesPattern import *
from NextStatePattern import *
#import LogicPattern
#import ExplicitStatesPattern
#import NextStatePattern

import random

class DisplayBase:

  pattern_list = [
'AllOnOff', 
'CyclingPanels',
'Middle_Edge_Cycling',
'PanelsHorizontalVertical',
'SingleLightCycling',
'WindmillPattern',
'AddedPanels',
'DarkPanelRotationPanelPattern',
'RotationPanelPattern',
'SwitchingPanels',
'PairedLightsCycling',
'SingleDarkspotCycling',
'SingleLightCyclingLP',
'AllOnOffPattern',
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
