from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')
from lib.GenericGeometry import GenericGeometry
from lib.BoardBase import BoardBase
from lib.DisplayBase_uP import DisplayBase
from lib.GraphicLight import GraphicLight
import sys

try:
    from collections import OrderedDict
except ImportError:
    from ucollections import OrderedDict

class GraphicBoard(DisplayBase, GenericGeometry, BoardBase):
    def __init__(self):
        print("init GraphicBoard")
        logger.debug("GraphicBoard __init__")
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
            self.logic_lights[i] = __import__('lib.Light', fromlist=['CoordLight']).CoordLight(i)
        logger.debug("GraphicBoard - logic_lights initialisiert")

    def init_panels_with_logic_lights(self):
        """Initialisiert Panels, sodass sie auf die globalen logic_lights referenzieren."""
        pid = 1
        panels = {}
        for pname in self.area_names:
            panels[pid] = self._create_panel_with_logic_lights(pid, self.num_lights_in_group)
            pid += 1
        self.panels = OrderedDict(panels)
        logger.debug("GraphicBoard - panels mit logic_lights initialisiert")

    def _create_panel_with_logic_lights(self, pid, size):
        from lib.Panel import PanelCoordLights
        panel = PanelCoordLights(pid, size=size)
        start_idx = (pid - 1) * size + 1
        for i in range(1, size+1):
            global_idx = start_idx + (i - 1)
            panel.lights[i] = self.logic_lights[global_idx]
        return panel

    def sync_lights_to_hw(self):
        """Synchronisiert alle logic_lights mit den Hardware-Lichtern (GraphicLight in self.led)."""
        for lid, logic_light in self.logic_lights.items():
            hw_light = self.led.get(lid)
            if hw_light:
                if logic_light.state:
                    hw_light.on()
                else:
                    hw_light.off()

    def enlight_led(self, i):
        """ accessing the hardware (graphic) """
        logger.debug(f"enlight_led({i}): state={self.led[i].state}")
        print(f"enlight_led({i}): state={self.led[i].state}")
        self.led[i].on() if self.led[i].state else self.led[i].off()
        logger.debug(f"GraphicLight {self.led[i]} set to {self.led[i].state}")
        print(f"GraphicLight {self.led[i]} set to {self.led[i].state}")

    def update_board(self):
        # Hier könnte man ggf. das tkinter Fenster updaten, falls nötig
        pass

    def init_leds(self):
        # Canvas wird ausschließlich in pdc_desktop.py initialisiert!
        led = OrderedDict()
        for i in range(1, self.num_lights_total+1):
            logger.debug(f"init_leds: initialisiere GraphicLight {i}")
            led[i] = GraphicLight(i)
        self.led = led
        print("GraphicBoard - init_leds")
        logger.debug("GraphicBoard - init_leds fertig")

    def change_board(self):
        logger.debug("change_board aufgerufen")
        print("change_board aufgerufen")
        super().enlighten()
        self.sync_lights_to_hw()
        logger.debug("change_board fertig")
        print("change_board fertig")
