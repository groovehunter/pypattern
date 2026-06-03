from app.patterns.base import BasePattern
from app.core.logger import log


def _collect_all_lights(engine):
    """Globale LED-Reihenfolge: Panel-ID, dann lokale LED-ID."""
    all_lights = []
    for pid in sorted(engine.panels.keys()):
        panel = engine.panels[pid]
        for lid in sorted(panel.lights.keys()):
            all_lights.append(panel.lights[lid])
    return all_lights

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
        # Flache Liste aller LEDs erzeugen
        self.all_lights = _collect_all_lights(self.engine)

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


class RotateSingleLightPattern(BasePattern):
    """Ein einzelnes Licht rotiert ueber alle LEDs."""
    def setup(self, speed=2, start_index=0, **kwargs):
        self.speed = speed
        self.all_lights = _collect_all_lights(self.engine)
        self.pos = int(start_index) if self.all_lights else 0
        if self.all_lights:
            self.pos %= len(self.all_lights)
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
        if not self.all_lights:
            return

        self.engine.clear_all()
        self.all_lights[self.pos].on()
        self.pos = (self.pos + 1) % len(self.all_lights)


class RotateDoubleLightPattern(BasePattern):
    """Zwei aktive Lichter rotieren gemeinsam ueber alle LEDs."""
    def setup(self, speed=2, spacing=1, start_index=0, **kwargs):
        self.speed = speed
        self.spacing = max(1, int(spacing))
        self.all_lights = _collect_all_lights(self.engine)
        self.pos = int(start_index) if self.all_lights else 0
        if self.all_lights:
            self.pos %= len(self.all_lights)
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
        if not self.all_lights:
            return

        self.engine.clear_all()
        n = len(self.all_lights)
        self.all_lights[self.pos].on()
        self.all_lights[(self.pos + self.spacing) % n].on()
        self.pos = (self.pos + 1) % n


class RotateDoubleDarkPattern(BasePattern):
    """Alle LEDs an, nur zwei dunkle Positionen rotieren."""
    def setup(self, speed=2, spacing=1, start_index=0, **kwargs):
        self.speed = speed
        self.spacing = max(1, int(spacing))
        self.all_lights = _collect_all_lights(self.engine)
        self.pos = int(start_index) if self.all_lights else 0
        if self.all_lights:
            self.pos %= len(self.all_lights)
        self.engine.full_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
        if not self.all_lights:
            return

        self.engine.full_all()
        n = len(self.all_lights)
        self.all_lights[self.pos].off()
        self.all_lights[(self.pos + self.spacing) % n].off()
        self.pos = (self.pos + 1) % n


class RotateTripleLightPattern(BasePattern):
    """Drei aktive Lichter rotieren gemeinsam ueber alle LEDs."""
    def setup(self, speed=2, spacing=1, start_index=0, **kwargs):
        self.speed = max(1, int(speed))
        self.spacing = max(1, int(spacing))
        self.all_lights = _collect_all_lights(self.engine)
        self.pos = int(start_index) if self.all_lights else 0
        if self.all_lights:
            self.pos %= len(self.all_lights)
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
        if not self.all_lights:
            return

        self.engine.clear_all()
        n = len(self.all_lights)
        self.all_lights[self.pos].on()
        self.all_lights[(self.pos + self.spacing) % n].on()
        self.all_lights[(self.pos + (2 * self.spacing)) % n].on()
        self.pos = (self.pos + 1) % n


class BreathingPanelsPattern(BasePattern):
    """Atmender Effekt: pro Panel steigt/faellt die Anzahl aktiver LEDs stufenweise."""
    def setup(self, speed=2, **kwargs):
        self.speed = max(1, int(speed))
        self.level = 0
        self.direction = 1
        self.max_level = max(0, int(getattr(self.engine, "leds_per_panel", 0)))
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return

        self.engine.clear_all()
        for panel in self.engine.panels.values():
            for local_idx in sorted(panel.lights.keys()):
                if local_idx <= self.level:
                    panel.lights[local_idx].on()

        if self.max_level <= 0:
            return

        self.level += self.direction
        if self.level >= self.max_level:
            self.level = self.max_level
            self.direction = -1
        elif self.level <= 0:
            self.level = 0
            self.direction = 1


class CometTrailPattern(BasePattern):
    """Komet mit Nachlauf: Kopf plus kurze Spur wandern ueber alle LEDs."""
    def setup(self, speed=2, trail=3, start_index=0, **kwargs):
        self.speed = max(1, int(speed))
        self.trail = max(1, int(trail))
        self.all_lights = _collect_all_lights(self.engine)
        self.head = int(start_index) if self.all_lights else 0
        if self.all_lights:
            self.head %= len(self.all_lights)
        self.engine.clear_all()

    def tick(self):
        super().tick()
        if self.tick_count % self.speed != 0:
            return
        if not self.all_lights:
            return

        self.engine.clear_all()
        n = len(self.all_lights)
        for i in range(self.trail + 1):
            idx = (self.head - i) % n
            self.all_lights[idx].on()
        self.head = (self.head + 1) % n


