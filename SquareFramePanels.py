from BoardCanvas import GameBoard
from Panel import Panel


class SquareFramePanels(GameBoard):
  def __init__(self, parent):
    GameBoard.__init__(self, parent)

  def init_panels(self):
    self.panels = {
      't' : Panel(orientation='H'),
      'r' : Panel(orientation='V'),
      'b' : Panel(orientation='H', rev=True),
      'l' : Panel(orientation='V', rev=True),
    }
    # offset is  row, col
    self.panels['t'].offset = (0, 1)
    self.panels['r'].offset = (1, 5)
    self.panels['b'].offset = (5, 4)
    self.panels['l'].offset = (4, 0)

  def mark_panels(self):
    """ draw a black border around the panel """
    col_outline = 'black'
    for i, panel in self.panels.items():
      fac = 4
      (y, x) = panel.offset
      y1 = y * self.size
      x1 = x * self.size
      if panel.orientation == 'H':
        if panel.reverse:
          x1 = (x+1) * self.size
          fac = -4
        x2 = x1 + (fac * self.size)
        y2 = y1 + self.size
      if panel.orientation == 'V':
        if panel.reverse:
          y1 = (y+1) * self.size
          fac = -4
        x2 = x1 + self.size
        y2 = y1 + (fac * self.size)
      self.canvas.create_rectangle(x1, y1, x2, y2,
          outline=col_outline, fill=None, tags="square")


  def mark_light_position(self):
    """ mark all lights, and show them lighting """
    col_outline = "grey"
    color = "yellow"
    for col in range(1, 5):
      x1 = (col * self.size)
      y1 = (0 * self.size)
      x2 = x1 + self.size
      y2 = y1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2,
          outline=col_outline, fill=color, tags="square")

      y1 = (5 * self.size)
      y2 = y1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2,
          outline=col_outline, fill=color, tags="square")

    for row in range(1, 5):
      x1 = (0 * self.size)
      y1 = (row * self.size)
      y2 = y1 + self.size
      x2 = x1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2, outline=col_outline, fill=color, tags="square")

      x1 = (5 * self.size)
      x2 = x1 + self.size
      self.canvas.create_rectangle(x1, y1, x2, y2, outline=col_outline, fill=color, tags="square")
