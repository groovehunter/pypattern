from LightPattern import LightPattern


class CyclingPanels(LightPattern):
  def state_0(self):
    self.board.panels['t'].full()
    self.set_panels_to_pat('rbl', '----')
  def state_1(self):
    self.board.panels['r'].full()
    self.set_panels_to_pat('tbl', '----')
  def state_2(self):
    self.board.panels['b'].full()
    self.set_panels_to_pat('trl', '----')
  def state_3(self):
    self.board.panels['l'].full()
    self.set_panels_to_pat('trb', '----')
  def state_4(self):
    self.state_0()

class LogicPattern(LightPattern):
  def __init__(self, board):
    LightPattern.__init__(self, board, states_count=4)
  def state_0(self):
    self.set_all_panels('o---')
  def state_1(self):
    self.set_all_panels('-o--')
  def state_2(self):
    self.set_all_panels('--o-')
  def state_3(self):
    self.set_all_panels('---o')
  def state_4(self):
    self.state_0()

class PanelsHorizontalVertical(LightPattern):
  def __init__(self, board):
    LightPattern.__init__(self, board, states_count=2)

  def state_0(self):
    self.board.panels['t'].set_pat('oooo')
    self.board.panels['b'].set_pat('oooo')
    self.board.panels['r'].clear()
    self.board.panels['l'].clear()
  def state_1(self):
    self.board.panels['t'].clear()
    self.board.panels['b'].clear()
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
