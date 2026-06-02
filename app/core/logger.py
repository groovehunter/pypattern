class Logger:
    def __init__(self, level="DEBUG"):
        self.level = level

    def log(self, lvl, msg):
        # Für Phase 1 halten wir das Logging RAM-schonend nur auf der Konsole (REPL)
        print(f"[{lvl}] {msg}")

    def info(self, msg): self.log("INFO", msg)
    def debug(self, msg): self.log("DEBUG", msg)
    def error(self, msg): self.log("ERROR", msg)
    def warn(self, msg): self.log("WARN", msg)

log = Logger()

