try:
    # This is the correct way for a relative import within a package.
    # It works when the application is started from main.py.
    from .Esp32Board import Esp32Board
except ImportError:
    # This is the fallback for simpler execution contexts, e.g., running
    # a script directly on the ESP32 where the package structure isn't fully resolved.
    from Esp32Board import Esp32Board

try:
    from lib.GraphicBoard import GraphicBoard
except ImportError:
    GraphicBoard = None

"""
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
"""


class PdcSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PdcSingleton, cls).__new__(cls)
        return cls.instance

    def init(self, board_type=None):
        print("init PDC")
        self.velocity = 5
        self.sleep_ms = 500
        self.current_track = 0
        self.current_pattern = None
        self.manual_pattern_mode = False
        if not hasattr(self, 'board') or board_type is not None:
            if board_type == 'graphic' and GraphicBoard is not None:
                self.board = GraphicBoard()
            else:
                self.board = Esp32Board()

    def set_current_track(self, track_id):
        self.current_track = track_id
        self.manual_pattern_mode = False

    def set_current_pattern(self, pattern_name):
        self.current_pattern = pattern_name
        self.manual_pattern_mode = True

    def is_manual_pattern(self):
        return getattr(self, 'manual_pattern_mode', False)
