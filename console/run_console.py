from tk.BoardCanvas import GameBoard
from console.ConsoleBoard import ConsoleBoard

if __name__ == "__main__":
    # Erzeuge das Board-Objekt (ohne GUI-Parent)
    board = GameBoard(None)
    # Optional: Pattern setzen, initialisieren etc.
    # board.set_pattern("AllOnOffPattern")  # Beispiel
    # board.pattern.initial_state()         # falls benötigt

    # Starte die Console-GUI
    console_board = ConsoleBoard(board)
    console_board.run()

