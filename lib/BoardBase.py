from flowpy.utils import setup_logger
logger = setup_logger(__name__, __name__+'.log')
import yaml
from settings import board_conf, global_conf, ROOT_DIR

class BoardBase:
    """ common board stuff,
        especially basic configuration of form and groups
    """

    def load_py_conf(self):
        self.boardcfg = board_conf[self.boardname]
        self.cfg = global_conf
        self.configure()


    def load_yaml_conf(self):
        cfgfile = open(ROOT_DIR + '/conf/settings.yaml')
        cfg = yaml.load(cfgfile, Loader=yaml.Loader)
        #logger.debug(cfgfile)
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



    def init(self):
        """ the main init protocol """
        logger.debug("BoardBase - init start")
#    self.init_areas()
#    self.init_groups()
        self.init_panels()
        self.init_panel_lights()

        self.init_leds()
        self.init_groups()
        self.subclass_init()

    def subclass_init(self):
        raise NotImplementedError
