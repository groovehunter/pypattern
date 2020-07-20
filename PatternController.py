

class PatternController:
  def __init__(self):
    # init as a list  - (of lists, appending later)
    self.pattern = []

  def loop(self):
    for p in self.pattern:
      self.current = p
      self.show()
      sleep(1)

  def show(self):
    print(self.current)

  def load(self, fn):
    """ load pattern sequence from a graphical file representation """
    f = open(fn, 'r')
    for line in f:
      if line.startswith('#') or line.startswith('_'):
        continue
      self.pattern.append(line)
