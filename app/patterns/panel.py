class Light:
    """ Repräsentiert ein logisches Licht, unabhängig von der Hardware. """
    def __init__(self, lid):
        self.lid = lid
        self.state = 0  # 0 = off, 1 = on
    def on(self):
        self.state = 1
    def off(self):
        self.state = 0
    def toggle(self):
        self.state = 1 if self.state == 0 else 0
class Panel:
    """ Gruppiert logische Lichter """
    def __init__(self, pid, light_ids):
        self.pid = pid
        # Dictionary from relative panel index (1 to N) to Light object
        self.lights = {i+1: Light(lid) for i, lid in enumerate(light_ids)}
        self.size = len(light_ids)
    def on(self):
        for light in self.lights.values():
            light.on()
    def off(self):
        for light in self.lights.values():
            light.off()
    def toggle(self):
        for light in self.lights.values():
            light.toggle()
    def is_full(self):
        return all(light.state == 1 for light in self.lights.values())
    def is_clear(self):
        return all(light.state == 0 for light in self.lights.values())


class Engine:
    """ 
    Die zentrale Logikschicht. 
    Hält den Gesamtstatus aller Panels und synchronisiert sich mit dem Hardware-HAL.
    """
    def __init__(self, hardware_controller, panel_config, leds_per_panel=4):
        self.hw = hardware_controller
        self.leds_per_panel = leds_per_panel
        self.panels = {}

        # panel_config ist eine Liste von Listen, z.B.:
        # [[1, 2, 3, 4], [5, 6], [7, 8, 9, 10]]
        for idx, light_ids in enumerate(panel_config):
            pid = idx + 1
            self.panels[pid] = Panel(pid, light_ids)

    def update_hardware(self):
        """ 
        Überträgt den logischen Zustand aller Panels/Lichter auf die echte Hardware.
        Muss am Ende jedes Pattern-Ticks aufgerufen werden!
        """
        for panel in self.panels.values():
            for light in panel.lights.values():
                self.hw.set_light(light.lid, light.state)
    def clear_all(self):
        for panel in self.panels.values():
            panel.off()
    def full_all(self):
        for panel in self.panels.values():
            panel.on()
