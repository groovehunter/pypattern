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
#  num_lights_total = 0
#  num_areas = 0
#  num_panels = 0
#  num_groups_in_area = 0
#  num_lights_in_group = 1
#  area_names = []

  def get_subarea(self):
    pass

  def init_panels(self):
    pid = 1
    panels = {}
    for pname in self.area_names:
      panels[pname] = PanelCoordLights(pid, size=self.num_lights_in_group)
      pid += 1
      print(panels[pname])
    self.panels = OrderedDict(panels)
    print(self.panels)
#    for i,led in self.led.items():
#      pid = int(i / 2)
#      self.panels[pid].lights[li] = Light(li)

  def init_areas(self):
    areas = {}
    for i in range(1, self.num_areas):
      areas[i] = Area()
      areas[i].aid = i
      areas[i].name = self.area_names[i]
    self.areas = areas
    print(self.areas)

  def init_groups(self):
    for ia in range(1, self.num_areas):
      for ig in range(1, self.num_groups_in_area):
        self.areas[ia].groups[ig] = LightGroup(ig)


  def init_panel_lights(self):
    for pname, panel in self.panels.items():
      panel.init_lights()

  def init_leds(self):
    """ init flat array of hardware lights, overwrite in hardware """
    # template for subclasses
    led = {}
    for i in range(1, self.num_lights_total+1):
      # USE HERE suitable Light klass
#      led[i] = LocatedLight(i)
      led[i] = CoordLight(i)
    self.led = led


  def enlighten_flatarray(self):
    #print(self.pattern.lights)
    for i, led in self.led.items():
      self.led[i].state = self.pattern.lights[i].state
      # in display superclass
      self.enlight_led(i)

    # in display superclass resp board subclass
    self.update_board()

  def enlighten(self):
    self.enlighten_flatarray()

  def all_on(self):
    for i, panel in self.panels.items():
      panel.full()
