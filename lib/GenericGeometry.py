
from lib.LightGroup import LightGroup
from lib.Area import Area
from lib.Light import LocatedLight, CoordLight


class GenericGeometry:
  """ a spatial hierarchy """
  num_areas = 0
  num_groups_in_area = 0
  num_lights_in_group = 1

  def get_subarea(self):
    pass

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

  def init_leds(self):
    """ init flat array of hardware lights """
    led = {}
    for i in range(1, self.num_lights_total+1):
#      led[i] = LocatedLight(i)
      led[i] = CoordLight(i)
    self.led = led
