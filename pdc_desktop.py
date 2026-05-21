import sys
import os
# Projekt-Root und relevante Unterverzeichnisse zu sys.path hinzufügen
ROOT = os.path.abspath(os.path.dirname(__file__))
for sub in ('', 'esp32', 'lib', 'conf'):
    p = os.path.join(ROOT, sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from pdc import PdcSingleton as PDC
from settings import boardname
from Track import Track
from lib.GraphicLight import GraphicLight

# Board initialisieren
pdc = PDC()
pdc.init(board_type='graphic')
pdc.board.boardname = boardname
pdc.board.load_py_conf()
pdc.board.init()
pdc.board.track = Track()

# Pattern-Logik per tkinter-"after"-Timer
STEP_MS = 200  # Intervall in Millisekunden

# Pattern-Status
current_pattern = None
pattern_step = 0
running = True

# Pattern-Liste aus Track-CSV extrahieren (erste Spalte, ohne Duplikate)
track_lines = list(pdc.board.track.lines.values())
pattern_abbrs = [line.split()[0] for line in track_lines if line.strip()]
pattern_names = []
pat_map = getattr(pdc.board.track, 'pat_map', None)
if pat_map is None:
    pat_map = {
        'SLC': 'SingleLightCycling',
        'RPP': 'RotationPanelPattern',
        'PLC': 'PairedLightsCycling',
        'DPP': 'DarkPanelRotationPanelPattern',
        'WM' : 'Windmill',
        'MES': 'MiddleEdgeSynchronousPattern',
        'AOO': 'AllOnOffPattern',
        'FFP': 'FiftyFiftyPattern',
        'OPS': 'OppositePanelsSwitching',
        'COPS': 'CyclingOppositePanelsSwitching',
        'OPB': 'OppositePanelsBlinking',
        'COPB':'CyclingOppositePanelsBlinking',
    }
for abbr in pattern_abbrs:
    name = pat_map.get(abbr, abbr)
    if name not in pattern_names:
        pattern_names.append(name)

# Callback-Funktionen für GUI

def start_pattern():
    global running
    running = True

def stop_pattern():
    global running
    running = False

def select_pattern(pattern_name):
    global current_pattern, pattern_step
    # Pattern sofort aktivieren
    pdc.board.set_pattern(pattern_name)
    pdc.set_current_pattern(pattern_name)
    current_pattern = pdc.board.pattern
    pattern_step = 0

# Canvas und GUI initialisieren
GraphicLight.setup_canvas(
    pdc.board.num_lights_total,
    pattern_names=pattern_names,
    pattern_select_callback=select_pattern,
    start_callback=start_pattern,
    stop_callback=stop_pattern
)
# Jetzt erst die LEDs erzeugen, damit die Kreise gezeichnet werden!
pdc.board.init_leds()
GraphicLight.root.update()

def pattern_step_func():
    global current_pattern, pattern_step
    if not running:
        GraphicLight.root.after(STEP_MS, pattern_step_func)
        return
    # Pattern auswählen, falls noch nicht gesetzt
    if current_pattern is None:
        pat_name = pdc.board.track.next_pattern()
        pdc.board.set_pattern(pat_name)
        pdc.set_current_pattern(pat_name)
        current_pattern = pdc.board.pattern
        pattern_step = 0
    # Nächster Pattern-Schritt
    current_pattern.next_state()
    pdc.board.change_board()
    pattern_step += 1
    # Nach states_count ggf. neues Pattern wählen
    if hasattr(current_pattern, 'states_count') and pattern_step >= current_pattern.states_count:
        current_pattern = None
    # Timer erneut setzen
    GraphicLight.root.after(STEP_MS, pattern_step_func)

# Starten, sobald das Fenster bereit ist
GraphicLight.root.after(500, pattern_step_func)

# Hauptloop (blockiert, hält Fenster offen)
GraphicLight.root.mainloop()
