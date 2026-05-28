
from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')
from lib.LightPattern import LightPattern
from lib.patterns.utils import get_pattern_class_by_name

class ComboPattern(LightPattern):
    """
    A meta-pattern that cycles through a list of other patterns.
    Each sub-pattern runs for a specified number of ticks before switching to the next.
    """
    render_mode = 'panel' # Default, can be overridden by sub-patterns.

    def __init__(self, board, pattern_configs=None, ticks_to_switch=30):
        """
        Initializes the ComboPattern.
        :param board: The board object.
        :param pattern_configs: A list of tuples, where each tuple contains
                                the pattern name (str) and its kwargs (dict).
                                e.g., [('Chase', {'length': 4}), ('RotationPanelPattern', {})]
        :param ticks_to_switch: The number of `next_state` calls each sub-pattern runs.
        """
        super().__init__(board)
        self.pattern_configs = pattern_configs
        self.ticks_to_switch = ticks_to_switch

        self.sub_pattern_index = 0
        self.tick_count = 0
        self.current_sub_pattern = None

    def _load_sub_pattern(self):
        """Loads and initializes the sub-pattern at the current index.
        This is made robust: pattern_configs may be empty (no-op), and
        the lookup will try the local globals first and then common
        pattern modules under lib.patterns.
        """
        if not self.pattern_configs:
            return

        pat_name, kwargs = self.pattern_configs[self.sub_pattern_index]

        constructor = None
        # First try the provided globals (module-local)
        try:
            constructor = get_pattern_class_by_name(pat_name, globals())
        except KeyError:
            # Try well-known pattern modules
            from importlib import import_module
            for modname in ('lib.patterns.flat', 'lib.patterns.panel', 'lib.patterns.new', 'lib.patterns.group', 'lib.patterns.meta'):
                try:
                    mod = import_module(modname)
                    if hasattr(mod, pat_name):
                        constructor = getattr(mod, pat_name)
                        break
                except Exception:
                    continue

        if constructor is None:
            logger.error("Error: Sub-pattern '%s' not found.", pat_name)
            self._advance_to_next_sub_pattern()
            return

        try:
            self.current_sub_pattern = constructor(self.board, **(kwargs or {}))
            self.current_sub_pattern.initialize()
            # Adapt render mode to the current sub-pattern
            self.render_mode = getattr(self.current_sub_pattern, 'render_mode', self.render_mode)
        except Exception as e:
            logger.error("Error initializing sub-pattern '%s': %s", pat_name, e)
            self._advance_to_next_sub_pattern() # Skip to the next one

    def _advance_to_next_sub_pattern(self):
        """Advances the index to the next pattern in the list, wrapping around."""
        self.sub_pattern_index = (self.sub_pattern_index + 1) % len(self.pattern_configs)
        self.tick_count = 0
        self._load_sub_pattern()

    def initialize(self):
        """Initializes the first sub-pattern."""
        self.sub_pattern_index = 0
        self.tick_count = 0
        self._load_sub_pattern()

    def next_state(self):
        """
        Calls the sub-pattern's next_state and switches to the next sub-pattern
        when the tick counter is reached.
        """
        if not self.current_sub_pattern:
            return
        # Advance the sub-pattern's state (synchronous)
        self.current_sub_pattern.next_state()
        self.tick_count += 1
        if self.tick_count >= self.ticks_to_switch:
            self._advance_to_next_sub_pattern()
