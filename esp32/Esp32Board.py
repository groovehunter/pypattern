from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')
from lib.GenericGeometry import GenericGeometry
from lib.Light import CoordLight
import os
#print(os.listdir('/lib'))

from lib.BoardBase import BoardBase
from lib.DisplayBase_uP import DisplayBase

try:
    from Esp32Light import Esp32Light
except ImportError:
    from esp32.Esp32Light import Esp32Light

try:
    from ucollections import OrderedDict  # MicroPython
except ImportError:
    from collections import OrderedDict   # CPython


class Esp32Board(DisplayBase, GenericGeometry, BoardBase):
    def __init__(self):
        logger.debug("Esp32Board __init__ (init board)")
        self.logic_lights = None  # Wird in init_logic_lights gesetzt

    def subclass_init(self):
        # Initialisiere logische Lichter
        self.init_logic_lights()
        # Panels initialisieren, sodass sie auf logic_lights referenzieren
        self.init_panels_with_logic_lights()
    def init_logic_lights(self):
        """Initialisiert self.logic_lights als OrderedDict mit CoordLight-Objekten."""
        self.logic_lights = OrderedDict()
        for i in range(1, self.num_lights_total+1):
            self.logic_lights[i] = Esp32Light(i)
        logger.debug("Esp32Board - logic_lights initialisiert (Esp32Light)")

    def init_panels_with_logic_lights(self):
        """Initialisiert Panels, sodass sie auf die globalen logic_lights referenzieren."""
        pid = 1
        panels = {}
        for pname in self.area_names:
            panels[pid] = self._create_panel_with_logic_lights(pid, self.num_lights_in_group)
            pid += 1
        self.panels = OrderedDict(panels)
        logger.debug("Esp32Board - panels mit logic_lights initialisiert")

    def _create_panel_with_logic_lights(self, pid, size):
        from lib.Panel import PanelCoordLights
        panel = PanelCoordLights(pid, size=size)
        # Panel-Lichter auf Referenzen aus logic_lights setzen
        start_idx = (pid - 1) * size + 1
        for i in range(1, size+1):
            global_idx = start_idx + (i - 1)
            panel.lights[i] = self.logic_lights[global_idx]
        return panel

    def sync_lights_to_hw(self):
        """Synchronisiert alle logic_lights mit den Hardware-Lichtern (Esp32Light in self.led)."""
        for lid, logic_light in self.logic_lights.items():
            hw_light = self.led.get(lid)
            if hw_light:
                if logic_light.state:
                    hw_light.on()
                else:
                    hw_light.off()

    def enlight_led(self, i):
        """ accessing the hardware pins """
        logger.debug(f"enlight_led({i}): state={self.led[i].state}")
        #print(f"enlight_led({i}): state={self.led[i].state}")
        self.led[i].pin.value(self.led[i].state)
        #logger.debug(f"Pin {self.led[i].pin} set to {self.led[i].state}")

    def change_board(self):
        # Ensure logic lights are copied to hardware lights, then enlighten
        try:
            self.sync_lights_to_hw()
        except Exception:
            logger.exception("sync_lights_to_hw failed")
        super().enlighten()
        logger.debug("change_board fertig")

    # stub XXX del
    def update_board(self):
        pass

    def init_leds(self):
        led = OrderedDict()
        for i in range(1, self.num_lights_total+1):
            logger.debug(f"init_leds: initialisiere Esp32Light {i}")
            led[i] = Esp32Light(i)
        self.led = led
        logger.debug("Esp32Board - init_leds fertig")

