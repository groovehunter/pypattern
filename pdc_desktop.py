import sys
import os
# Projekt-Root und relevante Unterverzeichnisse zu sys.path hinzufügen
ROOT = os.path.abspath(os.path.dirname(__file__))
for sub in ('', 'esp32', 'lib', 'conf'):
    p = os.path.join(ROOT, sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from pdc import PdcSingleton as PDC
import tkinter.messagebox as messagebox
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
# default interval (fallback) in Millisekunden; actual interval is read from pdc.sleep_ms
STEP_MS = 200

# Pattern-Status
current_pattern = None
pattern_step = 0
running = True

# Build pattern list for the GUI. Use the full list from the board (DisplayBase)
# so the GUI shows all available patterns, not only those referenced in the Track.
try:
    pattern_names = pdc.board.total_pattern_list()
except Exception:
    # Fallback: minimal list inferred from track as before
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
    ok = False
    kwargs = None
    # if track provided kwargs for this selection (ComboPattern), use them
    try:
        if pattern_name == 'ComboPattern' and hasattr(pdc.board, 'track') and getattr(pdc.board.track, 'last_pattern_kwargs', None):
            kwargs = pdc.board.track.last_pattern_kwargs
    except Exception:
        kwargs = None
    try:
        if kwargs:
            ok = pdc.board.set_pattern(pattern_name, **kwargs)
        else:
            ok = pdc.board.set_pattern(pattern_name)
    except Exception:
        ok = False
    if not ok:
        # error already shown by set_pattern; abort
        return
    try:
        pdc.set_current_pattern(pattern_name)
    except Exception:
        pass
    # clear any track-provided kwargs after successful use
    try:
        if hasattr(pdc.board, 'track') and getattr(pdc.board.track, 'last_pattern_kwargs', None):
            pdc.board.track.last_pattern_kwargs = None
    except Exception:
        pass
    current_pattern = pdc.board.pattern
    pattern_step = 0

def on_bpm_change(v):
    try:
        iv = int(v)
        if iv > 0:
            pdc.sleep_ms = int(60000 / iv)
            pdc.current_bpm = iv
    except Exception:
        pass

def quit_app():
    try:
        GraphicLight.root.destroy()
    except Exception:
        pass
    try:
        import sys
        sys.exit(0)
    except Exception:
        pass

# Geometry apply callback: Anzahl Lichter / Panels anpassen
def apply_geometry(num_lights, num_panels, lights_per_panel=0, area_names_str=''):
    global running
    try:
        nl = int(num_lights)
        npan = int(num_panels)
        if nl < 1 or npan < 1:
            return
    except Exception:
        return

    # Stop the pattern loop while reconfiguring
    running = False

    # Validate multiplicity: number of lights must be a multiple of number of panels
    try:
        lpp = int(lights_per_panel)
    except Exception:
        lpp = 0
    if lpp and lpp > 0:
        # if lights_per_panel provided, it must divide nl exactly
        if nl % lpp != 0:
            try:
                messagebox.showerror('Geometry error', f'Lights ({nl}) is not multiple of L/Panel ({lpp}).')
            except Exception:
                pass
            running = True
            return
        computed_panels = nl // lpp
        npan = computed_panels
    else:
        # require nl % npan == 0
        if nl % npan != 0:
            try:
                messagebox.showerror('Geometry error', f'Lights ({nl}) must be multiple of Panels ({npan}).')
            except Exception:
                pass
            running = True
            return

    # Rebuild canvas positions (aligned to panels) so GraphicLight.__init__ can create ovals
    GraphicLight.rebuild_positions(nl, num_panels=npan)

    # Draw panel bands behind lights
    try:
        GraphicLight.draw_panels(npan)
    except Exception:
        pass

    # Update board geometry
    import math
    pdc.board.num_lights_total = nl
    if lpp and lpp > 0:
        pdc.board.num_lights_in_group = max(1, lpp)
        pdc.board.num_panels = int(math.ceil(nl / pdc.board.num_lights_in_group))
    else:
        pdc.board.num_panels = max(1, int(npan))
        pdc.board.num_lights_in_group = max(1, int(math.ceil(nl / pdc.board.num_panels)))
    pdc.board.num_areas = pdc.board.num_panels
    # area names
    areas = []
    if area_names_str and area_names_str.strip():
        parts = [p.strip() for p in area_names_str.split(',') if p.strip()]
        if len(parts) == pdc.board.num_panels:
            areas = parts
        else:
            areas = [f'P{i}' for i in range(1, pdc.board.num_panels+1)]
    else:
        areas = [f'P{i}' for i in range(1, pdc.board.num_panels+1)]
    pdc.board.area_names = areas

    # Reinitialize board (panels, leds, groups)
    try:
        pdc.board.init()
    except Exception:
        pass
    try:
        GraphicLight.root.update()
    except Exception:
        pass

    # restart pattern loop
    running = True

# Canvas und GUI initialisieren
initial_bpm = getattr(pdc, 'current_bpm', None)
if initial_bpm is None and hasattr(pdc, 'sleep_ms') and pdc.sleep_ms > 0:
    try:
        initial_bpm = round(60000 / pdc.sleep_ms)
    except Exception:
        initial_bpm = None

GraphicLight.setup_canvas(
    pdc.board.num_lights_total,
    pattern_names=pattern_names,
    pattern_select_callback=select_pattern,
    start_callback=start_pattern,
    stop_callback=stop_pattern,
    bpm_change_callback=on_bpm_change,
    quit_callback=quit_app,
    bpm_initial=initial_bpm,
    geometry_apply_callback=apply_geometry
)
# Recompute positions aligned to panels, draw panels, then create LEDs
try:
    npan = getattr(pdc.board, 'num_panels', getattr(pdc.board, 'num_areas', 1))
    GraphicLight.rebuild_positions(pdc.board.num_lights_total, num_panels=npan)
    GraphicLight.draw_panels(npan)
except Exception:
    pass

# If setup created geometry vars, initialize them from current board config
if hasattr(GraphicLight, 'num_lights_var'):
    try:
        GraphicLight.num_lights_var.set(pdc.board.num_lights_total)
    except Exception:
        pass
if hasattr(GraphicLight, 'num_panels_var'):
    try:
        GraphicLight.num_panels_var.set(getattr(pdc.board, 'num_areas', 1))
    except Exception:
        pass
if hasattr(GraphicLight, 'lights_per_panel_var'):
    try:
        GraphicLight.lights_per_panel_var.set(getattr(pdc.board, 'num_lights_in_group', 0))
    except Exception:
        pass
if hasattr(GraphicLight, 'area_names_var'):
    try:
        GraphicLight.area_names_var.set(','.join(getattr(pdc.board, 'area_names', [])))
    except Exception:
        pass
if hasattr(GraphicLight, 'total_lights_var'):
    try:
        # prefer computed value from board if available
        lpp = getattr(pdc.board, 'num_lights_in_group', 0)
        npan = getattr(pdc.board, 'num_panels', getattr(pdc.board, 'num_areas', 1))
        if lpp and lpp > 0:
            GraphicLight.total_lights_var.set(npan * lpp)
        else:
            GraphicLight.total_lights_var.set(getattr(pdc.board, 'num_lights_total', 0))
    except Exception:
        pass
# Jetzt erst die LEDs erzeugen, damit die Kreise gezeichnet werden!
pdc.board.init_leds()
GraphicLight.root.update()

def pattern_step_func():
    global current_pattern, pattern_step
    if not running:
        next_ms = getattr(pdc, 'sleep_ms', STEP_MS)
        GraphicLight.root.after(next_ms, pattern_step_func)
        return
    # Pattern auswählen, falls noch nicht gesetzt
    if current_pattern is None:
        pat_name = pdc.board.track.next_pattern()
        ok = False
        kwargs = None
        try:
            if pat_name == 'ComboPattern' and hasattr(pdc.board, 'track') and getattr(pdc.board.track, 'last_pattern_kwargs', None):
                kwargs = pdc.board.track.last_pattern_kwargs
        except Exception:
            kwargs = None
        try:
            if kwargs:
                ok = pdc.board.set_pattern(pat_name, **kwargs)
            else:
                ok = pdc.board.set_pattern(pat_name)
        except Exception:
            ok = False
        if not ok:
            # error shown to user; skip this pattern selection
            current_pattern = None
            GraphicLight.root.after(getattr(pdc, 'sleep_ms', STEP_MS), pattern_step_func)
            return
        try:
            pdc.set_current_pattern(pat_name)
        except Exception:
            pass
        # clear any track-provided kwargs after successful use
        try:
            if hasattr(pdc.board, 'track') and getattr(pdc.board.track, 'last_pattern_kwargs', None):
                pdc.board.track.last_pattern_kwargs = None
        except Exception:
            pass
        current_pattern = pdc.board.pattern
        pattern_step = 0
    # Nächster Pattern-Schritt
    # synchronous next_state and change_board
    current_pattern.next_state()
    pdc.board.change_board()
    pattern_step += 1
    # Nach states_count ggf. neues Pattern wählen
    if hasattr(current_pattern, 'states_count') and pattern_step >= current_pattern.states_count:
        current_pattern = None
    # Update status display
    try:
        pat_name = getattr(pdc, 'current_pattern', None)
        if pat_name is None and current_pattern is not None:
            try:
                pat_name = current_pattern.__class__.__name__
            except Exception:
                pat_name = str(current_pattern)
        bpm_val = getattr(pdc, 'current_bpm', None)
        if bpm_val is None and hasattr(pdc, 'sleep_ms') and pdc.sleep_ms > 0:
            try:
                bpm_val = round(60000 / pdc.sleep_ms)
            except Exception:
                bpm_val = None
        GraphicLight.set_status(pattern=pat_name, track=getattr(pdc, 'current_track', None), bpm=bpm_val)
    except Exception:
        pass

    # Timer erneut setzen
    next_ms = getattr(pdc, 'sleep_ms', STEP_MS)
    GraphicLight.root.after(next_ms, pattern_step_func)

# Starten, sobald das Fenster bereit ist
GraphicLight.root.after(500, pattern_step_func)

# Hauptloop (blockiert, hält Fenster offen)
GraphicLight.root.mainloop()
