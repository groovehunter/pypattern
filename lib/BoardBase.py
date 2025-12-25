from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log')

import yaml
from settings import board_conf, global_conf, ROOT_DIR

class BoardBase:
    """ common board stuff,
        especially basic configuration of form and groups
    """

    """
    def __init__(self, **kwargs):
        boardname = kwargs.get('boardname', None)
        self.boardname = boardname
        self.boardcfg = None
        self.cfg = None
        # Initialisiere mit YAML-Konfiguration als Standard
        self.load_yaml_conf()
    """

    def load_py_conf(self):

        self.boardcfg = board_conf[self.boardname]
        self.cfg = global_conf
        self.configure()

    def load_yaml_conf(self):

        with open(ROOT_DIR + '/conf/settings.yaml') as cfgfile:
            cfg = yaml.load(cfgfile, Loader=yaml.Loader)
        self.boardcfg = cfg[self.boardname]
        self.cfg = cfg['global']
        self.configure()

    def configure(self):

        logger.debug('boardcfg', self.boardcfg)
        for attr, val in self.boardcfg.items():
            logger.debug('set board attr %s: %s', attr, val)
            setattr(self, attr, val)


        for attr, val in self.cfg.items():
            logger.debug('set board attr %s: %s', attr, val)
            setattr(self, attr, val)
#    self.init_areas()
#    self.init_groups()

    def init(self):

        """ the main init protocol """
        logger.debug("BoardBase - init start")
        self.init_panels()
        self.init_panel_lights()
        self.init_leds()
        self.init_groups()
        self.subclass_init()

    def subclass_init(self):
        raise NotImplementedError
