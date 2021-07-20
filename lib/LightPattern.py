from lib.Panel import Panel


class LightPattern(object):
  states_count = 4
  def __init__(self, board):
#    self.states_count = states_count
    self.states = []
    self.count = 1
    self.board = board
    self.subclass_init()
    self.uptime = 0

  def subclass_init(self):
    raise NotImplementedError

  def next_state(self):
    raise NotImplementedError

  def init_light_array(self):
    """
    # tests without panels:
    for p in range(0, 4):
      for l in range(0, 4):
        self.lights[c] = Light(c)
        c += 1
    """

    self.lights = {}
    c = 0
    # init light array with auto increment index
    for p, panel in self.board.panels.items():
      for l, light in panel.lights.items():
        self.lights[c] = light
        c += 1
    self.lights[16] = self.lights[0]
    self.lights[17] = self.lights[1]
    self.lights[18] = self.lights[2]
    self.count = 0


  def set_all_panels(self, pat):
    for i, panel in self.board.panels.items():
        panel.set_pat(pat)

  def set_panels_to_pat(self, panel_indexes, pat):
    for i in panel_indexes:
      self.board.panels[i].set_pat(pat)

  def all_panels_execute_method(self, method):
    """ run ie. 'clear' or 'full' on all panels """
    for i, panel in self.board.panels.items():
        getattr(panel, method)()
