import json
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
    try:
        with open(path, "r") as f:
            data = json.load(f)
            log.info(f"Hardware-Layouts from '{path}' loaded.")
            return data
    except OSError:
        log.warn(f"Hardware config '{path}' not found. Generating legacy defaults.")
        try:
            save_compact_json(DEFAULT_HARDWARE, path)
        except OSError as e:
            log.error(f"Failed to create {path}: {e}")
        return DEFAULT_HARDWARE
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
