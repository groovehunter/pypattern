# AGENTS.md

## Zweck und Scope
- Dieses Repository hat eine aktive Laufzeit im Ordner `app/`; `_legacy/` ist Referenzmaterial und wird von `main.py` nicht importiert.
- Startpfad: `boot.py` (GC + optional CPU-Frequenz auf ESP32) -> `main.py` (Orchestrierung aller Komponenten).

## Architektur in 90 Sekunden
- `app/core/`: Konfiguration und Logging (`load_config`, globales `log`).
- `app/hardware/`: WLAN (`WifiManager`), Layout-Aufloesung (`get_layout`), Controller-Fabrik (`get_controller`).
- `app/patterns/`: Logischer Zustand (`Engine`/`Panel`/`Light`), Pattern-Klassen in `library.py`, Playlist-Orchestrierung.
- `app/web/server.py`: sehr schlanker async HTTP-Server; steuert alles ueber Callbacks nach `main.py`.
- Hauptdatenfluss pro Tick in `main.py`: `playlist_manager.tick()` -> `engine.update_hardware()` -> `await asyncio.sleep(0.1)`.

## Wichtige Datenquellen (Dateien im Projektroot)
- `config.json`: WLAN + aktives Hardware-Layout (`hardware.layout`).
- `hardware.json`: Layouts als `layouts.<name>.{leds_per_panel,panels}`.
- `playlists.json`: Tracks mit `defaults` + `items[]` (`pattern`, `duration_sec`, optional `args`).
- Fehlen diese Dateien, erzeugen `app/core/config.py`, `app/hardware/layouts.py` und `app/patterns/playlist.py` automatisch Defaults.

## Projekt-spezifische Konventionen
- Neue Pattern muessen in `app/patterns/library.py` liegen, von `BasePattern` erben und auf `Pattern` enden (Discovery via `dir(library)` in `main.py`).
- Pattern sollten `setup(..., **kwargs)` akzeptieren; Playlists koennen zusaetzliche Args injizieren.
- Manual-Mode setzt **beide** Parameter (`speed` und `interval`) auf den Slider-Wert (`PlaylistManager.set_manual_pattern`).
- `Engine` arbeitet mit globalen Light-IDs; `Panel.lights` nutzt panel-lokale Indizes (1..N).
- Layout-Wechsel (`/api/layout`) baut Hardware+Engine neu auf und startet das aktuelle Pattern/Playlist erneut.

## Web/API-Verhalten (keine Framework-Magie)
- Nur GET-Routen mit Query-Parametern: `/api/status`, `/api/pattern?name=...`, `/api/playlist?name=...`, `/api/layout?name=...`, `/api/speed?val=...`.
- `app/web/static/app.js` pollt `/api/status` alle 3s; Frontend erwartet genau die Felder aus `handle_status()`.
- Server streamt statische Dateien in 512-Byte-Chunks (RAM-schonend fuer MicroPython).

## Workflows fuer Agenten
- Lokaler Desktop-Run (Dummy-Hardware automatisch):
```bash
python3 /home/flow/git-uber/pypattern/main.py
```
- UI aufrufen: `http://127.0.0.1:8080/`.
- API-Schnellcheck waehrend Laufzeit:
```bash
curl "http://127.0.0.1:8080/api/status"
curl "http://127.0.0.1:8080/api/pattern?name=WindmillPattern"
```
- Es gibt aktuell keine aktive Test-Suite fuer den neuen `app/`-Stack; Regressionen werden ueblicherweise ueber API/UI-Lauf getestet.

## Aenderungs-Hinweise mit hoher Hebelwirkung
- Wenn du Pattern-Args oder Namen aenderst, synchronisiere `playlists.json` und pruefe `PlaylistManager.next_in_playlist()` auf `TypeError`-Faelle.
- Wenn du API-Felder aenderst, passe gleichzeitig `app/web/static/app.js` an (Status-Payload ist eng gekoppelt).
- Wenn du an Layout-Mapping arbeitest, pruefe sowohl `leds_per_panel` als auch die globale Light-ID-Reihenfolge aus `get_layout()`.

