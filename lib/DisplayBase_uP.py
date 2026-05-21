# Import all patterns from the new structure
from lib.patterns.flat import *
from lib.patterns.panel import *
from lib.patterns.new import *
from lib.patterns.meta import *
from lib.patterns.group import *

# Keep other necessary imports
# from lib.ComboPattern import * # Obsolete

import random

class DisplayBase:
    pattern_list = [
        # Patterns from flat.py
        'SingleLightCycling',
        'SingleDarkspotCycling',
        'PairedLightsCycling',

        # Patterns from panel.py
        'AlternatingPanels',
        'AllOnOffPattern',
        'RotationPanelPattern',
        'DarkPanelRotationPanelPattern',
        'AddedPanels',

        # Pattern from new.py
        'Chase',

        # Pattern from meta.py
        'ComboPattern',

        # Pattern from group.py
        'AlternatingGroups',
    ]

    # argument, which pattern styles can be used; TODO
    def total_pattern_list(self):
        self.total_patlist = self.pattern_list
        return self.total_patlist

    def set_pattern(self, pat_name, **kwargs):
        # print("setting pattern ", pat_name)
        constructor = globals()[pat_name]
        self.pattern = constructor(self, **kwargs)
        self.pattern.initialize() # Use the new initialize method

    def set_random_pat(self):
        rand = random.choice(self.total_patlist)
        self.set_pattern(rand)
