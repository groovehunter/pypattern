from LightPattern import LightPattern
    # vom bisherigen state zum diesem, was sind fuer aenderungen
    # notwendig? Ist ja wie ein programm, transitions quasi
    # also die ganze struktur, die panels durchlaufen
"""
class SingleLightCycling(LightPattern):
  states_count = 16
  def state_0(self):
    self.board.panels['t'].set_pat('o---')
    self.set_panels_to_pat('rbl', '----')
  def state_1(self):
    self.board.panels['t'].set_pat('-o--')
  def state_2(self):
    self.board.panels['t'].set_pat('--o-')
  def state_3(self):
    self.board.panels['t'].set_pat('---o')
  def state_4(self):
    self.board.panels['t'].clear()
    self.board.panels['r'].set_pat('o---')
  def state_5(self):
    self.board.panels['r'].set_pat('-o--')
  def state_6(self):
    self.board.panels['r'].set_pat('--o-')
  def state_7(self):
    self.board.panels['r'].set_pat('---o')
  def state_8(self):
    self.board.panels['r'].clear()
    self.board.panels['b'].set_pat('o---')
  def state_9(self):
  def state_10(self):
  def state_11(self):
  def state_12(self):
  def state_13(self):
  def state_14(self):
  def state_15(self):
  def state_16(self):
    self.state_0()
"""
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
  def state_0(self):
    self.board.panels['t'].set_pat('oooo')
    self.board.panels['b'].set_pat('oooo')
    self.board.panels['r'].clear()
    self.board.panels['l'].clear()
  def state_1(self):
    self.board.panels['t'].clear()
    self.board.panels['b'].clear()
    self.board.panels['l'].full()
    self.board.panels['r'].full()
  def state_2(self):
    self.state_0()


class Middle_Edge_Cycling(LightPattern):
#  def __init__(self, board):
#    LightPattern.__init__(self, board, states_count=4)
  def state_0(self):
    self.set_all_panels('-oo-')
  def state_1(self):
    self.set_all_panels('o--o')
  def state_2(self):
    self.state_0()
  def state_3(self):
    self.state_1()
  def state_4(self):
    self.state_0()
