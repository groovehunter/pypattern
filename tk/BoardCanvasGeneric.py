import tkinter as tk

class GameBoardGeneric(tk.Frame):
    """ a more generic board than the first GameBoard """
    
    def __init__(self, parent, rows=15, columns=15, size=30, color1="white", color2="grey"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
            width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)

        self.canvas.bind("<Configure>", self.refresh2)
        self.canvas.bind("<Button-1>", self.set_square_color)

    def init_keys(self):
        self.canvas.bind("<Button-3>", self.ctrl.next_state )

    def refresh2(self, event):
        self.set_sizes(event)
        self.create_grid()
#        self.mark_panels()

    def set_sizes(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)

    def init(self):
        self.create_grid()
        self.init_panels()
#        self.init_panel_lights()

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

    def enlighten_flatarray(self):
      for i, led in self.led.items():
#        print("enlighten %s", i)
        self.led[i].state = self.pattern.lights[i].state
        self.set_square_color_atpos(self.led[i].position, self.led[i].state)

    def enlighten(self):
      #print("BCG 2 - enlighten in BoardCanvasGeneric")
      for i, panel in self.panels.items():
        for i, light in panel.lights.items():
          #self.led.state = light.state
          self.set_square_color_atpos(light.position, light.state)

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
