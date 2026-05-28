from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')
from lib.LightPattern import LightPattern

class SingleLightCycling(LightPattern):
    """ A single lit light rotates through all available lights. """
    render_mode = 'flat'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.clear_all_lights()
        # turn on first light (prefer logical lights)
        self.light_on(1)

    def next_state(self):
        logger.debug(f"SingleLightCycling.next_state: count={self.count}")
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1
        num_lights = self.board.num_lights_total
        prev_light_idx = (self.count - 2 + num_lights) % num_lights + 1
        logger.debug(f"SingleLightCycling: prev_light_idx={prev_light_idx}, new_light_idx={self.count}")
        self.light_off(prev_light_idx)
        self.light_on(self.count)
        # synchronous pattern step

class SingleDarkspotCycling(LightPattern):
    """ A single dark spot rotates through an otherwise fully lit board. """
    render_mode = 'flat'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        # turn all on, then darken first
        if hasattr(self.board, 'logic_lights') and self.board.logic_lights:
            for lid in self.board.logic_lights:
                self.light_on(lid)
        else:
            for lid in list(self.board.led.keys()):
                self.light_on(lid)
        self.light_off(1)

    def next_state(self):
        logger.debug(f"SingleDarkspotCycling.next_state: count={self.count}")
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1
        num_lights = self.board.num_lights_total
        prev_light_idx = (self.count - 2 + num_lights) % num_lights + 1
        logger.debug(f"SingleDarkspotCycling: prev_light_idx={prev_light_idx}, dark_light_idx={self.count}")
        self.light_on(prev_light_idx)
        self.light_off(self.count)
        # synchronous pattern step

class PairedLightsCycling(LightPattern):
    """ Two adjacent lights rotate through all available lights. """
    render_mode = 'flat'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.clear_all_lights()
        self.light_on(1)
        self.light_on(2)

    def next_state(self):
        logger.debug(f"PairedLightsCycling.next_state: count={self.count}")
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1
        num_lights = self.board.num_lights_total
        prev_trail_idx = (self.count - 2 + num_lights) % num_lights + 1
        logger.debug(f"PairedLightsCycling: prev_trail_idx={prev_trail_idx}")
        self.light_off(prev_trail_idx)
        new_lead_idx = (self.count % num_lights) + 1
        logger.debug(f"PairedLightsCycling: new_lead_idx={new_lead_idx}")
        self.light_on(new_lead_idx)
        # synchronous pattern step
