# WiFi Reconnect Module Documentation Index

## Overview

Aus der OOM-Fehlersuche entstand eine **isolierte, gut getestete WiFi-Reconnect-Komponente** mit eingebauten Schutzvorrichtungen.

## Dokumentation

### 1. **`README_wifi_reconnect.md`**
   - **Was:** Überblick über das WiFi-Reconnect-Modul
   - **Struktur:** Dateibeschreibungen, Testanweisungen
   - **Für wen:** Schnelle Orientierung

### 2. **`REFACTORING_IMPORT_PATHS.md`**
   - **Was:** Erklärung des `import_setup.py`-Moduls
   - **Struktur:** Warum im Root, Funktionsweise, Verwendungsbeispiele
   - **Für wen:** Dev der Boot-Sequenz verstehen/debuggen

### 3. **`SELFTEST_DOCUMENTATION.md`** ← **Du bist hier**
   - **Was:** Detailanleitung für `test_wifi_reconnect_micropython.py`
   - **Struktur:** Mock-Objekte, Test-Cases, Erweiterbarkeit
   - **Für wen:** Tests verstehen, neue Test-Cases hinzufügen

## Die Module im Überblick

```
pypattern/
├── import_setup.py                        # Bootstrap: sys.path Setup (Root!)
├── esp32/
│   └── wifi_simple.py                     # WiFi-Reconnect Logik
├── test_wifi_reconnect_micropython.py     # Unittest-freie Tests
└── test_wifi_reconnect_module.py          # Desktop Unit-Tests (unittest)
```

## Was löst das?

| Problem | Lösung |
|---------|--------|
| WiFi-OOM crashes ESP32 | Low-Heap-Guard + Backoff-Eskalation |
| Viele parallele Logdateien | Zentrale Log-Drosselung + Rotation |
| RAM-Fragmentation | Aggressive GC vor Connect + WiFi-Stack Reset |
| Unkontrollierte Retries | Circuit-Breaker nach 3 OOMs (15 min Pause) |
| Keine Tests auf MicroPython | unittest-freie Selftest-Suite |

## Quick Start

### Testen (Desktop)
```bash
python3 test_wifi_reconnect_micropython.py
python3 -m unittest -v test_wifi_reconnect_module.py
```

### Auf ESP32 verwenden
```python
# In main.py ist bereits eingebaut:
from esp32.wifi_simple import WifiReconnectService
```

### Test-Suite vor dem Boot ausführen
```python
# In main.py
import test_wifi_reconnect_micropython
code = test_wifi_reconnect_micropython._run()
if code != 0:
    print("SELFTEST FAILED!")
    # Handle error
else:
    # Continue with main()
```

## Weitere Dateien (OOM-Handling)

- **`main.py`**: Integration des Reconnectors + Memory-Checks
- **`flowpy/simplelogger.py`**: Zentrale Log-Drosselung + Rotation
- **`conf/settings.json`**: Logging-Config (Level, Größenlimit)

## Nächste Schritte (optional)

1. Reconnector mit Config-Option im JSON abschaltbar machen?
2. Weitere WiFi-Error-Szenarien testen? (Signal-Loss, WPA-Timeout, etc.)
3. Health-Check einer bestehenden Verbindung hinzufügen?

