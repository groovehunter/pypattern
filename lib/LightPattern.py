from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')

from lib.Panel import Panel

class LightPattern(object):
    """
    Base class for all light patterns.
    A pattern holds the logic to manipulate the state of lights on a board.
    It does NOT hold the state itself, but operates on the board's lights/panels.
    """
    # 'flat': The pattern manipulates self.board.led directly.
    # 'panel': The pattern manipulates lights within self.board.panels.
    render_mode = 'flat'

    def __init__(self, board):
        logger.debug(f'Initializing {self.__class__.__name__} pattern.')
        self.board = board
        self.count = 0

    def initialize(self):
        """
        Called once after the pattern is created to perform specific initializations
        and to set the very first visual state.
        Subclasses should override this.
        """
        pass

    def next_state(self):
        """
        Calculates and sets the next state of the lights.
        This is the core logic of the pattern, called in a loop.
        """
        raise NotImplementedError

    def clear_all_lights(self):
        """Helper method to turn all lights on the board off."""
        for light in self.board.led.values():
            light.off()

    def clear_all_panels(self):
        """Helper method to clear all panels on the board."""
        for panel in self.board.panels.values():
            panel.clear()

    # --- Legacy Methods (to be reviewed and possibly removed) ---

    def set_all_panels(self, pat):
        """ legacy method, to set all panels to visual pattern seq """
        for i, panel in self.board.panels.items():
            panel.set_pat(pat)

    def set_panels_to_pat(self, panel_indexes, pat):
        """ legacy method to set a pattern to given list of panels """
        for i in panel_indexes:
            self.board.panels[i].set_pat(pat)

    def all_panels_execute_method(self, method):
        """ run ie. 'clear' or 'full' on all panels """
        for i, panel in self.board.panels.items():
            getattr(panel, method)()
