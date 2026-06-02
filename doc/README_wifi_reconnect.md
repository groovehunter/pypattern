# WiFi Reconnect Isoliert Testen

Dieses Mini-Modul trennt den STA-Reconnect vom restlichen App-Code, damit WiFi-Verhalten separat getestet werden kann.

## Neue Dateien

- `esp32/wifi_simple.py` - isolierte Reconnect-Logik mit OOM/Low-Heap Schutz
- `test_wifi_reconnect_module.py` - Desktop-Unit-Tests mit Fake-Network/Fake-GC

## Schnelltest lokal (Desktop/CPython)

```bash
python3 -m py_compile esp32/wifi_simple.py test_wifi_reconnect_module.py
python3 -m unittest -v test_wifi_reconnect_module.py
```

## Schnelltest auf MicroPython (ohne unittest)

```bash
python3 -m py_compile esp32/wifi_simple.py test_wifi_reconnect_micropython.py
```

Auf dem ESP32 in der REPL:

```python
import test_wifi_reconnect_micropython
test_wifi_reconnect_micropython._run()
```

## Einbindung in `main.py` (optional)

1. Instanz mit `ESSID/PASS`, `network`, `gc`, `logger` erzeugen
2. Task starten mit `loop.create_task(service.run_forever())`
3. Alten Inline-Reconnector entfernen

## Parameter

- `retry_interval`: Basis-Wartezeit in Sekunden
- `connect_timeout`: Poll-Zeit bis Timeout
- `min_free_mem`: Unterhalb davon wird Connect uebersprungen
- `pause_after_oom`: Mindestpause ab 3 OOM-Faellen

