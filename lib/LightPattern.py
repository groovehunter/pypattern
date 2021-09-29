from lib.Panel import Panel


class LightPattern(object):

  def __init__(self, board):
    #self.states_count = states_count
    self.board = board
    self.states_count = self.board.num_panels
    self.lights = {}
    self.states = []
    self.count = 1
#    self.subclass_init()   # board.led not ready
    self.uptime = 0

  def subclass_init(self):
    raise NotImplementedError

  def next_state(self):
    raise NotImplementedError

  def init_light_array_2(self):
    """ simple copy reference to flat light array of board """
    n = self.board.num_lights_total
    for c in range(1, n+1):
      #print(c)
      self.lights[c] = self.board.led[c]
    # make endless chain -
#    self.lights[n] = self.lights[0]
    self.lights[n+1] = self.lights[1]
    self.lights[n+2] = self.lights[2]
    #print(self.lights)

  def init_light_array(self):
    """ looping the panels """
    self.lights = {}
    c = 1
    # init light array with auto increment index ## MOVE TO BOARD!
    print('init_light_array')
    print(self.board.panels)
    for p, panel in self.board.panels.items():
      for l, light in panel.lights.items():
        self.lights[c] = light
        c += 1
    n = self.board.num_lights_total
    # make endless chain -
    print(self.lights)
    self.lights[n+1] = self.lights[1]
    self.lights[n+2] = self.lights[2]
    self.count = 0
    print(self.lights)


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
