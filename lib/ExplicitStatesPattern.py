from lib.LightPattern import LightPattern
    # vom bisherigen state zum diesem, was sind fuer aenderungen
    # notwendig? Ist ja wie ein programm, transitions quasi
    # also die ganze struktur, die panels durchlaufen

class ExplicitStatesPattern(LightPattern):
  states_count = 0

  def subclass_init(self):
    self.initial_state()

  def initial_state(self):
    self.state_0()

  def next_state(self):
    if self.count == self.states_count:
      self.count = 0

    self.count += 1
    print("next: state %i" %self.count)
    exec('self.state_'+str(self.count)+'()')

class WindmillPattern(ExplicitStatesPattern):
  states_count = 4
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

class PanelsHorizontalVertical(ExplicitStatesPattern):
  states_count = 2
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


class Middle_Edge_Cycling(ExplicitStatesPattern):
  states_count = 2
  def state_0(self):
    self.set_all_panels('-oo-')
  def state_1(self):
    self.set_all_panels('o--o')
  def state_2(self):
    self.state_0()

class AllOnOff(ExplicitStatesPattern):
  states_count = 2
  def state_0(self):
    self.set_all_panels('oooo')
  def state_1(self):
    self.set_all_panels('----')
  def state_2(self):
    self.state_0()
