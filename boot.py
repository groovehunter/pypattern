import gc
try:
    import machine
    # MicroPython ESP32 Setup
    machine.freq(240000000) # Full speed
except ImportError:
    pass # Desktop Mock

# Clean boot up
gc.collect()

