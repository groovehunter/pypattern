from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')
from flowpy.simplelogger import SimpleLogger
import sys
from lib.LightGroup import LightGroup
from lib.Area import Area
from lib.Light import LocatedLight, CoordLight
from lib.Panel import Panel, PanelCoordLights

if sys.platform == 'esp32':
    from ucollections import OrderedDict
else:
    from collections import OrderedDict

logger = SimpleLogger(path=__name__+'.log', level='DEBUG')


class GenericGeometry:
    """ a spatial hierarchy """

    def init_leds(self):
        """ overwrite in subclass, use adequate display Light klass """
        raise NotImplementedError

    def init_panels(self):
        """ init a OrderedDict of Panels """
        pid = 1
        panels = {}
        for pname in self.area_names:
            # panels[pname] = PanelCoordLights(pid, size=self.num_lights_in_group)
            panels[pid] = PanelCoordLights(pid, size=self.num_lights_in_group)
            pid += 1
        self.panels = OrderedDict(panels)
        # logger.debug(self.panels)

    def init_areas(self):
        """ init a dict of Areas (like Panels) - DEPRECATED / UNUSED """
        # areas = {}
        # for i in range(1, self.num_areas):
        #     areas[i] = Area()
        #     areas[i].aid = i
        #     areas[i].name = self.area_names[i]
        # self.areas = areas
        pass

    def init_groups(self):
        """ initiate ares in groups """
        # gruppentypen: Zwei - ausreichend für vieles?
        # groupA groupB
        # init groups in a row
        nlig = self.num_lights_in_group

        self.groupsA = OrderedDict()
        self.groupsB = OrderedDict()
        for i in range(1, self.num_areas+1):
            self.groupsA[i] = LightGroup(i)
            self.groupsB[i] = LightGroup(i)
            # logger.debug("init LG A+B # ", i)

        lid = 1  # index flat light array
        for i in range(1, self.num_areas+1):
            for l in range(nlig):
                flat_indexA = i * nlig + l
                flat_indexB = i * nlig + l + int(nlig/2)
                # logger.debug("i, l: ", i, l)
                if flat_indexA > self.num_lights_total:
                    flat_indexA = flat_indexA - self.num_lights_total
                if flat_indexB > self.num_lights_total:
                    flat_indexB = flat_indexB - self.num_lights_total
                # logger.debug("flat_index", flat_indexA, flat_indexB)
                self.groupsA[i].lights[l] = self.led[flat_indexA]
                self.groupsB[i].lights[l] = self.led[flat_indexB]

        for i, group in self.groupsA.items():
            pass
        # logger.debug(self.groupsA)
        # logger.debug(self.groupsB)

    def init_panel_lights(self):
        """ for all panels, call the method to initiate the lights """
        for pname, panel in self.panels.items():
            panel.init_lights()

    def enlighten_flat(self):
        """
        Setzt für jedes Light im flachen Array self.led den aktuellen state auf die Hardware (z.B. Esp32Light) ODER ruft in der Desktop-Variante nur die Synchronisation auf.
        Für die Desktop-Variante (GraphicBoard) erfolgt die eigentliche Umschaltung über sync_lights_to_hw().
        """
        #logger.debug("enlighten_flat aufgerufen")
        for i in self.led.keys():
            self.enlight_led(i)

    def enlighten_panel(self):
        """
        Setzt für jedes Light in jedem Panel den aktuellen state auf die Hardware (z.B. Esp32Light) ODER ruft in der Desktop-Variante nur die Synchronisation auf.
        Für die Desktop-Variante (GraphicBoard) erfolgt die eigentliche Umschaltung über sync_lights_to_hw().
        """
        logger.debug("enlighten_panel aufgerufen")
        # Panel-Status als Zeichenkette ausgeben
        panel_status = []
        for panel in self.panels.values():
            status = ['O' if light.state else '-' for light in panel.lights.values()]
            panel_status.append('[' + ''.join(status) + ']')
            for light_idx_in_panel, light in panel.lights.items():
                flat_idx = (panel.pid - 1) * self.num_lights_in_group + light_idx_in_panel
                if flat_idx in self.led:
                    self.enlight_led(flat_idx)
        logger.debug(' '.join(panel_status))

    def enlighten_group(self):
        """
        Setzt für jede Gruppe (z.B. für Pattern mit Gruppenlogik) die aktiven/inaktiven Lichter auf den gewünschten state.
        Für die Desktop-Variante (GraphicBoard) erfolgt die eigentliche Umschaltung über sync_lights_to_hw().
        """
        logger.debug("enlighten_group aufgerufen")
        #print("enlighten_group aufgerufen")
        active_group = self.board.groupsA if self.pattern.count == 0 else self.board.groupsB
        inactive_group = self.board.groupsB if self.pattern.count == 0 else self.board.groupsA

        for group in active_group.values():
            for light in group.lights.values():
                logger.debug(f"enlighten_group: active light {light.lid} -> ON")
                light.on()
                self.enlight_led(light.lid)

        for group in inactive_group.values():
            for light in group.lights.values():
                logger.debug(f"enlighten_group: inactive light {light.lid} -> OFF")
                light.off()
                self.enlight_led(light.lid)

    def enlighten(self):
        """
        Generische Render-Methode.
        Ruft je nach Pattern-Render-Mode die passende enlighten_* Methode auf.
        Für Hardware-Boards (ESP32) werden die Hardware-Lichter direkt geschaltet.
        Für die Desktop-Variante (GraphicBoard) erfolgt die eigentliche Umschaltung über sync_lights_to_hw(),
        das in change_board() der Board-Klasse aufgerufen wird.
        """
        render_mode = getattr(self.pattern, 'render_mode', 'flat')

        if render_mode == 'panel':
            self.enlighten_panel()
        elif render_mode == 'group':
            self.enlighten_group()
        else:  # default to 'flat'
            self.enlighten_flat()

        self.update_board()
