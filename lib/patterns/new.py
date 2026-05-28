from lib.LightPattern import LightPattern

class Chase(LightPattern):
    """
    A new pattern: A "comet" of a specific length chases its tail.
    This is a flat pattern.
    """
    render_mode = 'flat'

    def __init__(self, board, length=3, **kwargs):
        super().__init__(board)
        self.length = max(1, length)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.clear_all_lights()
        # Light up the initial comet (prefer logical lights)
        for i in range(1, self.length + 1):
            try:
                self.light_on(i)
            except Exception:
                pass

    def next_state(self):
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1

        num_lights = self.board.num_lights_total

        # Index of the new head of the comet
        head_idx = (self.count + self.length - 2) % num_lights + 1

        # Index of the tail to be turned off
        tail_idx = (self.count - 1 + num_lights -1) % num_lights + 1

        try:
            self.light_off(tail_idx)
        except Exception:
            pass
        try:
            self.light_on(head_idx)
        except Exception:
            pass
