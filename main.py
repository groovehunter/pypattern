try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from app.core.config import load_config
from app.core.config import save_config
from app.core.logger import log
from app.hardware.wifi import WifiManager
from app.hardware.led_controller import get_controller
from app.hardware.layouts import get_layout
from app.patterns.panel import Engine
import app.patterns.library as library
from app.patterns.playlist import PlaylistManager
from app.web.server import WebServer

# Globale Variable für Manager & Webserver
playlist_manager = None
engine = None
leds = None
config = None

def get_current_state_str():
    global playlist_manager
    if not playlist_manager: return "None"
    mode = f"Playlist: {playlist_manager.active_playlist_name}" if playlist_manager.active_playlist_name else "Manual"
    return f"{mode} | {playlist_manager.get_current_name()}"

def get_available_patterns():
    # Holt alle Klassen aus library.py die auf 'Pattern' enden
    return [name for name in dir(library) if name.endswith('Pattern') and name != 'BasePattern']

def api_set_pattern(name):
    global playlist_manager
    return playlist_manager.set_manual_pattern(name)

def get_available_playlists():
    global playlist_manager
    return playlist_manager.get_available_playlists()

def api_set_playlist(name):
    global playlist_manager
    return playlist_manager.start_playlist(name)

def get_current_layout_name():
    global config
    if config:
        return config.get("hardware", {}).get("layout", "default")
    return "default"

def get_available_layouts():
    from app.hardware.layouts import load_hardware_config
    hw = load_hardware_config()
    return list(hw.get("layouts", {}).keys())

def api_set_layout(name):
    global config
    from app.core.config import save_config
    if config:
        config.setdefault("hardware", {})["layout"] = name
        save_config(config, "config.json")
    from app.core.logger import log
    log.info(f"Layout '{name}' saved as default.")

    # 1. Alte Logikschleife sicher stoppen (optional, aber Engine leeren reicht oft)
    playlist_manager.engine.clear_all()
    playlist_manager.engine.update_hardware()

    # 2. Alte LEDs freigeben (besonders ESP32 wichtig)
    if hasattr(playlist_manager.engine.hw, "deinit"):
        playlist_manager.engine.hw.deinit()

    # 3. Neue Hardware Objekte aufbauen
    from app.hardware.layouts import get_layout
    pinmap, panel_config, leds_per_panel = get_layout(name)
    leds = get_controller(pinmap)
    from app.patterns.panel import Engine
    engine = Engine(leds, panel_config, leds_per_panel)
    playlist_manager.engine = engine  # Dem Playlist Manager die neue Engine unterschieben

    # 4. Aktuelles Muster fix neu starten auf den neuen Panels
    if playlist_manager.active_playlist_name:
        playlist_manager.start_playlist(playlist_manager.active_playlist_name)
    else:
        # manual pattern neu starten
        patt_name = playlist_manager.get_current_name()
        if patt_name != "None":
            playlist_manager.set_manual_pattern(patt_name)
    return True

def api_set_speed(val):
    global playlist_manager
    return playlist_manager.set_manual_speed(val)

async def main():
    global playlist_manager, engine, config, leds
    log.info("Starting PyPattern System...")
    
    # 1. Init Config
    config = load_config("config.json")
    
    # 2. Init & Connect WiFi (Non-Blocking)
    wifi = WifiManager(config)
    await wifi.connect()
    
    # Start WiFi Watchdog (läuft im Hintergrund und macht Reconnects, falls nötig)
    asyncio.create_task(wifi.keepalive())
    
    # 3. Hardware / Layout ermitteln
    layout_name = config.get("hardware", {}).get("layout", "default")
    pinmap, panel_config, leds_per_panel = get_layout(layout_name)
    log.info(f"Loaded layout '{layout_name}': {len(panel_config)} panels, {len(pinmap)} lights, {leds_per_panel} leds_per_panel")

    # 4. Hardware Controller & Pattern Engine (Logikschicht) initiieren
    leds = get_controller(pinmap)
    engine = Engine(leds, panel_config, leds_per_panel)

    # 5. Playlist-Manager initiieren (FPS = 10 entspricht await asyncio.sleep(0.1))
    playlist_manager = PlaylistManager(engine, fps=10)
    
    # 6. Webserver initiieren & starten
    web = WebServer(
        get_current_state_str,
        api_set_pattern,
        get_available_patterns,
        get_available_playlists,
        api_set_playlist,
        get_available_layouts,
        api_set_layout,
        get_current_layout_name,
        api_set_speed
    )
    asyncio.create_task(web.start(port=8080))

    # 7. Start-Playlist laden!
    playlist_manager.start_playlist("track1_classic")
    log.info("LED Engine (4 Panels) bereit. Starte asynchrone Pattern-Loop!")

    # 8. Main Application Loop
    log.info("Entering main application loop (System is ready!)...")

    # Ziel: ca. 10 FPS (Tick alle 100ms)
    TICK_MS = 0.1

    try:
        while True:
            # 1. State verändern (Playlist steuert das Timing, Pattern steuern die Logik)
            playlist_manager.tick()

            # 2. GANZ WICHTIG: Das berechnete Bild an die Hardware senden!
            engine.update_hardware()
            
            # Warten für sauberes Timing
            await asyncio.sleep(TICK_MS)
    except asyncio.CancelledError:
        log.info("Main loop cancelled.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("System stopped via KeyboardInterrupt.")
