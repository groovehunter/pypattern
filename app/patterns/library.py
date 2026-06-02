from app.patterns.base import BasePattern
from app.core.logger import log

class CheckerboardPattern(BasePattern):
    """ Einfaches Schachbrett der 4 Panels (wie unser Test vorher) """
    def setup(self, interval=5, **kwargs):
        # Alle wie viele Ticks das Muster wechseln soll
        self.interval = interval 
        self.engine.clear_all()

    def tick(self):
        super().tick()

        # Nur alle 'interval'-Ticks wechseln
        if self.tick_count % self.interval != 0:
            return

        phase = (self.tick_count // self.interval) % 2

        # Dynamisch arbeiten, egal ob 2, 4 oder 6 Panels
        for pid, panel in self.engine.panels.items():
            if (pid % 2) == phase:
                panel.on()
            else:
                panel.off()

class RotatePanelPattern(BasePattern):
    """ Lässt die 4 Panels reihum aufleuchten """
    def setup(self, speed=5, **kwargs):
        self.speed = speed
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return

        self.engine.clear_all()
        # Active Panel = 1, 2, 3, 4, 1, 2, 3, 4... (dynamisch je nach topology)
        num_panels = len(self.engine.panels)
        if num_panels == 0:
            return

        active_panel = ( (self.tick_count // self.speed) % num_panels ) + 1
        self.engine.panels[active_panel].on()

class WindmillPattern(BasePattern):
    """ Windmühlen-Effekt: Läuft durch die einzelnen Lichter der Panels """
    def setup(self, speed=2, **kwargs):
        self.speed = speed
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
        self.engine.clear_all()

        # Nutzt jetzt engine.leds_per_panel für ein einheitliches Timing
        # egal ob ein spezielles Panel evtl. aus Layout-Gründen Hardware-Pins weglässt
        max_lights = getattr(self.engine, 'leds_per_panel', 4)
        if max_lights == 0:
            return
            
        active_light = ( (self.tick_count // self.speed) % max_lights ) + 1
        for p in self.engine.panels.values():
            if active_light in p.lights:
                p.lights[active_light].on()


class PulseAllPattern(BasePattern):
    """ Lässt alle Lichter synchron blinken """
    def setup(self, speed=5, **kwargs):
        self.speed = speed
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
            
        phase = (self.tick_count // self.speed) % 2
        if phase == 0:
            self.engine.full_all()
        else:
            self.engine.clear_all()


class LarsonScannerPattern(BasePattern):
    """ Knight-Rider / Cylon Lauflicht, das hin und her wandert """
    def setup(self, speed=2, **kwargs):
        self.speed = speed
        self.engine.clear_all()
        self.all_lights = []
        # Flache Liste aller LEDs erzeugen
        for pid in sorted(self.engine.panels.keys()):
            panel = self.engine.panels[pid]
            for lid in sorted(panel.lights.keys()):
                self.all_lights.append(panel.lights[lid])
                
        self.pos = 0
        self.direction = 1

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
            
        if not self.all_lights:
            return

        self.engine.clear_all()
        self.all_lights[self.pos].on()
        
        # Ping-Pong-Logik
        self.pos += self.direction
        if self.pos >= len(self.all_lights) - 1:
            self.pos = len(self.all_lights) - 1
            self.direction = -1
        elif self.pos <= 0:
            self.pos = 0
            self.direction = 1


class RandomSparklePattern(BasePattern):
    """ Zufälliges Flackern einzelner LEDs (Sternenhimmel-Effekt) """
    def setup(self, speed=1, density=30, **kwargs):
        self.speed = speed
        self.density = density  # Wahrscheinlichkeit in %, dass eine LED an ist
        self.engine.clear_all()
        
        # Sicherer Import von getrandbits für PC oder MicroPython
        try:
            from urandom import getrandbits
            self._rand = getrandbits
        except ImportError:
            import random
            self._rand = lambda k: random.getrandbits(k)

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0: 
            return
            
        for panel in self.engine.panels.values():
            for light in panel.lights.values():
                # self._rand(8) gibt 0-255 zurück
                if (self._rand(8) / 255.0 * 100) < self.density:
                    light.on()
                else:
                    light.off()
