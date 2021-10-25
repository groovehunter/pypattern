from Esp32Board import Esp32Board


def connect(wifi):
  import network
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(wifi['essid'], wifi['wifikey'])
    while not sta_if.isconnected():
      pass
      print('network config:', sta_if.ifconfig())


class PdcSingleton(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(PdcSingleton, cls).__new__(cls)
    return cls.instance

  def init(self):
    print("init PDC")
    self.velocity = 5
    self.sleep_ms = 100
    
    if not hasattr(self, 'board'):
        #self.board = GenericBoard()
        self.board = Esp32Board()

  def config(self, wifi):
    self.connect(wifi)
