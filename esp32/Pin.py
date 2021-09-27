

class DummyPin:
    OUT = None
    """ dummy pin class for posix """
    def __init__(self, pid, mode):
      pass
    def on(self): pass
    def off(self): pass
    def value(self, val): pass
