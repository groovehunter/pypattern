
class GameBoard:
    def __init__(self, rows=6, columns=6):

        self.rows = rows
        self.columns = columns

    def init(self):
        self.init_panels()
        self.init_panel_lights()

    def init_panel_lights(self):
        for i, panel in self.panels.items():
            panel.init_lights()

    def enlighten(self):
        for i, panel in self.panels.items():
          for i, light in panel.lights.items():
              print(light.states)
