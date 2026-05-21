# Desktop- und Hardware-Synchronisation der Lichter

## Architekturüberblick

- Die Pattern-Logik arbeitet immer mit logischen Light-Objekten (`logic_lights`), die den gewünschten Zustand (an/aus) speichern.
- Für die Hardware (ESP32) gibt es eigene Light-Objekte (z.B. `Esp32Light`), die die Pins schalten.
- Für die Desktop-GUI gibt es eigene Light-Objekte (`GraphicLight`), die die grafische Darstellung übernehmen.

## Synchronisation

- Nach jedem Pattern-Schritt wird in der Board-Klasse (`change_board()`) die Methode `sync_lights_to_hw()` aufgerufen.
- Diese Methode überträgt die Zustände der logischen Lichter (`logic_lights`) auf die Hardware-Lichter (`self.led`), egal ob ESP32 oder Desktop.
- Die eigentlichen Umschaltungen (Pin setzen oder Farbe ändern) erfolgen nur in den Hardware-Lichtern (`Esp32Light`, `GraphicLight`).

## Render-Methoden

- Die Methoden `enlighten_flat`, `enlighten_panel`, `enlighten_group` in `GenericGeometry` rufen für die betroffenen Lichter jeweils `self.enlight_led(i)` auf.
- In der Desktop-Variante (GraphicBoard) ist `enlight_led` nur für Kompatibilität da, die eigentliche Umschaltung erfolgt über `sync_lights_to_hw()`.
- In der Hardware-Variante (Esp32Board) schaltet `enlight_led` direkt die Pins.

## Wichtig

- Die Pattern-Logik bleibt für beide Varianten identisch.
- Die Synchronisation ist immer klar getrennt: Logik → Hardware/GUI.
- Die Board-Klasse ist für die Synchronisation zuständig, nicht die Pattern- oder Geometry-Klasse.

---

**Letzter Stand: 2026-05-21**

mm