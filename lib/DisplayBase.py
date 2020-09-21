import sys
from os.path import join
from settings import ROOT_DIR
sys.path.append(join(ROOT_DIR, 'lib'))
import inspect
from LogicPattern import *
from PanelPattern import *
#from ExplicitStatesPattern import *
#from NextStatePattern import *
import LogicPattern
import ExplicitStatesPattern
import NextStatePattern
import PanelPattern

import random

class DisplayBase:

  def get_pattern_classes(self, module):
    pattern_list = []
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj):
        #print(name, obj)
        pattern_list.append(obj.__name__)
    if 'LightPattern' in pattern_list:
        pattern_list.remove('LightPattern')
    return pattern_list

  # argument, which pattern styles can be used; TODO
  # rename to get_total.... # TODO:
  def total_pattern_list(self):
    OPTIONS = []
    OPTIONS += self.get_pattern_classes(ExplicitStatesPattern)
    OPTIONS += self.get_pattern_classes(PanelPattern)
    OPTIONS += self.get_pattern_classes(LogicPattern)
    OPTIONS += self.get_pattern_classes(NextStatePattern)
    OPTIONS.remove('NextStatePattern')
    OPTIONS.remove('PanelPattern')
    OPTIONS.remove('LogicPattern')
    OPTIONS.remove('ExplicitStatesPattern')
    self.total_patlist = OPTIONS

  def set_pattern(self, pat_name):
    #print("setting pattern ", pat_name)
    constructor = globals()[pat_name]
    self.pattern = constructor(self)

  def set_random_pat(self):
    rand = random.choice(self.total_patlist)
    self.set_pattern(rand)
