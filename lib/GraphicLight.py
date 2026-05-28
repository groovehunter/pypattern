import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import math
from lib.Light import Light
from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__+'.log', level='DEBUG')

class GraphicLight(Light):
    """
    Ein Light-Objekt, das grafisch als Kreis auf einem tkinter-Canvas dargestellt wird.
    Die LEDs werden kreisförmig angeordnet.
    """
    canvas = None
    root = None
    radius = 20
    circle_radius = 100  # Abstand vom Mittelpunkt
    center_x = 200
    center_y = 200
    circles = {}  # lid -> canvas item
    positions = {}  # lid -> (x, y)

    @classmethod
    def setup_canvas(cls, num_lights, pattern_names=None, pattern_select_callback=None, start_callback=None, stop_callback=None, bpm_change_callback=None, quit_callback=None, bpm_initial=None, geometry_apply_callback=None, panel_band_width=40):
        # determine canvas size to fit half the screen (useful on tiling WMs)
        cls.root = tk.Tk()
        try:
            screen_w = cls.root.winfo_screenwidth()
            screen_h = cls.root.winfo_screenheight()
            # aim for a square canvas that fits half the screen width and most of height
            target_w = max(200, int(screen_w / 2))
            target_h = max(200, int(screen_h * 0.9))
            size = min(target_w, target_h)
            # make canvas a bit smaller per request: use ~3/4 of computed size
            size = max(200, int(size * 3 / 4))
        except Exception:
            size = cls.center_x * 2
        # set centers and sensible defaults based on chosen size
        cls.center_x = size // 2
        cls.center_y = size // 2
        # set a reasonable default light radius relative to size
        cls.radius = max(3, int(size * 0.02))
        cls.root.title("LED Simulation")
        # Two-row control area for better layout
        top_ctrl = tk.Frame(cls.root)
        top_ctrl.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        left_top = tk.Frame(top_ctrl)
        left_top.pack(side=tk.LEFT)
        right_top = tk.Frame(top_ctrl)
        right_top.pack(side=tk.RIGHT)

        # Control column: put QUIT directly above Start/Stop to save a line
        control_col = tk.Frame(left_top)
        control_col.pack(side=tk.LEFT, padx=(2,8))

        if quit_callback is None:
            def _default_quit():
                try:
                    cls.root.destroy()
                except Exception:
                    pass
                try:
                    import sys
                    sys.exit(0)
                except Exception:
                    pass
            quit_callback = _default_quit
        quit_btn = tk.Button(control_col, text='QUIT', command=quit_callback, fg='white', bg='red')
        quit_btn.config(font=(None, 14), width=6, height=1)
        quit_btn.pack(side=tk.TOP, padx=2, pady=(2,4))

        # Start/Stop Buttons directly below QUIT (same column)
        btn_row = tk.Frame(control_col)
        btn_row.pack(side=tk.TOP)
        btn_start = tk.Button(btn_row, text="Start", command=start_callback)
        btn_start.pack(side=tk.LEFT, padx=5, pady=2)
        btn_stop = tk.Button(btn_row, text="Stop", command=stop_callback)
        btn_stop.pack(side=tk.LEFT, padx=5, pady=2)

        # Pattern list (top-left, next to start/stop)
        if pattern_names:
            # Build a tabular view showing pattern name and render mode
            tree = ttk.Treeview(left_top, columns=('pattern', 'mode'), show='headings', height=min(len(pattern_names), 8))
            tree.heading('pattern', text='Pattern')
            tree.heading('mode', text='Mode')
            tree.column('pattern', width=160, anchor='w')
            tree.column('mode', width=80, anchor='center')

            def _resolve_mode(pat_name):
                # try to find the class in known pattern modules and return render_mode
                try:
                    for modname in ('lib.patterns.flat', 'lib.patterns.panel', 'lib.patterns.new', 'lib.patterns.meta', 'lib.patterns.group'):
                        try:
                            mod = __import__(modname, fromlist=['*'])
                            if hasattr(mod, pat_name):
                                cls = getattr(mod, pat_name)
                                return getattr(cls, 'render_mode', 'flat')
                        except Exception:
                            continue
                except Exception:
                    pass
                return 'unknown'

            for pat in pattern_names:
                mode = _resolve_mode(pat)
                tree.insert('', 'end', values=(pat, mode))
            tree.pack(side=tk.LEFT, padx=10, pady=5)

            def on_tree_select(event):
                sel = tree.selection()
                if not sel:
                    return
                item = sel[0]
                vals = tree.item(item, 'values')
                if vals and pattern_select_callback:
                    pattern_select_callback(vals[0])
            tree.bind('<<TreeviewSelect>>', on_tree_select)

        # right_top reserved for future controls (previously had Quit button)

        # Bottom controls: BPM + geometry + apply/reload
        bottom_ctrl = tk.Frame(cls.root)
        bottom_ctrl.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # BPM controls (bottom-left)
        bpm_frame = tk.Frame(bottom_ctrl)
        bpm_frame.pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(bpm_frame, text='BPM').pack(side=tk.LEFT)
        # allow caller to provide an initial bpm (e.g. from pdc.current_bpm)
        # default to 300 BPM if caller did not provide an initial value
        bpm_var = tk.IntVar(value=(int(bpm_initial) if bpm_initial else 300))
        bpm_display = tk.StringVar(value=str(bpm_var.get()))
        def _on_bpm(v):
            try:
                iv = int(float(v))
            except Exception:
                return
            bpm_display.set(str(iv))
            if bpm_change_callback:
                bpm_change_callback(iv)
        bpm_slider = tk.Scale(bpm_frame, from_=30, to=400, orient=tk.HORIZONTAL, variable=bpm_var, command=_on_bpm, length=240)
        bpm_slider.pack(side=tk.LEFT)
        tk.Label(bpm_frame, textvariable=bpm_display, width=4).pack(side=tk.LEFT, padx=6)

        # Geometry controls (bottom-center) - support explicit lights_per_panel
        cls.num_lights_var = tk.IntVar(value=num_lights)
        cls.total_lights_var = tk.IntVar(value=num_lights)
        cls.num_panels_var = tk.IntVar(value=1)
        cls.lights_per_panel_var = tk.IntVar(value=0)  # 0 means auto-calc
        geom_frame = tk.Frame(bottom_ctrl)
        geom_frame.pack(side=tk.LEFT, padx=10, pady=5)
        # row 1: counts
        row1 = tk.Frame(geom_frame)
        row1.pack(side=tk.TOP)
        tk.Label(row1, text='Total').pack(side=tk.LEFT)
        lbl_total = tk.Label(row1, textvariable=cls.total_lights_var, width=6, anchor='w')
        lbl_total.pack(side=tk.LEFT)
        tk.Label(row1, text='Panels').pack(side=tk.LEFT, padx=(8,0))
        spin_panels = tk.Spinbox(row1, from_=1, to=256, textvariable=cls.num_panels_var, width=5)
        spin_panels.pack(side=tk.LEFT)
        tk.Label(row1, text='L/Panel').pack(side=tk.LEFT, padx=(8,0))
        spin_lpp = tk.Spinbox(row1, from_=0, to=1024, textvariable=cls.lights_per_panel_var, width=5)
        spin_lpp.pack(side=tk.LEFT)
        # apply/reload callback (areas removed from UI)
        def _apply_geom():
            try:
                nl = int(cls.total_lights_var.get())
                npan = int(cls.num_panels_var.get())
                lpp = int(cls.lights_per_panel_var.get())
            except Exception:
                return
            areas = ''
            if geometry_apply_callback:
                geometry_apply_callback(nl, npan, lpp, areas)

        # Apply button on the same line as the counts for compactness
        btn_apply = tk.Button(row1, text='Apply', command=_apply_geom)
        btn_apply.pack(side=tk.LEFT, padx=(8,0))
        # update total when panels or lpp change
        def _update_total(*args):
            try:
                npan = int(cls.num_panels_var.get())
                lpp = int(cls.lights_per_panel_var.get())
            except Exception:
                cls.total_lights_var.set(num_lights)
                return
            if lpp and lpp > 0:
                total = npan * lpp
            else:
                # default fallback: keep previous total or initial num_lights
                total = num_lights
            cls.total_lights_var.set(total)
        try:
            cls.num_panels_var.trace('w', _update_total)
            cls.lights_per_panel_var.trace('w', _update_total)
        except Exception:
            pass
        # (area names control removed)
        # Apply handled inline on row1

        # Status bar (bottom-right)
        status_frame = tk.Frame(bottom_ctrl)
        status_frame.pack(side=tk.RIGHT, padx=10)
        cls.status_pattern_var = tk.StringVar(value='pattern: -')
        cls.status_track_var = tk.StringVar(value='track: -')
        cls.status_bpm_var = tk.StringVar(value='bpm: -')
        tk.Label(status_frame, textvariable=cls.status_pattern_var).pack(side=tk.TOP, anchor='e')
        tk.Label(status_frame, textvariable=cls.status_track_var).pack(side=tk.TOP, anchor='e')
        tk.Label(status_frame, textvariable=cls.status_bpm_var).pack(side=tk.TOP, anchor='e')

        def set_status(pattern=None, track=None, bpm=None):
            try:
                if pattern is not None:
                    cls.status_pattern_var.set(f'pattern: {pattern}')
                if track is not None:
                    cls.status_track_var.set(f'track: {track}')
                if bpm is not None:
                    cls.status_bpm_var.set(f'bpm: {bpm}')
            except Exception:
                pass
        cls.set_status = set_status

        # Canvas für LEDs
        cls.canvas = tk.Canvas(cls.root, width=size, height=size, bg='black')
        cls.canvas.pack()
        # store base size for interactive scaling
        cls.base_canvas_size = int(size)
        # store panel band width for later recalculations
        cls.panel_band_width = int(panel_band_width)
        # compute geometry (circle_radius and light radius) and positions
        cls.update_geometry(num_lights)
        # draw initial panel bands (behind lights)
        try:
            cls.draw_panels(getattr(cls, 'num_panels', 1), band_width=cls.panel_band_width)
        except Exception:
            pass

        # Canvas size discrete choices (user requested 60,80,100,120 percent)
        try:
            scale_choices = [('60%', 0.6), ('80%', 0.8), ('100%', 1.0), ('120%', 1.2)]
            # default canvas scale choice: 80%
            canvas_scale_var = tk.StringVar(value='80%')
            def _on_canvas_scale_choice(val):
                try:
                    if isinstance(val, str) and val.endswith('%'):
                        pct = int(val.rstrip('%'))
                        scale = pct / 100.0
                    else:
                        scale = float(val)
                except Exception:
                    return
                new_size = max(200, int(cls.base_canvas_size * scale))
                try:
                    cls.resize_canvas(new_size)
                except Exception:
                    pass

            scale_frame = tk.Frame(bpm_frame)
            scale_frame.pack(side=tk.LEFT, padx=(8,0))
            tk.Label(scale_frame, text='Canvas').pack(side=tk.LEFT)
            # OptionMenu with fixed user-requested stages
            options = [label for (label, _) in scale_choices]
            om = tk.OptionMenu(scale_frame, canvas_scale_var, *options, command=_on_canvas_scale_choice)
            om.config(width=6)
            om.pack(side=tk.LEFT)
        except Exception:
            pass

    @classmethod
    def draw_panels(cls, num_panels, band_width=40, gap_deg=4, color='#444', pad=6, border_color='#222'):
        """Draw panel arcs (rounded bands) behind the lights.
        num_panels: number of panels to draw around the circle
        band_width: thickness of the arc band
        gap_deg: degrees gap between panels
        """
        # remove old panel items
        try:
            if hasattr(cls, 'panel_items') and cls.panel_items:
                for it in cls.panel_items:
                    try:
                        cls.canvas.delete(it)
                    except Exception:
                        pass
        except Exception:
            pass
        cls.panel_items = []
        if cls.canvas is None:
            return
        # compute angular span per panel
        span = 2 * math.pi / max(1, int(num_panels))
        start_offset = -math.pi/2  # start at top
        # panel centered on lights circle: expand both inward and outward by pad
        r_light = getattr(cls, 'circle_radius', cls.center_x - 60)
        half = band_width / 2.0
        r_inner = max(6, r_light - half - pad)
        r_outer = r_light + half + pad
        for pid in range(int(num_panels)):
            start_ang = start_offset + pid * span + math.radians(gap_deg)/2.0
            end_ang = start_ang + span - math.radians(gap_deg)
            pts = []
            steps = max(2, int(((end_ang - start_ang) * r_outer) / 6))
            for i in range(steps+1):
                a = start_ang + (end_ang - start_ang) * (i / steps)
                x = cls.center_x + r_outer * math.cos(a)
                y = cls.center_y + r_outer * math.sin(a)
                pts.append((x, y))
            for i in range(steps, -1, -1):
                a = start_ang + (end_ang - start_ang) * (i / steps)
                x = cls.center_x + r_inner * math.cos(a)
                y = cls.center_y + r_inner * math.sin(a)
                pts.append((x, y))
            flat = [coord for p in pts for coord in p]
            try:
                it = cls.canvas.create_polygon(flat, fill=color, outline=border_color)
                cls.panel_items.append(it)
            except Exception:
                pass
        # thin border lines at sector boundaries
        try:
            for pid in range(int(num_panels)):
                ang = start_offset + pid * span
                ix = cls.center_x + r_inner * math.cos(ang)
                iy = cls.center_y + r_inner * math.sin(ang)
                ox = cls.center_x + r_outer * math.cos(ang)
                oy = cls.center_y + r_outer * math.sin(ang)
                try:
                    line = cls.canvas.create_line(ix, iy, ox, oy, fill=border_color, width=2)
                    cls.panel_items.append(line)
                except Exception:
                    pass
        except Exception:
            pass
        # control area finished
        # KEIN mainloop-Thread mehr hier!
        cls.root.update()

    @classmethod
    def update_geometry(cls, num_lights, num_panels=None, gap_deg=4):
        """Compute circle_radius and light radius to avoid overlaps for given number of lights.
        Sets cls.circle_radius and cls.radius and recomputes cls.positions.
        """
        # panel band: outer radius close to edge
        band_width = getattr(cls, 'panel_band_width', 40)
        band_outer = cls.center_x - 10
        band_inner = max(10, band_outer - int(band_width))
        # lights circle radius placed inside the band
        lights_circle_radius = max(10, band_inner - 10 - cls.radius)
        # prevent overlapping lights: compute max light radius from angular spacing
        try:
            angle = 2 * math.pi / max(1, int(num_lights))
            # approximate max radius so adjacent centers are at least 2*radius apart
            max_r_by_angle = max(2, int((lights_circle_radius * angle) / 2 * 0.9))
            # adjust light radius if necessary
            cls.radius = min(cls.radius, max_r_by_angle)
        except Exception:
            pass
        # set class circle_radius to the computed lights radius circle
        cls.circle_radius = int(lights_circle_radius)
        # recompute positions
        cls.positions = {}
        nlights = int(max(1, num_lights))
        if num_panels and nlights % int(num_panels) == 0:
            # distribute lights grouped per panel so they sit inside panel sectors
            npan = int(num_panels)
            per_panel = nlights // npan
            span = 2 * math.pi / npan
            start_offset = -math.pi / 2
            gap_rad = math.radians(gap_deg)
            for pid in range(npan):
                sector_start = start_offset + pid * span + gap_rad / 2.0
                sector_end = start_offset + (pid + 1) * span - gap_rad / 2.0
                for i in range(per_panel):
                    frac = (i + 0.5) / per_panel  # center lights within sector
                    a = sector_start + (sector_end - sector_start) * frac
                    lid = pid * per_panel + i + 1
                    x = cls.center_x + cls.circle_radius * math.cos(a)
                    y = cls.center_y + cls.circle_radius * math.sin(a)
                    cls.positions[lid] = (x, y)
        else:
            for lid in range(1, nlights+1):
                angle = 2 * math.pi * (lid-1) / nlights
                x = cls.center_x + cls.circle_radius * math.cos(angle)
                y = cls.center_y + cls.circle_radius * math.sin(angle)
                cls.positions[lid] = (x, y)

    def __init__(self, lid):
        super().__init__(lid)
        self.lid = lid
        if GraphicLight.canvas is not None and lid in GraphicLight.positions:
            x, y = GraphicLight.positions[lid]
            self.circle = GraphicLight.canvas.create_oval(
                x - GraphicLight.radius, y - GraphicLight.radius,
                x + GraphicLight.radius, y + GraphicLight.radius,
                fill='grey', outline='white', width=2
            )
            GraphicLight.circles[lid] = self.circle
        else:
            self.circle = None
        logger.debug(f"GraphicLight.__init__ lid={lid}")

    @classmethod
    def rebuild_positions(cls, num_lights, num_panels=None):
        """Recompute positions for a new number of lights and clear existing canvas items.
        After calling this, board.init_leds() should be invoked to recreate GraphicLight instances.
        """
        # clear existing canvas items and recompute geometry/positions
        cls.circles = {}
        if cls.canvas is not None:
            try:
                cls.canvas.delete('all')
            except Exception:
                pass
        # recompute geometry for new number of lights (and optionally panels)
        try:
            cls.update_geometry(num_lights, num_panels=num_panels)
        except Exception:
            # fall back to simple positions
            cls.positions = {}
            for lid in range(1, num_lights+1):
                angle = 2 * math.pi * (lid-1) / num_lights
                x = cls.center_x + cls.circle_radius * math.cos(angle)
                y = cls.center_y + cls.circle_radius * math.sin(angle)
                cls.positions[lid] = (x, y)

    @classmethod
    def resize_canvas(cls, new_size):
        """Resize the canvas while keeping existing LED items: reposition circles and redraw panels."""
        if cls.canvas is None:
            return
        try:
            cls.canvas.config(width=new_size, height=new_size)
        except Exception:
            pass
        # update center and sensible defaults
        cls.center_x = new_size // 2
        cls.center_y = new_size // 2
        cls.radius = max(3, int(new_size * 0.02))
        # recompute geometry
        try:
            num_lights = getattr(cls, 'num_lights_var', None)
            if num_lights is not None:
                nl = int(num_lights.get())
            else:
                nl = max(1, len(cls.positions) or getattr(cls, 'total_lights_var', 1))
            npan = getattr(cls, 'num_panels', None)
            cls.update_geometry(nl, num_panels=npan)
        except Exception:
            pass
        # redraw panel bands
        try:
            cls.draw_panels(getattr(cls, 'num_panels', 1), band_width=getattr(cls, 'panel_band_width', 40))
        except Exception:
            pass
        # reposition existing circles
        try:
            for lid, cid in list(getattr(cls, 'circles', {}).items()):
                if lid in cls.positions:
                    x, y = cls.positions[lid]
                    r = cls.radius
                    try:
                        cls.canvas.coords(cid, x - r, y - r, x + r, y + r)
                        cls.canvas.tag_raise(cid)
                    except Exception:
                        pass
        except Exception:
            pass
        try:
            cls.root.update()
        except Exception:
            pass

    def on(self):
        self.state = 1
        try:
            # verify the canvas/root still exist in the Tcl interpreter
            if self.circle and GraphicLight.canvas and GraphicLight.canvas.winfo_exists():
                GraphicLight.canvas.itemconfig(self.circle, fill='yellow')
                if GraphicLight.root and GraphicLight.root.winfo_exists():
                    GraphicLight.root.update()
        except tk.TclError as e:
            # widget was destroyed or Tcl interpreter gone: degrade gracefully
            logger.error(f"GraphicLight.on TclError: {e}")
            # stop trying to access the canvas in future
            self.circle = None
            GraphicLight.canvas = None
            GraphicLight.root = None
        except Exception as e:
            logger.error(f"GraphicLight.on unexpected error: {e}")
        #logger.debug(f"GraphicLight {self.lid} ON")
        #print(f"[GraphicLight] LED {self.lid} ON (state={self.state})")

    def off(self):
        self.state = 0
        try:
            if self.circle and GraphicLight.canvas and GraphicLight.canvas.winfo_exists():
                GraphicLight.canvas.itemconfig(self.circle, fill='grey')
                if GraphicLight.root and GraphicLight.root.winfo_exists():
                    GraphicLight.root.update()
        except tk.TclError as e:
            logger.error(f"GraphicLight.off TclError: {e}")
            self.circle = None
            GraphicLight.canvas = None
            GraphicLight.root = None
        except Exception as e:
            logger.error(f"GraphicLight.off unexpected error: {e}")
        #logger.debug(f"GraphicLight {self.lid} OFF")
        #print(f"[GraphicLight] LED {self.lid} OFF (state={self.state})")

    def __repr__(self):
        return f"GraphicLight {self.lid} (state={self.state})"
