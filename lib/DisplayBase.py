# Import all patterns from the new structure
from lib.patterns.flat import *
from lib.patterns.panel import *
from lib.patterns.new import *
from lib.patterns.meta import *
from lib.patterns.group import *
from lib.patterns.utils import *

import random
from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')


class DisplayBase:
    """
    Base class for the CPython display environment.
    Handles pattern loading and switching.
    """

    def __init__(self):
        self.pattern_list = [
            # This list should ideally be the same as in DisplayBase_uP
            'SingleLightCycling', 'SingleDarkspotCycling', 'PairedLightsCycling',
            'AlternatingPanels', 'AllOnOffPattern', 'RotationPanelPattern',
            'DarkPanelRotationPanelPattern', 'AddedPanels', 'Chase',
            'ComboPattern', 'AlternatingGroups'
        ]
        self.total_patlist = self.pattern_list
        self.pattern = None
        # This is used by the Tkinter GUI, needs to be handled gracefully
        self.variable = None

    def total_pattern_list(self):
        # This method is now simpler as the list is predefined.
        logger.debug("Available patterns: %s ", self.total_patlist)
        return self.total_patlist

    def set_pattern(self, pat_name=None, **kwargs):
        if pat_name is None and self.variable:
             pat_name = self.variable.get()

        if not pat_name:
            logger.warning("set_pattern called with no pattern name.")
            return

        logger.debug('set_pattern: %s with args %s', pat_name, kwargs)
        try:
            # The board object is passed to the pattern constructor.
            # In the CPython context, `self` is the DisplayBase, but the pattern expects the board.
            # This assumes DisplayBase is mixed into the board class (e.g., GenericBoard).
            board_instance = self
            constructor = get_pattern_class_by_name(pat_name, globals())
            self.pattern = constructor(board_instance, **kwargs)
            self.pattern.initialize()
            logger.debug('Pattern %s initialized.', pat_name)
        except KeyError as e:
            logger.error(e)
        except Exception as e:
            logger.error("Failed to set pattern '%s': %s", pat_name, e)

    def set_random_pat(self):
        if not self.total_patlist:
            logger.warning("Cannot set random pattern, list is empty.")
            return
        rand = random.choice(self.total_patlist)
        self.set_pattern(rand)