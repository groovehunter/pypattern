import json
from app.core.logger import log
DEFAULT_CONFIG = {
    "wifi": {
        "ssid": "uvchakras",
        "pwd": "roll2026",
        "ap_fallback_ssid": "PyPattern-AP",
        "ap_fallback_pwd": "password123",
        "timeout_sec": 15,
        "ip": "192.168.43.10",
        "netmask": "255.255.255.0",
        "gateway": "192.168.43.1",
        "dns": "8.8.8.8"
    },
    "hardware": {
        "node": "node1",
        "layout": "default"
    }
}

def load_config(path="config.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            # Einfaches Merge, um Defaults nicht zu verlieren
            for k, v in data.items():
                if isinstance(v, dict) and k in DEFAULT_CONFIG:
                    DEFAULT_CONFIG[k].update(v)
                else:
                    DEFAULT_CONFIG[k] = v
            log.info(f"Config '{path}' loaded.")
    except OSError:
        log.warn(f"Config '{path}' not found. Using defaults and saving.")
        save_config(DEFAULT_CONFIG, path)
    return DEFAULT_CONFIG

def save_config(config, path="config.json"):
    try:
        with open(path, "w") as f:
            json.dump(config, f)
            log.info(f"Config saved to '{path}'.")
    except OSError as e:
        log.error(f"Error saving config: {e}")
