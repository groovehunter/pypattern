import sys
from os.path import join
from settings import ROOT_DIR
sys.path.append(join(ROOT_DIR, 'lib'))
import inspect
from LogicPattern import *
from PanelPattern import *
from ExplicitStatesPattern import *
from NextStatePattern import *
from SynchronousPanelsPattern import *
import LogicPattern
import ExplicitStatesPattern
import NextStatePattern
import PanelPattern
import SynchronousPanelsPattern

import random

class DisplayBase:
  """ base stuff for a board: setting the pattern, """
  def get_pattern_classes(self, module):
    """ inspect the file with all the klasses """
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
    OPTIONS += self.get_pattern_classes(SynchronousPanelsPattern)
    OPTIONS += self.get_pattern_classes(NextStatePattern)
    OPTIONS.remove('NextStatePattern')
    OPTIONS.remove('PanelPattern')
    OPTIONS.remove('LogicPattern')
    OPTIONS.remove('SynchronousPanelsPattern')
    OPTIONS.remove('ExplicitStatesPattern')
    self.total_patlist = OPTIONS
    for p in self.total_patlist:
      print("'",p,"', ", sep='')

  def set_pattern(self, pat_name):
    """ XXX move, unify with turtle.board """
    #print("setting pattern ", pat_name)
    constructor = globals()[pat_name]
    self.pattern = constructor(self)

  def set_random_pat(self):
    rand = random.choice(self.total_patlist)
    self.set_pattern(rand)
