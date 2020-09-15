

class Light:
  """ generic object, represent one Light Element """
  def __init__(self, lid):
    self.lid = lid
    self.state = False
  def viceversa(self):
    self.state = not self.state
  def __repr__(self):
    return "Light %i: %i" %(self.lid, self.state)


class LocatedLight(Light):
  """ has a row+col position """
  def __init__(self, lid, position=None):
    Light.__init__(self, lid)
    self.position = position
  def __repr__(self):
    (x, y) = self.position
    return "Light (%i, %i): %i" %(x, y, self.state)
