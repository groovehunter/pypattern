import tkinter as tk
import math
import threading
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
    def setup_canvas(cls, num_lights, pattern_names=None, pattern_select_callback=None, start_callback=None, stop_callback=None):
        size = cls.center_x * 2
        cls.root = tk.Tk()
        cls.root.title("LED Simulation")
        # Control-Frame
        ctrl_frame = tk.Frame(cls.root)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)
        # Start/Stop Buttons
        btn_start = tk.Button(ctrl_frame, text="Start", command=start_callback)
        btn_start.pack(side=tk.LEFT, padx=5, pady=5)
        btn_stop = tk.Button(ctrl_frame, text="Stop", command=stop_callback)
        btn_stop.pack(side=tk.LEFT, padx=5, pady=5)
        # Pattern-Liste
        if pattern_names:
            listbox = tk.Listbox(ctrl_frame, height=len(pattern_names), exportselection=False)
            for pat in pattern_names:
                listbox.insert(tk.END, pat)
            listbox.pack(side=tk.LEFT, padx=10, pady=5)
            def on_select(evt):
                w = evt.widget
                idx = w.curselection()
                if idx:
                    pat = w.get(idx[0])
                    if pattern_select_callback:
                        pattern_select_callback(pat)
            listbox.bind('<<ListboxSelect>>', on_select)
        # Canvas für LEDs
        cls.canvas = tk.Canvas(cls.root, width=size, height=size, bg='black')
        cls.canvas.pack()
        # Positionen für alle LEDs berechnen (gleichmäßig auf Kreis)
        for lid in range(1, num_lights+1):
            angle = 2 * math.pi * (lid-1) / num_lights
            x = cls.center_x + cls.circle_radius * math.cos(angle)
            y = cls.center_y + cls.circle_radius * math.sin(angle)
            cls.positions[lid] = (x, y)
        # KEIN mainloop-Thread mehr hier!
        cls.root.update()

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

    def on(self):
        self.state = 1
        if self.circle and GraphicLight.canvas:
            GraphicLight.canvas.itemconfig(self.circle, fill='yellow')
            GraphicLight.root.update()
        logger.debug(f"GraphicLight {self.lid} ON")
        print(f"[GraphicLight] LED {self.lid} ON (state={self.state})")

    def off(self):
        self.state = 0
        if self.circle and GraphicLight.canvas:
            GraphicLight.canvas.itemconfig(self.circle, fill='grey')
            GraphicLight.root.update()
        logger.debug(f"GraphicLight {self.lid} OFF")
        print(f"[GraphicLight] LED {self.lid} OFF (state={self.state})")

    def __repr__(self):
        return f"GraphicLight {self.lid} (state={self.state})"
