from LightPattern import LightPattern


class LogicPattern(LightPattern):
    pass

class PanelsHorizontalVertical(LightPattern):
  def __init__(self, board):
    LightPattern.__init__(self, board, states_count=2)

  def state_0(self):
    self.board.panels['t'].set_pat('oooo')
    self.board.panels['b'].set_pat('oooo')
    self.board.panels['r'].set_pat('----')
    self.board.panels['l'].set_pat('----')
  def state_1(self):
    self.board.panels['t'].set_pat('----')
    self.board.panels['b'].set_pat('----')
    self.board.panels['l'].set_pat('oooo')
    self.board.panels['r'].set_pat('oooo')
  def state_2(self):
    self.state_0()


class Middle_Edge_Cycling(LightPattern):
  def __init__(self, board):
    LightPattern.__init__(self, board, states_count=4)

  def define_states(self):
    # vom bisherigen state zum diesem, was sind fuer aenderungen
    # notwendig? Ist ja wie ein programm, transitions quasi
    # also die ganze struktur, die panels durchlaufen
    pass

  def state_0(self):
    self.board.panels['t'].set_pat('-oo-')
    self.board.panels['l'].set_pat('-oo-')
    self.board.panels['r'].set_pat('-oo-')
    self.board.panels['b'].set_pat('-oo-')
  def state_1(self):
    self.board.panels['t'].set_pat('o--o')
    self.board.panels['l'].set_pat('o--o')
    self.board.panels['r'].set_pat('o--o')
    self.board.panels['b'].set_pat('o--o')
  def state_2(self):
    self.state_0()
  def state_3(self):
    self.state_1()
  def state_4(self):
    self.state_0()
