#import yaml
from settings import board_conf, global_conf, ROOT_DIR
from GenericGeometry import GenericGeometry
from DisplayBase_uP import DisplayBase

class BoardBase:
  """ common board stuff,
      especially basic configuration of form and groups
  """

  def load_py_conf(self):
    self.boardcfg = board_conf[self.boardname]
    self.cfg = global_conf
    self.configure()


  def load_yaml_conf(self):
    cfgfile = open(ROOT_DIR+ '/conf/settings.yaml')
    cfg = yaml.load(cfgfile)
    print(cfgfile)
    self.boardcfg = cfg[self.boardname]
    self.cfg = cfg['global']

    self.configure()

  def configure(self):
    print(self.boardcfg)
    for attr, val in self.boardcfg.items():
      setattr(self, attr, val)
    print(self.num_lights_total)

    for attr, val in self.cfg.items():
      print(attr, val)
      setattr(self, attr, val)

  def init(self):
    """ the main init protocol """
    print("BoardBase - init start")
#    self.init_areas()
#    self.init_groups()
    self.init_panels()
    self.init_panel_lights()

    self.init_leds()
    self.subclass_init()

  def subclass_init(self):
    raise NotImplementedError
