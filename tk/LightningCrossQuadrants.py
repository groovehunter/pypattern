from lib.LightGroup import LightGroup
from lib.Light import LocatedLight
from lib.GenericGeometry import GenericGeometry

from tk.BoardCanvasGeneric import GameBoardGeneric
import yaml, os

class LightningCrossQuadrants(GameBoardGeneric, GenericGeometry):
  """ board subclass for cross with quadrants, lights in the
      center, this was tested first with generic geometry approach """
  num_areas = 4
  num_groups_in_areas = 4
  area_names = ['UL', 'UR', 'LL', 'LR']

# yaml config of areas and groups and their positions, offsets
  def __init__(self, parent):
    GameBoardGeneric.__init__(self, parent)
    # material locations, init material
    # slots for lights
    # generic: all lights independent from panels, groups, bars
#    self.init_areas()
#    self.init_groups()
    self.init_leds()
    self.init_panels()

  def enlighten(self):
    """ link to superclass enlighten """
    super().enlighten_flatarray()

  def init_leds(self):
    """ init flat array of hardware lights """
    led = {}
    for i in range(1, 17):
      led[i] = LocatedLight(i)
    self.led = led

  def init_panels(self):
    """ set attributes of lights (was: panels), ie position
        all from yaml config file """
    cfg_file = os.path.dirname(__file__) + '/panels00.yaml'
    cfg = open(cfg_file, 'r')
    lights = yaml.load(cfg) #, Loader=yaml.SafeLoader())
    i = 1
    num = 0
    for item in lights:
      # for panels00.yaml
      (area, od, pos) = item.split('_')
      name = area
      offset = eval(pos)
      orientation = od[0]
      reverse = False
      """
      # for panels0.yaml
      reverse = item.get('reverse', False)
      name    = item.get('name', '')
      orientation = item.get('orientation', 'H')
      offset  = item.get('offset', [0,0])
      """
      (row, col) = offset
      print(name, row, col)
      if not name:
        name = "%s_%s_%s".format(offset, orientation, reverse)
      add = 1
      if reverse:
        add = -1
      if orientation == 'h':
        self.led[i].position = (row, col + num*add)
      if orientation == 'v':
        self.led[i].position = (row + num*add, col)
      i += 1

