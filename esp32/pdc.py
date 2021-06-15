from Esp32Board import Esp32Board

class PdcSingleton(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(PdcSingleton, cls).__new__(cls)
    return cls.instance

  def init(self):
    print("init PDC")
    if not hasattr(self, 'board'):
        self.board = Esp32Board()
        
        