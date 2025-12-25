import tkinter as tk

from flowpy.utils import setup_logger
from lib.BoardBase import BoardBase

logger = setup_logger(__name__, __name__ + '.log')


class GameBoard(BoardBase, tk.Frame):
    def __init__(self, parent, rows=6, columns=6, size=60, color1="white", color2="grey"):
        BoardBase.__init__(self)
        tk.Frame.__init__(self, parent)
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
            width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)

        self.canvas.bind("<Configure>", self.refresh2)
        self.canvas.bind("<Button-1>", self.set_square_color)

        # Board-Konfiguration laden
        self.boardname = getattr(self, 'boardname', 'square')
        self.boardcfg = None
        self.cfg = None
        self.load_py_conf()

    def init_keys(self):
        self.canvas.bind("<Button-3>", self.ctrl.next_state )

    def refresh2(self, event):
        self.set_sizes(event)
        self.create_grid()
#        self.init_panels()
#        self.init_panel_lights()
#        self.enlighten()
        self.mark_panels()

    def set_sizes(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)

    def init(self):
        self.create_grid()
        self.init_panels()
        self.init_panel_lights()
#        self.enlighten()
#        self.mark_panels()

    def create_grid(self):
        col_outline = "grey"
        color = self.color1
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2,
                    outline=col_outline, fill=color, tags="square")


    def init_panel_lights(self):
        for i, panel in self.panels.items():
            panel.init_lights()

    def refresh_board(self):
        """Leert das Canvas und zeichnet das Board gemäß aktuellem Zustand neu."""
        #self.canvas.delete("all")
        #self.create_grid()
        for i, panel in self.panels.items():
            for j, light in panel.lights.items():
                self.set_square_color_atpos(light.position, light.state)

    def enlighten(self):
        logger.debug("BoardCanvas - enlighten")
        """
        for i, panel in self.panels.items():
            logger.debug("enlighten panel %s", i)
            for j, light in panel.lights.items():
                self.set_square_color_atpos(light.position, light.state)
        """
        self.refresh_board()

    def set_square_color(self, event):
        color = "yellow"
        col_outline = "grey"
        x1 = int(event.x/self.size) * self.size
        y1 = int(event.y/self.size) * self.size
        x2 = x1 + self.size
        y2 = y1 + self.size
        self.canvas.create_rectangle(x1, y1, x2, y2,
            outline=col_outline, fill=color, tags="square")

    def set_square_color_atpos(self, pos, state):
        #logger.debug("BoardCanvas - set_square_color  %s at pos %s", state, pos)
        color = "grey"
        if state == 1:
            color = "yellow"
        if state == 0:
            color = "white"
        col_outline = "grey"
        (y, x) = pos    # y= row-nr // x=col-nr
        x1 = x * self.size
        y1 = y * self.size
        x2 = x1 + self.size
        y2 = y1 + self.size
        self.canvas.create_rectangle(x1, y1, x2, y2,
            outline=col_outline, fill=color, tags="square")

    ### unused
    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)
