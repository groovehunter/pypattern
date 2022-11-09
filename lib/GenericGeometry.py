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
      #panels[pname] = PanelCoordLights(pid, size=self.num_lights_in_group)
      panels[pid] = PanelCoordLights(pid, size=self.num_lights_in_group)
      pid += 1
    self.panels = OrderedDict(panels)
    print(self.panels)

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
    # gruppentypen: Zwei - ausreichend für vieles?
    # groupA groupB
    # init groups in a row
    nlig = self.num_lights_in_group

    self.groupsA = OrderedDict()
    self.groupsB = OrderedDict()
    for i in range(1, self.num_areas+1):
      self.groupsA[i] = LightGroup(i)
      self.groupsB[i] = LightGroup(i)
      print("init LG A+B # ", i)

    lid = 1 # index flat light array
    for i in range(1, self.num_areas+1):
      for l in range(nlig):
        flat_indexA = i * nlig + l
        flat_indexB = i * nlig + l + int(nlig/2)
        print("i, l: ", i, l)
        if flat_indexA > self.num_lights_total:
          flat_indexA = flat_indexA - self.num_lights_total
        if flat_indexB > self.num_lights_total:
          flat_indexB = flat_indexB - self.num_lights_total
        print("flat_index" , flat_indexA, flat_indexB)
        self.groupsA[i].lights[l] = self.led[flat_indexA]
        self.groupsB[i].lights[l] = self.led[flat_indexB]

    for i, group in self.groupsA.items():
      pass
    print(self.groupsA)
    print(self.groupsB)


  def init_panel_lights(self):
    """ for all panels, call the method to initiate the lights """
    for pname, panel in self.panels.items():
      panel.init_lights()

  def enlighten_flatarray(self):
    """ go through all lights of the board and set the state """
    #print(self.pattern.lights)
    for i, led in self.led.items():
      self.led[i].state = self.pattern.lights[i].state
      # in display superclass
      self.enlight_led(i)

  def enlighten_panel(self):
    """ loop all panels and their lights to set the state """
    # why not loop over self.pattern.panels.items() ?
    for i, panel in self.panels.items():
      c = (panel.pid-1)*self.num_lights_in_group + 1
      #print(panel.lights)
      for i, light in panel.lights.items():
        self.led[c].state = light.state
        self.enlight_led(c)
        c += 1
    #self.show_lightning_leds()

  def show_lightning_leds(self):
    """ debugging output, which leds have ON value """
    white = []
    for i, led in self.led.items():
      if led.pin.value() == 1:
        white.append(led)
    print(white)

  def enlighten(self):
    """ branch different methods according to pattern klass """
    #print(self.pattern.type)
    enligthen_by_panel = [
      'PanelPattern',
      'SynchronousPanelsPattern',
      'FixedStateNumberPattern',
      'ComboPattern',
    ]
    if self.pattern.type in enligthen_by_panel: # etc...
      self.enlighten_panel()
    if self.pattern.type == 'LogicPattern':
      self.enlighten_flatarray()

    self.update_board()
