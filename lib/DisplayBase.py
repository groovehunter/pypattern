#import sys
#from os.path import join
#from settings import ROOT_DIR
import lib.PanelPattern as panelpattern_mod
import lib.LogicPattern as logicpattern_mod
import lib.NextStatePattern as nextstatepattern_mod
import lib.SynchronousPanelsPattern as synchronouspanels_mod
import lib.ComboPattern as combopattern_mod
import inspect
import random
from flowpy.utils import setup_logger
logger = setup_logger(__name__, __name__ + '.log')


def list_pattern_classes(module, base_class=None, exclude=None):
    """
    Liefert alle Klassennamen im Modul, die (optional) von base_class erben und nicht im exclude-Set stehen.
    """
    if exclude is None:
        exclude = set()
    result = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
            if base_class is None or issubclass(obj, base_class):
                if name not in exclude:
                    result.append(name)
    return result

def get_pattern_class_by_name(name):
    for mod in [panelpattern_mod, logicpattern_mod, synchronouspanels_mod, nextstatepattern_mod, combopattern_mod]:
        if hasattr(mod, name):
            return getattr(mod, name)
    raise KeyError(f"Pattern class '{name}' not found in known modules.")


class DisplayBase:
    """ base stuff for a board: setting the pattern, """

    def total_pattern_list(self):
        # Sammle alle Pattern-Klassen aus den relevanten Modulen
        exclude = {'LightPattern', 'NextStatePattern', 'PanelPattern', 'LogicPattern', 'SynchronousPanelsPattern'}
        pattern_names = set()
        # PanelPattern
        pattern_names.update(list_pattern_classes(panelpattern_mod, exclude=exclude))
        # LogicPattern
        pattern_names.update(list_pattern_classes(logicpattern_mod, exclude=exclude))
        # SynchronousPanelsPattern
        pattern_names.update(list_pattern_classes(synchronouspanels_mod, exclude=exclude))
        # NextStatePattern
        pattern_names.update(list_pattern_classes(nextstatepattern_mod, exclude=exclude))
        # ComboPattern (optional, falls gewünscht)
        pattern_names.update(list_pattern_classes(combopattern_mod, exclude=exclude))
        # Sortiert für bessere Übersicht
        self.total_patlist = sorted(pattern_names)
        logger.debug("Available patterns: %s ", self.total_patlist)

    def set_pattern(self, pat_name=None):
        if pat_name is None:
            pat_name = self.variable.get()
        logger.debug('set_pattern: %s', pat_name)
        constructor = get_pattern_class_by_name(pat_name)
        self.pattern = constructor(self.board)
        self.pattern.subclass_init()
        logger.debug('set_pattern')

    def set_random_pat(self):
        rand = random.choice(self.total_patlist)
        self.set_pattern(rand)
