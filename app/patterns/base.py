class BasePattern:
    """ Abstrakte Basisklasse für alle Pattern. """
    def __init__(self, engine, **kwargs):
        self.engine = engine
        self.tick_count = 0

        # Sicherstellen, dass nur erwartete Kwargs in setup() landen (MicroPython-sicher!)
        # Alle fehlenden ignorieren, indem wir setup() so umschreiben, dass es immer **kwargs im Base schluckt.
        self.setup(**kwargs)

    def setup(self, **kwargs):
        """ Wird einmalig aufgerufen (beim Start des Patterns). """
        pass
    def tick(self):
        """ Wird z.B. 10x pro Sekunde aufgerufen. Hier state verändern! """
        self.tick_count += 1
        pass
    def render(self):
        """ Optionale Trennung zwischen Logik-State Update (tick) und Canvas-Output. """
        pass
