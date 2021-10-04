## main settings file
import sys
if not sys.platform == 'esp32':
  import os
  ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
  CONFIG_PATH = os.path.join(ROOT_DIR, 'configuration.conf')
else:
  import uos as os
  ROOT_DIR = '/'
  CONFIG_PATH = ROOT_DIR + '/configuration.conf'


boardname = 'triangle3x3'
#boardname = 'square'
#boardname = 'hexagon'
#boardname = 'octagon'


global_conf = {
  'boardname': boardname,
  'size': 300,
  'speed': 50,
}


board_conf = {
  'octagon':
    {
      'num_lights_total': 16,
      'num_areas': 8,
      'num_panels': 8,
      'num_lights_in_group': 2,
      'area_names': ['rtu', 'rtl', 'rbu', 'rbl', 'lbl', 'lbu', 'ltl', 'ltu']
    },

   'hexagon':
    {
      'num_lights_total': 12,
      'num_areas': 6,
      'num_panels': 6,
      'num_lights_in_group': 2,
      'area_names': ['rt', 'rm', 'rb', 'lb', 'lm', 'lt']
    },

    'triangle':
    {
      'num_lights_total': 12,
      'num_areas': 3,
      'num_panels': 3,
      'num_lights_in_group': 4,
      'area_names': ['r', 'b', 'l']
    },

    'triangle3x3':
    {
      'num_lights_total': 9,
      'num_areas': 3,
      'num_panels': 3,
      'num_lights_in_group': 3,
      'area_names': ['r', 'b', 'l']
    },

    'square':
    {
      'num_lights_total': 16,
      'num_areas': 4,
      'num_panels': 4,
      'num_lights_in_group': 4,
      'area_names': ['t', 'r', 'b', 'l']
    },
}
