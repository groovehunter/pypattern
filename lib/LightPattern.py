from lib.Panel import Panel


class LightPattern(object):
  """ Base class for light pattern, basic init methods """

  def __init__(self, board):
    self.board = board
    self.lights = {}
    self.count = 1

  def subclass_init(self):
    raise NotImplementedError
  def initial_state(self):
    raise NotImplementedError
  def next_state(self):
    raise NotImplementedError

  def init_panels_array(self):
    """ method to init another array of panels as attribute of the pattern """
    self.panels = {}
    n = self.board.num_panels
    c = 1
    for i, panel in self.board.panels.items():
      self.panels[c] = panel
      c += 1
    # make endless chain -
    self.panels[n+1] = self.panels[1]
    self.panels[n+2] = self.panels[2]

  def init_pattern_panels(self):
    """ like the boards panels, set also the panels of the pattern
        but indexed with pid number instead of an unused abbr
    """
    n = self.board.num_panels
    #self.panels = {}
    for loc_index, panel in self.board.panels.items():
      #print("subclass_init: panel.pids: ", panel.pid)
      self.panels[panel.pid] = panel
      self.panels[panel.pid].clear()
    self.panels[n+1] = self.panels[1]
    self.panels[n+2] = self.panels[2]
    self.panels[n+3] = self.panels[3]

  def init_light_array_2(self):
    """ simple copy reference to flat light array of board """
    n = self.board.num_lights_total
    for c in range(1, n+1):
      self.lights[c] = self.board.led[c]
    # make endless chain -
    self.lights[n+1] = self.lights[1]
    self.lights[n+2] = self.lights[2]

  def init_light_array(self):
    """ looping the panels, and init like that a flat array of lights """
    self.lights = {}
    c = 1
    # init light array with auto increment index ## MOVE TO BOARD!
    print('init_light_array')
    #print(self.board.panels)
    for p, panel in self.board.panels.items():
      for l, light in panel.lights.items():
        self.lights[c] = light
        c += 1
    n = self.board.num_lights_total
    # make endless chain -
    self.lights[n+1] = self.lights[1]
    self.lights[n+2] = self.lights[2]
    self.count = 0
    #print(self.lights)


  def set_all_panels(self, pat):
    """ legacy method, to set all panels to visual pattern seq """
    for i, panel in self.board.panels.items():
        panel.set_pat(pat)

  def set_panels_to_pat(self, panel_indexes, pat):
    """ legacy method to set a pattern to given list of panels """
    for i in panel_indexes:
      self.board.panels[i].set_pat(pat)

  def all_panels_execute_method(self, method):
    """ run ie. 'clear' or 'full' on all panels """
    for i, panel in self.board.panels.items():
        getattr(panel, method)()
