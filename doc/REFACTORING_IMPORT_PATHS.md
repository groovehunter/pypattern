# Import Path Setup - Refactoring Summary

## Was wurde gemacht

Der `sys.path`-Setup-Code aus `main.py` wurde extrahiert und in ein separates, flexibles Modul organisiert.

**Wichtig:** Das Modul muss im **Root** des Projekts liegen (nicht in einem Unterordner), weil es beim Programmstart VOR allen anderen Modulimporten geladen werden muss.

### `import_setup.py` (Root)

- **`setup_import_paths(modules=None, use_absolute=True)`** — zentrale Funktion
  - `modules`: Liste der gewünschten Module (Standard: alle 5). Tests können Teilmenge übergeben.
  - `use_absolute`: 
    - `True` (Default): ESP32 mit absoluten Paths (`/esp32`, `/lib`, etc.)
    - `False`: Desktop/Testing mit relativen Paths (von cwd aus)
  - Entfernt alte relative/absolute Einträge, fügt neue hinzu
  - **Flexibel**: Tests brauchen nur `['esp32']`, nicht alle 5 Module

### `main.py`

```python
from import_setup import setup_import_paths
setup_import_paths()  # Alle Module, absolute Paths (Standard)
```

- Wird am Anfang aufgerufen, bevor andere Module importiert werden
- `use_absolute=True` (Default) → optimal für ESP32

### Test-Scripts

- **`test_wifi_reconnect_micropython.py`** und **`test_wifi_reconnect_module.py`**
  ```python
  from import_setup import setup_import_paths
  setup_import_paths(['esp32'], use_absolute=False)
  ```
  - Laden nur `esp32/`-Modul (weniger Overhead)
  - Arbeiten mit relativen Paths auf dem Desktop

## Verwendungsbeispiele

```python
# ESP32 (main.py)
setup_import_paths()  # Alle Module, absolute Paths

# Test auf Desktop
setup_import_paths(['esp32'], use_absolute=False)  # Nur esp32, relative Paths

# Hybridsetup (z.B. web-Test auf Desktop mit esp32 + lib)
setup_import_paths(['esp32', 'lib'], use_absolute=False)
```

## Projektstruktur

```
pypattern/
├── import_setup.py           ← ROOT (nicht in esp32/ !)
├── main.py
├── test_wifi_reconnect_module.py
├── test_wifi_reconnect_micropython.py
├── esp32/
│   ├── wifi_simple.py
│   ├── pdc.py
│   └── ...
├── lib/
└── ...
```

## Verifizierung

```bash
# Kompilierung
python3 -m py_compile import_setup.py main.py

# Tests (alle grün)
python3 test_wifi_reconnect_micropython.py  # OK
python3 -m unittest -v test_wifi_reconnect_module.py  # OK, 3/3
```

## Vorteile

- ✅ Flexible Modullisten (Tests laden nur nötige Module)
- ✅ Desktop-Testing mit relativen Paths
- ✅ ESP32-Deployment mit absoluten Paths
- ✅ Zentrale Verwaltung → einfach zu debuggen
- ✅ Keine Duplikation importspezifischen Codes
- ✅ **Korrekt platziert:** Root, nicht in Unterordner


