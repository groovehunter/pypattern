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


boardname = 'hexagon'

global_conf = {
  'boardname': 'hexagon',
  'size': 100,
}


board_conf = {
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
    'square':
    {
      'num_lights_total': 16,
      'num_areas': 4,
      'num_panels': 4,
      'num_lights_in_group': 4,
      'area_names': ['t', 'r', 'b', 'l']
    },
}
