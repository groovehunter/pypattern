# WiFi Reconnect Self-Test (`run_selftest`)

## Überblick

Das Modul `test_wifi_reconnect_micropython.py` enthält ein **unittest-freies Selbsttest-Framework** für `WifiReconnectService` aus `esp32/wifi_simple.py`.

Warum unittest-frei?
- MicroPython hat kein `unittest`-Modul
- Das Framework soll auf ESP32 und Desktop gleich funktionieren
- Minimale Abhängigkeiten = bessere Portabilität

## Architektur

### 1. **Fake-Objekte** (Mock Objects)

Statt echter Hardware-Module (die nicht im Test verfügbar sind) verwenden wir **Fakes**, die den gleichen Interface haben:

#### `FakeGC` – Simuliert `gc` (Garbage Collector)
```python
FakeGC(free=70000, alloc=90000)  # Nur 70 KB frei (Low-Heap-Szenario)
FakeGC(free=120000, alloc=50000)  # Normal: 120 KB frei
```
- `mem_free()` → gibt konfigurierte freie Bytes zurück
- `mem_alloc()` → gibt konfigurierte allokierte Bytes zurück
- `collect()` → wird aufgerufen, wenn GC läuft (trackbar)

#### `FakeSTA` – Simuliert WiFi-Interface
```python
FakeSTA()
  .connected = False                # Startszustand: nicht verbunden
  .raise_on_connect = None          # Oder: Exception("WiFi Out of Memory")
  .connect_calls = 0                # Zähler für Diagnose
```
- `isconnected()` → gibt `connected`-Status zurück
- `ifconfig()` → gibt Fake-IP (192.168.1.23) zurück
- `active(True|False)` → setzt aktiven State
- `connect(essid, pw)` → versucht zu verbinden (kann Exception werfen)

#### `FakeNetwork` – Wrapper um `FakeSTA`
```python
FakeNetwork(sta)
  .WLAN(network.STA_IF) → liefert die FakeSTA-Instanz
```

### 2. **Test-Helper**

#### `_check(name, condition)`
```python
_check("my test", some_boolean)
```
- Gibt `[PASS]` oder `[FAIL]` auf der Konsole aus
- Gibt `True` oder `False` zurück (für Aggregation)
- **Ziel:** einfach, lesbar, MicroPython-kompatibel

## Die Test-Cases in `run_selftest()`

### **Test 1: Low-Heap-Guard**
```python
# Setup: Free Memory < min_free_mem
FakeGC(free=70000, alloc=90000)      # 70 KB frei < 86 KB threshold
svc1 = WifiReconnectService(..., min_free_mem=86000)

# Action
res1 = await svc1.attempt_once()

# Assertion
✓ res1["status"] == "skip_low_heap"  (Ei, nicht versucht!)
✓ sta1.connect_calls == 0            (kein Connect-Aufruf gemacht)
```

**Warum dieser Test?**
- Verhindert einen WiFi-Connect-Versuch bei zu kleinem Heap
- Schützt vor Heap-Fragmentierung + OOM crashes

---

### **Test 2: Normaler Connect (Happy Path)**
```python
# Setup: Ausreichend Speicher
FakeGC(free=120000, alloc=50000)     # 120 KB frei (groß genug)
svc2 = WifiReconnectService(...)

# Action
res2 = await svc2.attempt_once()

# Assertion
✓ res2["status"] == "connected"      (erfolgreich!)
✓ sta2.connect_calls >= 1            (Connect wurde aufgerufen)
```

**Warum dieser Test?**
- Normale Operation sollte funktionieren
- Sanity-Check: Happy-Path funktioniert noch

---

### **Test 3: OOM-Backoff-Eskalation**
```python
# Setup: WiFi-Modul wirft OOM-Exception
sta3.raise_on_connect = Exception("WiFi Out of Memory")
svc3 = WifiReconnectService(
    ...,
    retry_interval=60,     # Basis-Wartezeit
    pause_after_oom=900,   # Nach 3+ OOMs: 15min Pause
)

# Action: 3 Versuche hintereinander
r31 = await svc3.attempt_once()   # OOM → wait 180s (60*3)
r32 = await svc3.attempt_once()   # OOM → wait 180s (60*3)
r33 = await svc3.attempt_once()   # OOM → wait 900s (pause_after_oom)

# Assertion
✓ Alle 3: status == "oom"
✓ r33["wait_s"] == 900             (eskaliert zu 15 min!)
```

**Warum dieser Test?**
- OOMs sind ernsthafte Fehler; unkontrollierte Retries würden noch mehr Schaden anrichten
- Backoff verhindert "Hammering" der Hardware
- Eskalation schützt den Rest des Systems (Pattern-Loop, Webserver)

---

## Verwendung

### **Lokal testen (Desktop/CPython)**
```bash
python3 test_wifi_reconnect_micropython.py
```

**Output:**
```
[PASS] low heap skip
[PASS] connect success
[PASS] oom backoff escalation
SELFTEST RESULT: OK
```

### **Auf ESP32 testen (REPL)**
```python
import test_wifi_reconnect_micropython
test_wifi_reconnect_micropython._run()
```

Oder direkt im Skript:
```bash
# Beim Boot von main.py vor dem Loop
import test_wifi_reconnect_micropython
test_wifi_reconnect_micropython._run()
# Wenn OK → Weitermachen, sonst Fehler anschauen
```

### **Einzelne Test-Cases in eigenem Skript einbinden**
```python
from test_wifi_reconnect_micropython import FakeSTA, FakeGC, FakeNetwork
from esp32.wifi_simple import WifiReconnectService

# Eigener Test
sta = FakeSTA()
svc = WifiReconnectService(
    essid="test",
    password="pwd",
    network_mod=FakeNetwork(sta),
    gc_mod=FakeGC(free=100000),
)
result = await svc.attempt_once()
print(result)
```

## Technische Details

### Async-Kompatibilität
```python
def _run():
    try:
        return asyncio.run(run_selftest())  # Python 3.7+
    except AttributeError:
        loop = asyncio.get_event_loop()      # Fallback: MicroPython
        return loop.run_until_complete(run_selftest())
```

### Rückgabewert
- `0` → alle Tests OK
- `1` → mindestens ein Test FAIL

Ermöglicht Integration in Boot-Sequenzen mit exit-codes.

## Erweiterung mit neuen Tests

**Template für einen neuen Test:**
```python
# In run_selftest()

# N) Test-Beschreibung
staN = FakeSTA()
staN.raise_on_connect = Exception("Specific Error")
svcN = WifiReconnectService(
    essid="test",
    password="pw",
    network_mod=FakeNetwork(staN),
    gc_mod=FakeGC(free=100000),
)
resN = await svcN.attempt_once()
ok = _check(
    "test case name here",
    resN.get("status") == "expected_status" and staN.connect_calls == expected_count
) and ok
```

## Vorteile dieses Ansatzes

✅ **Keine externen Abhängigkeiten** – unittest nicht nötig  
✅ **Läuft auf ESP32 UND Desktop** – siehe `asyncio`-Kompatibilität  
✅ **Leicht erweiterbar** – neue Test-Cases einfach hinzufügen  
✅ **Lesbar** – `_check()` + aussagekräftige Assertions  
✅ **Aussagekräftig** – Fakes haben Zähler für State-Tracking  
✅ **Schnell** – läuft in < 50ms

