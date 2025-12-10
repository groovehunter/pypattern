from lib.Light import LocatedLight


class LightGroup:
    def __init__(self, pid):
        """
        """
        self.lights = {}
        #self.state = 1

    def __repr__(self):
        s = ''
        for key, light in self.lights.items():
            s += light.__repr__()
            s += "\n"
        return s

    def init_lights(self):
        """ calc lights and positions
        """
        pass
