from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import time

from flowpy.utils import setup_logger
logger = setup_logger(__name__, __name__ + '.log')


class ConsoleBoard:
    def __init__(self, board):
        self.board = board
        self.console = Console()
        self.rows = getattr(board, 'rows', 6)
        self.columns = getattr(board, 'columns', 6)

    def render_board(self):
        table = Table(show_header=False, box=None, pad_edge=False)
        for col in range(self.columns):
            table.add_column(justify="center")
        for row in range(self.rows):
            cells = []
            for col in range(self.columns):
                state = self.get_light_state(row, col)
                cell = "[yellow]●[/yellow]" if state else "[white]○[/white]"
                cells.append(cell)
            table.add_row(*cells)
        return Panel(table, title="Pattern Board", border_style="blue")

    def get_light_state(self, row, col):
        # Annahme: board.panels ist ein dict mit Panel-Objekten, Panel.lights ist dict mit Light-Objekten
        for panel in self.board.panels.values():
            for light in panel.lights.values():
                if hasattr(light, 'position') and light.position == (row, col):
                    return light.state
        return 0

    def run(self):
        with Live(self.render_board(), refresh_per_second=4, console=self.console) as live:
            while True:
                # Hier kann z.B. ein Pattern-Wechsel oder next_state ausgelöst werden
                time.sleep(1)
                # Beispiel: board.pattern.next_state() und Board neu rendern
                if hasattr(self.board, 'pattern') and hasattr(self.board.pattern, 'next_state'):
                    self.board.pattern.next_state()
                live.update(self.render_board())

# Beispiel für die Verwendung:
# from tk.BoardCanvas import GameBoard
# board = GameBoard(None)
# console_board = ConsoleBoard(board)
# console_board.run()

