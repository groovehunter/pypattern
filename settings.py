## main settings file
import sys
try:
    is_micropython = sys.implementation[0] == 'micropython'
except Exception:
    is_micropython = False

if sys.platform == 'esp32' or is_micropython:
    import uos as os
    ROOT_DIR = '/'
    CONFIG_PATH = ROOT_DIR + '/configuration.conf'
else:
    import os
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'configuration.conf')

#boardname = 'square'
#boardname = 'square_4x2'
#boardname = 'square_4x8'
# uses qq pins 22+23;
#boardname = 'hexagon_qq'
# avoid rx and tx pins
boardname = 'hexagon_rxtx'
#boardname = 'hexagon_single'
#boardname = 'test'
#boardname = 'octagon'


global_conf = {
    'boardname': boardname,
    'size': 300,
    'speed': 500,
}

board_conf = {
    'test': {
        'num_lights_total': 16,
        'num_areas': 2,
        'num_panels': 2,
        'num_lights_in_group': 8,
        'area_names': ['r', 'l']
    },
    'octagon': {
        'num_lights_total': 16,
        'num_areas': 8,
        'num_panels': 8,
        'num_lights_in_group': 2,
        'area_names': ['rtu', 'rtl', 'rbu', 'rbl', 'lbl', 'lbu', 'ltl', 'ltu']
    },
    'hexagon_qq': {
        'num_lights_total': 12,
        'num_areas': 6,
        'num_panels': 6,
        'num_lights_in_group': 2,
        'area_names': ['rt', 'rm', 'rb', 'lb', 'lm', 'lt']
    },
    'hexagon_rxtx': {
        'num_lights_total': 12,
        'num_areas': 6,
        'num_panels': 6,
        'num_lights_in_group': 2,
        'area_names': ['rt', 'rm', 'rb', 'lb', 'lm', 'lt']
    },
    'hexagon_single': {
        'num_lights_total': 6,
        'num_areas': 6,
        'num_panels': 6,
        'num_lights_in_group': 1,
        'area_names': ['rt', 'rm', 'rb', 'lb', 'lm', 'lt']
    },
    'triangle': {
        'num_lights_total': 12,
        'num_areas': 3,
        'num_panels': 3,
        'num_lights_in_group': 4,
        'area_names': ['r', 'b', 'l']
    },
    'triangle_3x3': {
        'num_lights_total': 9,
        'num_areas': 3,
        'num_panels': 3,
        'num_lights_in_group': 3,
        'area_names': ['r', 'b', 'l']
    },
    'square4x1': {
        'num_lights_total': 4,
        'num_areas': 4,
        'num_panels': 4,
        'num_lights_in_group': 1,
        'area_names': ['t', 'r', 'b', 'l']
    },
    'square4x2': {
        'num_lights_total': 8,
        'num_areas': 4,
        'num_panels': 4,
        'num_lights_in_group': 2,
        'area_names': ['t', 'r', 'b', 'l']
    },
    'square': {
        'num_lights_total': 16,
        'num_areas': 4,
        'num_panels': 4,
        'num_lights_in_group': 4,
        'area_names': ['t', 'r', 'b', 'l']
    },
    'square_4x8': {
        'num_lights_total': 32,
        'num_areas': 4,
        'num_panels': 4,
        'num_lights_in_group': 8,
        'area_names': ['t', 'r', 'b', 'l']
    },
}
