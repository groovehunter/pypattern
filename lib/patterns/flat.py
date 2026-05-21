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
        self.board.led[1].on()

    def next_state(self):
        logger.debug(f"SingleLightCycling.next_state: count={self.count}")
        print(f"SingleLightCycling.next_state: count={self.count}")
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1
        num_lights = self.board.num_lights_total
        prev_light_idx = (self.count - 2 + num_lights) % num_lights + 1
        logger.debug(f"SingleLightCycling: prev_light_idx={prev_light_idx}, new_light_idx={self.count}")
        print(f"SingleLightCycling: prev_light_idx={prev_light_idx}, new_light_idx={self.count}")
        self.board.led[prev_light_idx].off()
        self.board.led[self.count].on()

class SingleDarkspotCycling(LightPattern):
    """ A single dark spot rotates through an otherwise fully lit board. """
    render_mode = 'flat'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        for light in self.board.led.values():
            light.on()
        self.board.led[1].off()

    def next_state(self):
        logger.debug(f"SingleDarkspotCycling.next_state: count={self.count}")
        print(f"SingleDarkspotCycling.next_state: count={self.count}")
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1
        num_lights = self.board.num_lights_total
        prev_light_idx = (self.count - 2 + num_lights) % num_lights + 1
        logger.debug(f"SingleDarkspotCycling: prev_light_idx={prev_light_idx}, dark_light_idx={self.count}")
        print(f"SingleDarkspotCycling: prev_light_idx={prev_light_idx}, dark_light_idx={self.count}")
        self.board.led[prev_light_idx].on()
        self.board.led[self.count].off()

class PairedLightsCycling(LightPattern):
    """ Two adjacent lights rotate through all available lights. """
    render_mode = 'flat'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.clear_all_lights()
        self.board.led[1].on()
        self.board.led[2].on()

    def next_state(self):
        logger.debug(f"PairedLightsCycling.next_state: count={self.count}")
        print(f"PairedLightsCycling.next_state: count={self.count}")
        self.count += 1
        if self.count > self.board.num_lights_total:
            self.count = 1
        num_lights = self.board.num_lights_total
        prev_trail_idx = (self.count - 2 + num_lights) % num_lights + 1
        logger.debug(f"PairedLightsCycling: prev_trail_idx={prev_trail_idx}")
        print(f"PairedLightsCycling: prev_trail_idx={prev_trail_idx}")
        self.board.led[prev_trail_idx].off()
        new_lead_idx = (self.count % num_lights) + 1
        logger.debug(f"PairedLightsCycling: new_lead_idx={new_lead_idx}")
        print(f"PairedLightsCycling: new_lead_idx={new_lead_idx}")
        self.board.led[new_lead_idx].on()

