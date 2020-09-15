import inspect
from LogicPattern import *
from CyclingPattern import *
from NextStatePattern import *
import LogicPattern
import CyclingPattern
import NextStatePattern

import random

class DisplayBase:

  def get_pattern_classes(self, module):
    pattern_list = []
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj):
        pattern_list.append(obj.__name__)
    pattern_list.remove('LightPattern')
    return pattern_list

  # argument, which pattern styles can be used; TODO
  def total_pattern_list(self):
      # exlclude cycling for raspi run method
    OPTIONS = []
#    OPTIONS += self.get_pattern_classes(CyclingPattern)
    OPTIONS += self.get_pattern_classes(LogicPattern)
    OPTIONS += self.get_pattern_classes(NextStatePattern)
    OPTIONS.remove('NextStatePattern')
    OPTIONS.remove('LogicPattern')
#    OPTIONS.remove('CyclingPattern')
    #print(OPTIONS)
    self.total_patlist = OPTIONS

  def set_pattern(self, pat_name):
    #print("setting pattern ", pat_name)
    constructor = globals()[pat_name]
    self.pattern = constructor(self)

  def set_random_pat(self):
    rand = random.choice(self.total_patlist)
    self.set_pattern(rand)