from BoardCanvas import GameBoard
from Panel import Panel

class StackedPanelsSquare(GameBoard):
    def __init__(self, parent):
        GameBoard.__init__(self, parent)

    def init_panels(self):
        self.panels = {
          't' : Panel(orientation='H'),
          'r' : Panel(orientation='H'),
          'b' : Panel(orientation='H'),
          'l' : Panel(orientation='H'),
        }
        # offset is  row, col
        self.panels['t'].offset = (1, 1)
        self.panels['r'].offset = (2, 1)
        self.panels['b'].offset = (3, 1)
        self.panels['l'].offset = (4, 1)

    def mark_light_position(self):
        col_outline = "grey"
        color = "yellow"

        for col in range(1, 5):
            for row in range(1, 5):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2,
                    outline=col_outline, fill=color, tags="square")

    def mark_panels(self):
        for row in range(1, 5):
            x1 = (1 * self.size)
            y1 = (row * self.size)
            x2 = (5 * self.size)
            y2 = y1 + self.size
            self.canvas.create_rectangle(x1, y1, x2, y2,
                outline="black", fill=None, tags="panel")
