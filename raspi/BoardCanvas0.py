from Panel0 import Panel


class GameBoard:
    def __init__(self):
      pass

    def init(self):
        self.init_panels()
        self.init_panel_lights()


    def init_panels(self):
      self.panels = {
        't' : Panel(1),
        'r' : Panel(2),
        'b' : Panel(3),
        'l' : Panel(4),
      }

    def init_panel_lights(self):
        for i, panel in self.panels.items():
            panel.init_lights()

    def enlighten(self):
        for i, panel in self.panels.items():
          for i, light in panel.lights.items():
              print(light.state)
