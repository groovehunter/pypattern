import json
from app.core.logger import log
import app.patterns.library as library

DEFAULT_PLAYLISTS = {
    "track1": {
        "defaults": {"speed": 2, "interval": 5},
        "items": [
            {"pattern": "RotatePanelPattern", "duration_sec": 5},
            {"pattern": "CheckerboardPattern", "duration_sec": 5},
            {"pattern": "WindmillPattern", "duration_sec": 5, "args": {"speed": 1}}
        ]
    },
    "track2_fast": {
        "defaults": {"speed": 1},
        "items": [
            {"pattern": "WindmillPattern", "duration_sec": 2},
            {"pattern": "RotatePanelPattern", "duration_sec": 2}
        ]
    }
}

def save_compact_playlist_json(data, path):
    """ Eigener JSON-Writer für Playlists, damit sie auf dem ESP32 hübsch formatiert bleibt. """
    out = "{\n"
    tracks = list(data.items())
    for t_idx, (track_name, track_data) in enumerate(tracks):
        out += f"  \"{track_name}\": {{\n"
        
        # Flexibles Speichern, egal ob neue Dict-Struktur oder alt (Liste)
        if isinstance(track_data, list):
            defaults_str = "{}"
            items = track_data
        else:
            defaults_str = json.dumps(track_data.get("defaults", {}))
            items = track_data.get("items", [])
            
        out += f"    \"defaults\": {defaults_str},\n"
        out += "    \"items\": [\n"
        
        for i_idx, item in enumerate(items):
            p_name = item.get("pattern", "")
            d_sec = item.get("duration_sec", 0)
            
            if "args" in item and item["args"]:
                args_str = json.dumps(item["args"])
                line = f"      {{\"pattern\": \"{p_name}\", \"duration_sec\": {d_sec}, \"args\": {args_str}}}"
            else:
                line = f"      {{\"pattern\": \"{p_name}\", \"duration_sec\": {d_sec}}}"
                
            if i_idx < len(items) - 1:
                line += ","
            out += line + "\n"
            
        out += "    ]\n  }"
        if t_idx < len(tracks) - 1:
            out += ","
        out += "\n"
        
    out += "}\n"
    with open(path, "w") as f:
        f.write(out)

class PlaylistManager:
    def __init__(self, engine, fps=10):
        self.engine = engine
        self.fps = fps
        self.playlists = self._load()
        self.active_playlist_name = None
        self.current_index = 0
        self.ticks_remaining = 0
        self.current_pattern = None
        self.manual_speed = 2  # default speed for manual patterns
    def _load(self, path="playlists.json"):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                log.info(f"Playlists from '{path}' loaded.")
                return data
        except OSError:
            pass  # File missing
        except ValueError:
            log.warn(f"Playlists config '{path}' contains broken JSON. Generating defaults.")
            pass  # File corrupted

        log.info(f"Generating default playlists in '{path}'.")
        try:
            save_compact_playlist_json(DEFAULT_PLAYLISTS, path)
        except OSError as e:
            log.error(f"Failed to create {path}: {e}")
        return DEFAULT_PLAYLISTS
    def start_playlist(self, name):
        if name not in self.playlists:
            log.error(f"Playlist '{name}' not found.")
            return False
        log.info(f"Starting playlist: {name}")
        self.active_playlist_name = name
        self.current_index = -1
        self.ticks_remaining = 0
        self.next_in_playlist()
        return True
    def set_manual_pattern(self, name, **kwargs):
        """ Stoppt die aktuelle Playlist und setzt hart ein manuelles Pattern (z.B. durch UI-Klick) """
        if hasattr(library, name):
            self.active_playlist_name = None  # Playlist abbrechen
            p_class = getattr(library, name)
            
            # Inject current manual speed
            kwargs['speed'] = self.manual_speed
            kwargs['interval'] = self.manual_speed
            
            self.current_pattern = p_class(self.engine, **kwargs)
            log.info(f"Manual pattern set: {name}")
            return True
        log.error(f"Pattern '{name}' not found in library.")
        return False
        
    def set_manual_speed(self, val):
        try:
            self.manual_speed = int(val)
            # Update immediately if a manual pattern is running
            if not self.active_playlist_name and self.current_pattern:
                if hasattr(self.current_pattern, 'interval'):
                    self.current_pattern.interval = self.manual_speed
                if hasattr(self.current_pattern, 'speed'):
                    self.current_pattern.speed = self.manual_speed
            return True
        except ValueError:
            return False

    def next_in_playlist(self):
        if not self.active_playlist_name:
            return
            
        playlist_data = self.playlists[self.active_playlist_name]
        
        # Abwärtskompatibilität: Alt (Liste), Neu (Dict mit Defaults/Items)
        if isinstance(playlist_data, list):
            items = playlist_data
            defaults = {}
        else:
            items = playlist_data.get("items", [])
            defaults = playlist_data.get("defaults", {})
            
        if not items:
            return
            
        self.current_index = (self.current_index + 1) % len(items)
        track_item = items[self.current_index]
        
        p_name = track_item.get("pattern")
        
        # Wir kombinieren Playlist-Defaults mit pattern-spezifischen Args
        p_args = defaults.copy()
        p_args.update(track_item.get("args", {}))
        
        duration_sec = track_item.get("duration_sec", 10)
        
        if hasattr(library, p_name):
            p_class = getattr(library, p_name)
            
            try:
                self.current_pattern = p_class(self.engine, **p_args)
                self.ticks_remaining = int(duration_sec * self.fps)
                log.info(f"Track -> {p_name} (for {duration_sec}s with args {p_args})")
            except TypeError as te:
                log.error(f"Track skipped pattern {p_name} because of arg mismatch: {te}")
                self.ticks_remaining = int(duration_sec * self.fps)
        else:
            log.error(f"Track skipped invalid pattern: {p_name}")
            self.ticks_remaining = int(duration_sec * self.fps) # Trotzdem die Zeit abwarten

    def tick(self):
        # 1. Timer der Playlist herunterzählen
        if self.active_playlist_name:
            self.ticks_remaining -= 1
            if self.ticks_remaining <= 0:
                self.next_in_playlist()
        # 2. Aktuelles Pattern berechnen lassen
        if self.current_pattern:
            self.current_pattern.tick()
    def get_current_name(self):
        if self.current_pattern:
            return self.current_pattern.__class__.__name__
        return "None"
    def get_available_playlists(self):
        return list(self.playlists.keys())
