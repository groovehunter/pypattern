# Import all patterns from the new structure
from lib.patterns.flat import *
from lib.patterns.panel import *
from lib.patterns.new import *
from lib.patterns.meta import *
from lib.patterns.group import *

try:
    import tkinter.messagebox as messagebox
except Exception:
    # Headless or MicroPython environment: provide a lightweight fallback
    class _StubMsgBox:
        @staticmethod
        def showerror(title, msg):
            try:
                # best effort: print to stderr
                import sys
                print(f"ERROR: {title}: {msg}", file=sys.stderr)
            except Exception:
                pass
    messagebox = _StubMsgBox()

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
        # Try to construct and initialize the selected pattern.
        # Add debug logging for call tracing to help diagnose unexpected changes
        try:
            import traceback
            tb = ''.join(traceback.format_stack(limit=6))
            from flowpy.simplelogger import SimpleLogger
            logger = SimpleLogger(path=__name__ + '.set_pattern.log', level='DEBUG')
            logger.debug(f"set_pattern called: {pat_name}, kwargs={kwargs}\ncallstack:\n{tb}")
        except Exception:
            # best-effort logging, ignore failures
            pass
        try:
            constructor = globals()[pat_name]
        except KeyError:
            try:
                messagebox.showerror('Pattern error', f"Pattern '{pat_name}' not found.")
            except Exception:
                pass
            return False

        try:
            self.pattern = constructor(self, **kwargs)
        except Exception as e:
            try:
                messagebox.showerror('Pattern error', f"Error creating pattern '{pat_name}': {e}")
            except Exception:
                pass
            self.pattern = None
            return False

        # synchronous initialize (guard errors during initialization)
        try:
            self.pattern.initialize()
        except Exception as e:
            try:
                messagebox.showerror('Pattern error', f"Error initializing pattern '{pat_name}': {e}")
            except Exception:
                pass
            self.pattern = None
            return False
        return True

    def set_random_pat(self):
        rand = random.choice(self.total_patlist)
        self.set_pattern(rand)
