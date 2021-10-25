
class PatternHelper:
  def calc_opp(self):
    i = self.i
    np = self.board.num_panels
    tmp = i + int(np/2)
    if tmp > np:
      opp = i - int(np/2)
    else:
      opp = tmp
    #print("tmp", tmp)
    self.opp = opp
    self.i = i
