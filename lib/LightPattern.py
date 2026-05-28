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
        """Helper method to turn all lights on the board off.
        Preferentially operates on logical lights (`board.logic_lights`) if present;
        otherwise falls back to hardware lights (`board.led`).
        """
        if hasattr(self.board, 'logic_lights') and self.board.logic_lights:
            for light in self.board.logic_lights.values():
                try:
                    light.off()
                except Exception:
                    pass
        else:
            for light in getattr(self.board, 'led', {}).values():
                try:
                    light.off()
                except Exception:
                    pass

    def _get_light_obj(self, lid):
        """Return the logical light if available, otherwise the hardware light.
        Raises KeyError if no light found.
        """
        if hasattr(self.board, 'logic_lights') and self.board.logic_lights:
            if lid in self.board.logic_lights:
                return self.board.logic_lights[lid]
        if hasattr(self.board, 'led') and self.board.led:
            if lid in self.board.led:
                return self.board.led[lid]
        raise KeyError(f'Light {lid} not found')

    def light_on(self, lid):
        """Turn a single light on (logical preferred)."""
        try:
            self._get_light_obj(lid).on()
        except Exception:
            pass

    def light_off(self, lid):
        """Turn a single light off (logical preferred)."""
        try:
            self._get_light_obj(lid).off()
        except Exception:
            pass

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
