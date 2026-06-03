import json
import os
from app.core.logger import log
# Die alten esp32 Hardware Pin-Gruppierungen direkt im neuen, sauberen 2D-Listen Format:
# Äußere Liste = Alle Panels
# Innere Liste = Die einzelnen echten Pins (LEDs) auf diesem Panel
DEFAULT_HARDWARE = {
    "layouts": {
        "square": {
            "leds_per_panel": 4,
            "panels": [
                [13, 12, 14, 27],
                [26, 25, 33, 32],
                [2, 4, 16, 17],
                [5, 18, 19, 21]
            ]
        },
        "triangle": {
            "leds_per_panel": 4,
            "panels": [
                [13, 12, 14, 27],
                [26, 25, 33, 32],
                [2, 4, 16, 17]
            ]
        },
        "default": {
            "leds_per_panel": 4,
            "panels": [
                [13, 12, 14, 27],
                [26, 25, 33, 32],
                [2, 4, 16, 17],
                [5, 18, 19, 21]
            ]
        },
        "hexagon_qq": {
            "leds_per_panel": 2,
            "panels": [
                [13, 12],
                [14, 27],
                [26, 25],
                [33, 32],
                [2, 4],
                [22, 23]
            ]
        },
        "hexagon_rxtx": {
            "leds_per_panel": 2,
            "panels": [
                [13, 12],
                [14, 27],
                [26, 25],
                [33, 32],
                [2, 4],
                [16, 17]
            ]
        },
        "hexagon_single": {
            "leds_per_panel": 1,
            "panels": [
                [13],
                [12],
                [14],
                [27],
                [26],
                [25]
            ]
        },
        "hexagon_full": {
            "leds_per_panel": 3,
            "panels": [
                [13, 12, 14],
                [27, 26, 25],
                [33, 32, 2],
                [4, 16, 17],
                [5, 18, 19],
                [21, 22, 23]
            ]
        }
    }
}

_hardware_cache_path = None
_hardware_cache_mtime = None
_hardware_cache_data = None

# GPIOs mit denen im Projekt sinnvoll LED-Ausgaenge betrieben werden koennen.
ESP32_ALLOWED_PINS = [2, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33]
ESP32_RESTRICTED_PINS = [2, 12, 15]
ESP32_INPUT_ONLY_PINS = [34, 35, 36, 39]


def _read_mtime(path):
    """Liest mtime robust fuer CPython und MicroPython."""
    try:
        st = os.stat(path)
    except OSError:
        return None

    try:
        return st.st_mtime
    except AttributeError:
        if isinstance(st, tuple) and len(st) > 8:
            return st[8]
    return None
def save_compact_json(data, path):
    """
    Speichert das Dict manuell, damit Listen-Elemente 
    z.B. [13, 12, 14, 27] schön kompakt in EINER Zeile bleiben.
    """
    out = "{\n    \"layouts\": {\n"
    layouts = data.get("layouts", {})
    last_l = len(layouts) - 1
    
    for i, (name, layout_data) in enumerate(layouts.items()):
        if isinstance(layout_data, list):
            leds_pp = 4
            panels = layout_data
        else:
            leds_pp = layout_data.get("leds_per_panel", 4)
            panels = layout_data.get("panels", [])

        out += f"        \"{name}\": {{\n"
        out += f"            \"leds_per_panel\": {leds_pp},\n"
        out += f"            \"panels\": [\n"

        last_p = len(panels) - 1
        for j, panel in enumerate(panels):
            str_panel = ", ".join(str(p) for p in panel)
            out += f"                [{str_panel}]"
            out += ",\n" if j < last_p else "\n"
        out += "            ]\n"
        out += "        }"
        out += ",\n" if i < last_l else "\n"
        
    out += "    }\n}\n"
    
    with open(path, "w") as f:
        f.write(out)

def load_hardware_config(path="hardware.json"):
    global _hardware_cache_path, _hardware_cache_mtime, _hardware_cache_data
    mtime = _read_mtime(path)
    cache_hit = (
        _hardware_cache_data is not None and
        _hardware_cache_path == path and
        (_hardware_cache_mtime == mtime or mtime is None)
    )
    if cache_hit:
        return _hardware_cache_data

    try:
        with open(path, "r") as f:
            data = json.load(f)
            log.info(f"Hardware-Layouts from '{path}' loaded.")
            _hardware_cache_path = path
            _hardware_cache_mtime = mtime
            _hardware_cache_data = data
            return data
    except OSError:
        log.warn(f"Hardware config '{path}' not found. Generating legacy defaults.")
        try:
            save_compact_json(DEFAULT_HARDWARE, path)
        except OSError as e:
            log.error(f"Failed to create {path}: {e}")
        _hardware_cache_path = path
        _hardware_cache_mtime = _read_mtime(path)
        _hardware_cache_data = DEFAULT_HARDWARE
        return DEFAULT_HARDWARE


def get_pin_metadata():
    return {
        "allowed_pins": ESP32_ALLOWED_PINS,
        "restricted_pins": ESP32_RESTRICTED_PINS,
        "input_only_pins": ESP32_INPUT_ONLY_PINS,
    }


def save_hardware_config(data, path="hardware.json"):
    global _hardware_cache_path, _hardware_cache_mtime, _hardware_cache_data
    try:
        save_compact_json(data, path)
    except OSError as e:
        log.error(f"Failed to save hardware config '{path}': {e}")
        return False

    _hardware_cache_path = path
    _hardware_cache_mtime = _read_mtime(path)
    _hardware_cache_data = data
    return True


def clone_layout(source_name, target_name, path="hardware.json"):
    hw_config = load_hardware_config(path)
    layouts = hw_config.get("layouts", {})

    if source_name not in layouts:
        return False, "Source layout not found"
    if not target_name:
        return False, "Target layout required"
    if target_name in layouts:
        return False, "Target layout already exists"

    source = layouts[source_name]
    if isinstance(source, dict):
        src_panels = source.get("panels", [])
        leds_per_panel = source.get("leds_per_panel", 4)
    else:
        src_panels = source
        leds_per_panel = 4

    cloned_panels = []
    for panel in src_panels:
        cloned_panels.append([int(pin) for pin in panel])

    layouts[target_name] = {
        "leds_per_panel": int(leds_per_panel),
        "panels": cloned_panels,
    }
    return (True, "Layout cloned") if save_hardware_config(hw_config, path) else (False, "Save failed")


def set_layout_pin(layout_name, panel_index, slot_index, pin, path="hardware.json", protect_default=True):
    hw_config = load_hardware_config(path)
    layouts = hw_config.get("layouts", {})
    if layout_name not in layouts:
        return False, "Layout not found"
    if protect_default and layout_name == "default":
        return False, "Default layout is read-only"

    layout_data = layouts[layout_name]
    if isinstance(layout_data, dict):
        panels = layout_data.get("panels", [])
    else:
        panels = layout_data
        layout_data = {"leds_per_panel": 4, "panels": panels}
        layouts[layout_name] = layout_data

    try:
        panel_idx = int(panel_index) - 1
        slot_idx = int(slot_index) - 1
        new_pin = int(pin)
    except (TypeError, ValueError):
        return False, "panel, slot and pin must be integers"

    if new_pin not in ESP32_ALLOWED_PINS:
        return False, "Pin not allowed"
    if panel_idx < 0 or panel_idx >= len(panels):
        return False, "Panel index out of range"
    if slot_idx < 0 or slot_idx >= len(panels[panel_idx]):
        return False, "Slot index out of range"

    for p_idx, panel in enumerate(panels):
        for s_idx, used_pin in enumerate(panel):
            if p_idx == panel_idx and s_idx == slot_idx:
                continue
            if int(used_pin) == new_pin:
                return False, f"Pin {new_pin} already used"

    panels[panel_idx][slot_idx] = new_pin
    return (True, "Pin updated") if save_hardware_config(hw_config, path) else (False, "Save failed")


def get_layout_editor_status(path="hardware.json"):
    hw_config = load_hardware_config(path)
    layouts = hw_config.get("layouts", {})
    return {
        "layouts": layouts,
        "pin_meta": get_pin_metadata(),
        "protected_layouts": ["default"],
    }


def get_layout(layout_name):
    """
    Liest aus der JSON die Layouts.
    Spuckt das fertig nummerierte Pin-Map-Dict (fürs HAL),
    die Panel-Konfiguration (für die Engine) und die
    maximale/erwartete Anzahl LEDs pro Panel aus.
    """
    hw_config = load_hardware_config()
    layouts = hw_config.get("layouts", DEFAULT_HARDWARE["layouts"])
    # Ausgewähltes Layout holen, Fallback ist "default"
    layout_data = layouts.get(layout_name, layouts.get("default", {}))

    # Neu: Layouts sind jetzt dicts mit "panels" und "leds_per_panel"
    if isinstance(layout_data, dict):
        groups = layout_data.get("panels", [])
        leds_per_panel = layout_data.get("leds_per_panel", 4)
    else:
        # Fallback für alte Konfiguration (nur Liste)
        groups = layout_data
        leds_per_panel = 4

    pinmap = {}
    panel_config = []
    lid = 1
    for group in groups:
        panel_lights = []
        for pin in group:
            pinmap[str(lid)] = pin
            panel_lights.append(lid)
            lid += 1
        panel_config.append(panel_lights)
    return pinmap, panel_config, leds_per_panel
