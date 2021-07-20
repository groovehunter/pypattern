from lib.LightPattern import LightPattern


class NextStatePattern(LightPattern):
  def __init__(self, board):
    self.board = board
    self.count = 0
    #LightPattern.__init__(board)

  def next_state(self):
    #super().next_state()
    self.count += 1
    print('NSP - next PLC: ', self.count)
    if self.count > self.states_count-1:
      print("reset counter")
      self.count = 0
    



class AllOnOffPattern(NextStatePattern):
  states_count = 2
  def initial_state(self):
    self.set_all_panels('oooo')

  def next_state(self):
    super().next_state()
#    self.set_all_panels('----')
    self.all_panels_execute_method('viceversa')
