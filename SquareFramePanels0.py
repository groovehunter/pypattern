from BoardCanvas0 import GameBoard
from Panel0 import Panel


class SquareFramePanels0(GameBoard):
  def __init__(self):
    GameBoard.__init__(self)

  def init_panels(self):
    self.panels = {
      't' : Panel(),
      'r' : Panel(),
      'b' : Panel(),
      'l' : Panel(),
    }
