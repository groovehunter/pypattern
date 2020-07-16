from LightPattern import LightPattern


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
  def state_1(self):
    self.panels['t'].set_pat('o--o')
    self.panels['l'].set_pat('o--o')
  def state_2(self):
    self.panels['t'].set_pat('-oo-')
    self.panels['l'].set_pat('-oo-')
  def state_3(self):
    self.panels['t'].set_pat('o--o')
    self.panels['l'].set_pat('o--o')
  def state_4(self):
    self.state_0()
