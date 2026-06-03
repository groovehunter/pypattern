## pypattern - LED-Steuerung
### Ziel des Projekts

Es soll eine Steuerung von Lichtern erreicht werden. Diese Lichter sind in verschiedenen Formen angeordnet und sollen eine Vielzahl möglicher Muster darstellen können. 

Implementiert sind die Lichter zum einen simuliert in Tkinter, zum anderen laufen sie auf einem esp32 Microcontroller.

Es sind maximal 16 Lichter.


#### Microcontroller esp32  / config

Der Microcontroller braucht die Definition der Pinbelegung

Die configuration soll in python dicts oder json erfolgen. Yaml ist nicht vorhanden in micropython


#### Webinterface

Die website soll vom Handy aus bedienbar sein;
Über das Webinter sollen gewählt werden können:

- Muster
- Geschwindigkeit
- Musterkombinationen
- START/STOPP

### Ablauf

Der Controller soll sich beim Start mit einem vorhandenen WLAN verbinden. Anschlieend wird ein Webserver gestartet, ber den die Steuerung der Lichter mglich ist. 

Die Implementierung sollte so erfolgen dass der zeitliche Ablauf der Muster nicht von der Reaktionszeit des Webservers abhngig ist. Es soll also mglich sein, dass die Muster auch dann weiterlaufen, wenn gerade eine Anfrage an den Webserver bearbeitet wird. Die Zahl der Requests ist berschaubar. 


### Geplante & neu implementierte Funktionen

Es soll eine einfache Mglichkeit geben, die Muster zu ndern und neue Muster hinzuzufgen.

* **Dynamische Hardware Layouts:** Untersttzung verschiedener Hardware-Formen (z. B. Square, Hexagon, Triangle) ber eine Konfigurationsdatei. Die Layouts definieren Panels mit unterschiedlichen Anzahlen von LEDs. Die Musterlogik passt sich dynamisch an (symmetrisches Rendering, unabhngig vom Layout).
* **Live Layout-Wechsel:** Das Webinterface erlaubt den fliegenden Wechsel zwischen den Hardware-Formen ohne Neustart; neue Konfigurationen werden direkt angewandt.
* **Playlists & Tracks:** Automatischer Wechsel zwischen Mustern, formatiert als JSON (`playlists.json`). Jede Playlist definiert eigene Intervalle, Geschwindigkeiten und individuelle Muster-Parameter pro Track.
* **Manuelle Geschwindigkeitskontrolle:** Wenn Lichter manuell angesteuert werden, kann ein "BPM" Schieberegler ber das Webinterface die Lauflichtgeschwindigkeit ohne zu ruckeln vllig nahtlos beschleunigen oder verlangsamen.
* **Non-Blocking uasyncio Engine:** Weder WLAN-Abbrche, noch der GUI-Server drfen die Taktung der LEDs unterbrechen.

---

### Fragen & Offene Punkte (Architektur-Design)

Um die Architektur sauber aufzusetzen, müssen wir noch ein paar Details klären:

1. **Art der Lichter:** Handelt es sich um adressierbare LEDs (z.B. WS2812B / NeoPixel) an einem Datenpin, oder um 16 separate LEDs an 16 verschiedenen GPIO-Pins?
2. **Geometrie/Anordnung:** Sind die Lichter als Matrix (Reihen/Spalten) angeordnet oder freiliegend? Es gab in der alten Codebase Begriffe wie Hexagon, Triangle, Square. Brauchen wir ein echtes 2D-Koordinatensystem für die Muster?
3. **WLAN Fallback:** Wenn das Heim-WLAN nicht erreichbar ist, soll der ESP32 automatisch einen Access Point (AP) aufspannen, damit man Notfall-Einstellungen (wie neues WLAN-Passwort) vornehmen kann?
4. **"Musterkombinationen":** Ist damit eine "Playlist" (Track) gemeint, wo Muster automatisch nach X Sekunden rotieren, oder eher das Übereinanderlegen (Layering) verschiedener Effekte?
5. **Websocket vs. REST:** Reichen normale HTTP-Requests für die Steuerung via Handy, oder soll das Webinterface "Live" Feedback anzeigen (z.B. aktuelles Muster) mittels WebSockets?

Antworten: 

1. GPIO Pins, keine adressierbaren LEDs
2. Nein, es ist nur eine logische Unterteilung in Panel erforderlich. Es gibt 16 Lichter, die in Panels organisiert sind (z.B. 4 Panels mit je 4 Lichtern). Die Muster können sich auf die Panels beziehen, aber es gibt kein echtes 2D-Koordinatensystem.
3. Ja, ein AP-Fallback wäre super;
4. Eher eine Playlist, also automatische Rotation der Muster nach X Sekunden.
5. REST-API reicht eigentlich aus. Es wäre eine Statusanzeige nett, doch kann diese manuell refresht werden, also kein WebSocket notwendig.



### Architektur & Framework-Vorschlag (Grundgerüst)

Ein Neuanfang ist eine sehr gute Idee, um die MicroPython Speicherlimits (Speicherfragmentierung!) von Anfang an zu beherrschen. Wir trennen die Logik radikal in Schichten (Hardware Abstraction Layer - HAL).

#### 1. Schichten-Architektur (HAL)
- **Hardware & Environment Layer:** Kapselt WLAN-Verbindung, Memory-Management und Pin-Setup.
- **Light Controller (HAL):** Ein gemeinsames Interface (`LightController`). Davon gibt es zwei Implementierungen:
  - `Esp32NeoPixelController` (oder PinController)
  - `TkinterSimController` (für den Desktop)
- **Pattern Engine:** Eine asynchrone Endlosschleife (`uasyncio`), die völlig hardware-unabhängig mathematische Muster auf die virtuellen LEDs anwendet.
- **Web/API Layer:** Ein ressourcenschonender `uasyncio`-Webserver, der rein über Message-Queues oder shared State mit der Pattern Engine kommuniziert (komplett Non-Blocking).

#### 2. Vorgehensweise / Roadmap

**Phase 1: Das Fundament (System & Netzwerk)**
- Aufräumen des Workspaces (alte Dateien in ein Backup-Directory `_legacy/` verschieben).
- Modulares Boot-Setup: JSON-Config laden, Non-blocking WLAN (mit AP-Fallback).
- Implementierung eines minimalen `SimpleLogger`, der von Tag 1 an RAM-Limits beachtet.

**Phase 2: Hardware Abstraction & LED Basis**
- Bau des `LightController` Interfaces.
- Basis-Test: "Blink" auf dem ESP32 und im Tkinter (identischer Kerncode!).
- Prüfen, was wir aus dem alten `lib/` (z.B. Geometrie-Mapping) retten können und rüberziehen.

**Phase 3: Pattern Engine & Loop**
- `uasyncio` Task für das Licht bauen. Der läuft in z.B. 20-50 FPS (Ticks).
- State-Management: Eine Thread-Safe/Async-Safe Klasse, die Musterparameter (Speed, Colors) hält.

**Phase 4: Web Application**
- Aufbau der Frontend-Dateien (`index.html`, `app.js`, `style.css`).
- Vanilla JS (keine schweren Frameworks), Fetch API.
- API-Endpunkte für Start/Stop, Musterwahl, etc. implementieren.

**Phase 5: Patterns portieren**
- Die besten Muster aus dem alten Code nehmen, auf das neue Interface umschreiben und optimieren.

### Nächster konkreter Schritt:
Sobald du die Fragen oben beantwortet hast, erstellen wir den `_legacy/` Ordner, schieben den alten Code zur Seite und bauen `boot.py`, `main.py` und das Config-Laden komplett sauber und neu auf.

---

### Analyse der alten Codebase (Legacy Review)
Basierend auf den Antworten können Teile des alten Codes in die neue Architektur übernommen (oder zumindest als Vorlage genutzt) werden:

* **Was wir wiederverwenden/retten:**
  * **Logik von `Light.py` und `Panel.py`:** Die Unterteilung in abstrakte Lichter und Panels (z.B. als Arrays) ist gut, um Muster wie "Alle Lichter eines Panels an" abzubilden.
  * **Muster-Dateien (`patterns/`) und Tracks (`Track.py`):** Die Basis-Idee der CSV-Tracks ist super. Wir laden den Track aber künftig beim Start einmal in den RAM (oder iterativ als Stream), statt bei jedem Loop-Durchlauf in Dateien herumzuhantieren.
  * **`Esp32Light`:** Die Nutzung von `machine.Pin(pin_nr, Pin.OUT)` ist komplett richtig.

* **Was wir verwerfen/stark ändern:**
  * **Dezentrales Logging:** In der alten Codebase hat gefühlt jedes `Light` einen eigenen Logger erzeugt. Das bläht den RAM extrem auf. Wir nutzen einen Single-Point-Logger!
  * **Synchrone Loops:** Der alte Pattern-Loop war oft blockierend. Wir stellen komplett auf `uasyncio` um.

### Neue Ordnerstruktur (Vorschlag)
```text
pypattern/
 ├── _legacy/           # Alles Alte (Referenz)
 ├── app/
 │   ├── core/          # Config-Loader, Logger, uasyncio-Boilerplate
 │   ├── hardware/      # HAL (Hardware Abstraction Layer): ESP32-Pins vs. Tkinter
 │   ├── patterns/      # Panel-Klassen und Pattern-Logik (unabhängig von HW)
 │   └── web/           # REST-API (Lightweight Micro-API)
 ├── tracks/            # Track-CSVs / Playlists
 ├── boot.py            # Minimal! Lädt Env und startet AP/STA-Fallback
 └── main.py            # Ruft app.core auf (Startet Event-Loop)
```
