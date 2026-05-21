from lib.LightPattern import LightPattern
from lib.patterns.utils import get_pattern_class_by_name

class ComboPattern(LightPattern):
    """
    A meta-pattern that cycles through a list of other patterns.
    Each sub-pattern runs for a specified number of ticks before switching to the next.
    """
    render_mode = 'panel' # Default, can be overridden by sub-patterns.

    def __init__(self, board, pattern_configs, ticks_to_switch=30):
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
        """Loads and initializes the sub-pattern at the current index."""
        if not self.pattern_configs:
            return

        pat_name, kwargs = self.pattern_configs[self.sub_pattern_index]

        try:
            constructor = get_pattern_class_by_name(pat_name, globals())
            self.current_sub_pattern = constructor(self.board, **kwargs)
            self.current_sub_pattern.initialize()
            # Adapt render mode to the current sub-pattern
            self.render_mode = self.current_sub_pattern.render_mode
        except KeyError:
            print(f"Error: Sub-pattern '{pat_name}' not found.")
            self._advance_to_next_sub_pattern() # Skip to the next one
        except Exception as e:
            print(f"Error initializing sub-pattern '{pat_name}': {e}")
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

        # Advance the sub-pattern's state
        self.current_sub_pattern.next_state()

        self.tick_count += 1
        if self.tick_count >= self.ticks_to_switch:
            self._advance_to_next_sub_pattern()
