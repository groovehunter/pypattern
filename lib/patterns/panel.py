from lib.LightPattern import LightPattern

class AlternatingPanels(LightPattern):
    """ Panels with odd and even indices alternate between being on and off. """
    render_mode = 'panel'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.next_state() # Initial state is the first step

    def next_state(self):
        self.count = (self.count + 1) % 2
        
        if self.count == 1: # State 1: Odd on, Even off
            for i in range(1, self.board.num_panels + 1):
                if i % 2 != 0:
                    self.board.panels[i].full()
                else:
                    self.board.panels[i].clear()
        else: # State 0: Even on, Odd off
            for i in range(1, self.board.num_panels + 1):
                if i % 2 == 0:
                    self.board.panels[i].full()
                else:
                    self.board.panels[i].clear()

class AllOnOffPattern(LightPattern):
    """ All panels switch between fully on and fully off. """
    render_mode = 'panel'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.next_state()

    def next_state(self):
        self.count = (self.count + 1) % 2
        if self.count == 1:
            self.all_panels_execute_method('full')
        else:
            self.all_panels_execute_method('clear')

class RotationPanelPattern(LightPattern):
    """ A single lit panel rotates through all available panels. """
    render_mode = 'panel'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.clear_all_panels()
        self.board.panels[1].full()

    def next_state(self):
        self.count += 1
        if self.count > self.board.num_panels:
            self.count = 1
        
        num_panels = self.board.num_panels
        prev_panel_idx = (self.count - 2 + num_panels) % num_panels + 1
        
        self.board.panels[prev_panel_idx].clear()
        self.board.panels[self.count].full()

class DarkPanelRotationPanelPattern(LightPattern):
    """ A single dark panel rotates through an otherwise fully lit board. """
    render_mode = 'panel'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.all_panels_execute_method('full')
        self.board.panels[1].clear()

    def next_state(self):
        self.count += 1
        if self.count > self.board.num_panels:
            self.count = 1

        num_panels = self.board.num_panels
        prev_panel_idx = (self.count - 2 + num_panels) % num_panels + 1

        self.board.panels[prev_panel_idx].full()
        self.board.panels[self.count].clear()

class AddedPanels(LightPattern):
    """ One panel after another is turned on until all are lit, then resets. """
    render_mode = 'panel'

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        self.clear_all_panels()

    def next_state(self):
        self.count += 1
        if self.count > self.board.num_panels:
            self.count = 1
            self.clear_all_panels() # Reset for the next cycle
        
        self.board.panels[self.count].full()

