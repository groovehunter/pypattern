import inspect
from LogicPattern import *
from CyclingPattern import *
from NextStatePattern import *
import LogicPattern
import CyclingPattern
import NextStatePattern


class DisplayBase:

  def get_pattern_classes(self, module):
    pattern_list = []
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj):
        pattern_list.append(obj.__name__)
    pattern_list.remove('LightPattern')
    return pattern_list

  def total_pattern_list(self):
    OPTIONS = self.get_pattern_classes(CyclingPattern)
    OPTIONS += self.get_pattern_classes(LogicPattern)
    OPTIONS += self.get_pattern_classes(NextStatePattern)
    return OPTIONS

  def set_pattern(self, pat_name):
    constructor = globals()[pat_name]
    self.pattern = constructor(self)
