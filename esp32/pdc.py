from Esp32Board import Esp32Board
#from BoardBase import GenericBoard

class PdcSingleton(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(PdcSingleton, cls).__new__(cls)
    return cls.instance

  def init(self):
    print("init PDC")
    self.velocity = 5
    if not hasattr(self, 'board'):
        #self.board = GenericBoard()
        self.board = Esp32Board()
