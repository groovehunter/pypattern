import sys
from app.core.logger import log
class BaseLightController:
    """ Abstraktes Basis-Interface für Licht-Steuerung """
    def __init__(self, num_lights=16):
        self.num_lights = num_lights
        # Zustandscache (spart Lese-Aufrufe an den echten Pins)
        self.state = {i: 0 for i in range(1, num_lights + 1)}
    def set_light(self, lid, state):
        """ Muss von Kindklasse implementiert werden """
        pass
    def set_all(self, state):
        for lid in range(1, self.num_lights + 1):
            self.set_light(lid, state)
    def toggle_all(self):
        for lid in range(1, self.num_lights + 1):
            self.set_light(lid, not self.state[lid])
class Esp32PinController(BaseLightController):
    """ Echte MicroPython GPIO Steuerung """
    def __init__(self, pinmap):
        super().__init__(len(pinmap))
        import machine
        self.pins = {}
        for lid, pin_nr in pinmap.items():
            try:
                self.pins[int(lid)] = machine.Pin(pin_nr, machine.Pin.OUT)
                self.pins[int(lid)].value(0) # Init als OFF
            except Exception as e:
                log.error(f"Failed to init Pin {pin_nr} for Light {lid}: {e}")
        log.info(f"Esp32PinController initialized with {len(self.pins)} GPIO pins.")
    def set_light(self, lid, state):
        val = 1 if state else 0
        if lid in self.pins and self.state[lid] != val:
            self.pins[lid].value(val)
            self.state[lid] = val
class DummyLightController(BaseLightController):
    """ Dummy Controller für Desktop-Entwicklung (Simuliert GPIOs) """
    def __init__(self, num_lights=16):
        super().__init__(num_lights)
        log.info(f"DummyLightController initialized with {num_lights} virtual lights.")
    def set_light(self, lid, state):
        val = 1 if state else 0
        if self.state[lid] != val:
            self.state[lid] = val
            # Um die Konsole nicht zu überfluten, loggen wir nicht jeden Tick
            # log.debug(f"[Dummy] Light {lid} -> {'ON' if state else 'OFF'}")
def get_controller(pinmap):
    """ Factory-Methode, die automatisch die richtige Hardware erkennt """
    
    # Check if we are on MicroPython / ESP32
    if sys.platform not in ('win32', 'linux', 'darwin'):
        try:
            import machine
            return Esp32PinController(pinmap)
        except ImportError:
            pass
    return DummyLightController(len(pinmap))
