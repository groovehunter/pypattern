from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')


# is this supposed to be an abstract light for pattern class
# OR is this a hardware LED item??
# OR BOTH possible?!!
class Light:
    """ generic object, represent one Light Element """
    def __init__(self, lid):
        self.lid = lid
        self.state = 0

    def viceversa(self):
        self.state = not self.state

    def __repr__(self):
        return "Light %i: %i" % (self.lid, self.state)

    def on(self):
        self.state = 1
        logger.debug(f"Light {self.lid} ON (state={self.state})")
        #print(f"Light {self.lid} ON (state={self.state})")

    def off(self):
        self.state = 0
        logger.debug(f"Light {self.lid} OFF (state={self.state})")
        #print(f"Light {self.lid} OFF (state={self.state})")


class LocatedLight(Light):
    """ A Light that has a row+col position """
    def __init__(self, lid, position=None):
        Light.__init__(self, lid)
        self.position = position

    def __repr__(self):
        (x, y) = self.position
        return "Light located row/col (%i, %i): %i" % (x, y, self.state)


class CoordLight(Light):
    """ A Light that has coordinates position """
    def __init__(self, lid, position=None):
        Light.__init__(self, lid)
        self.position = position

    def __repr__(self):
        if self.position:
            (x, y) = self.position
            total = "Light (%i, %i): %i" % (x, y, self.state)
        else:
            total = "Light (coord n/a): %i" % (self.state)
        return total

    def on(self):
        self.state = 1
        logger.debug(f"CoordLight {self.lid} ON (state={self.state})")
        #print(f"CoordLight {self.lid} ON (state={self.state})")

    def off(self):
        self.state = 0
        logger.debug(f"CoordLight {self.lid} OFF (state={self.state})")
        #print(f"CoordLight {self.lid} OFF (state={self.state})")

