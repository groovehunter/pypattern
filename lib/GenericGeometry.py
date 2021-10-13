import sys
from lib.LightGroup import LightGroup
from lib.Area import Area
from lib.Light import LocatedLight, CoordLight
from lib.Panel import Panel, PanelCoordLights

if sys.platform == 'esp32':
  from ucollections import OrderedDict
else:
  from collections import OrderedDict

class GenericGeometry:
  """ a spatial hierarchy """

  def init_leds(self):
    """ overwrite in subclass, use adequate display Light klass """
    raise NotImplementedError

  def init_panels(self):
    """ init a OrderedDict of Panels """
    pid = 1
    panels = {}
    for pname in self.area_names:
      panels[pname] = PanelCoordLights(pid, size=self.num_lights_in_group)
      pid += 1
    self.panels = OrderedDict(panels)

  def init_areas(self):
    """ init a dict of Areas (like Panels) - UNUSED """
    areas = {}
    for i in range(1, self.num_areas):
      areas[i] = Area()
      areas[i].aid = i
      areas[i].name = self.area_names[i]
    self.areas = areas

  def init_groups(self):
    """ initiate ares in groups """
    for ia in range(1, self.num_areas):
      for ig in range(1, self.num_groups_in_area):
        self.areas[ia].groups[ig] = LightGroup(ig)

  def init_panel_lights(self):
    """ for all panels, call the method to initiate the lights """
    for pname, panel in self.panels.items():
      panel.init_lights()

  def init_leds(self):
    """ init flat array of hardware lights, overwrite in hardware """
    raise NotImplementedError

  def enlighten_flatarray(self):
    """ go through all lights of the board and set the state """
    #print(self.pattern.lights)
    for i, led in self.led.items():
      self.led[i].state = self.pattern.lights[i].state
      # in display superclass
      self.enlight_led(i)

  def enlighten_panel(self):
    """ loop all panels and their lights to set the state """
    for i, panel in self.panels.items():
      c = (panel.pid-1)*self.num_lights_in_group + 1
      #print(panel.lights)
      for i, light in panel.lights.items():
        self.led[c].state = light.state
        self.enlight_led(c)
        c += 1

  def enlighten(self):
    """ branch different methods according to pattern klass """
    #print(self.pattern.type)
    enligthen_by_panel = [
      'PanelPattern',
      'SynchronousPanelsPattern',
      'FixedStateNumberPattern',
    ]
    if self.pattern.type in enligthen_by_panel: # etc...
      self.enlighten_panel()
    if self.pattern.type == 'LogicPattern':
      self.enlighten_flatarray()

    self.update_board()

  def all_on(self):
    """ set all panels to full lights """
    for i, panel in self.panels.items():
      panel.full()
