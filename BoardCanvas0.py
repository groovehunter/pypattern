
class GameBoard:
    def __init__(self):
      pass

    def init(self):
        self.init_panels()
        self.init_panel_lights()


    def init_panels(self):
      self.panels = {
        't' : Panel(),
        'r' : Panel(),
        'b' : Panel(),
        'l' : Panel(),
      }

    def init_panel_lights(self):
        for i, panel in self.panels.items():
            panel.init_lights()

    def enlighten(self):
        for i, panel in self.panels.items():
          for i, light in panel.lights.items():
              print(light.states)
