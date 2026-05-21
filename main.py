### entry point - for ESP32 platforms and others


import sys, os
# sys.path für ESP32/MicroPython-Umgebung robust setzen
ROOT = os.path.abspath(os.path.dirname(__file__)) if hasattr(os, 'path') else '/'
for sub in ('', 'esp32', 'lib', 'conf', 'www', 'esp32_http'):
    try:
        p = os.path.join(ROOT, sub)
    except Exception:
        p = '/' + sub if not sub.startswith('/') else sub
    if p not in sys.path:
        sys.path.insert(0, p)

#print(__file__)
#print(sys.path)
import time

MICROPYTHON = False
if sys.platform == 'esp32':  # oder sys.implementation[0]=='micropython'
    MICROPYTHON = True

if MICROPYTHON:
    from flowpy.simplelogger import SimpleLogger
    logger = SimpleLogger(path='main.log', level='DEBUG')
else:
    from flowpy.utils import setup_logger
    logger = setup_logger('main', 'main.log')


for i in range(3):
    print(i)
    logger.debug(f"main.py start-loop {i}")
    time.sleep(0.01)

MICROPYTHON = False
if sys.platform == 'esp32':  # or sys.implementation[0]=='micropython':
    MICROPYTHON = True

cwd = ''
if sys.platform == 'esp32':
    import esp
    import network
    esp.osdebug(None)
    cwd = os.getcwd()
    import uasyncio as asyncio
else:
    print("WARNING: NO esp32 environment !")
    from env import HOME
    cwd = HOME
    #sys.exit()
    import asyncio

import gc
gc.collect()


def check_memory():
    free = gc.mem_free()
    alloc = gc.mem_alloc()

    print('avail: ', free)
    print('alloc: ', alloc)
    print('total: ', alloc+free)
          
def check_filesystem_usage():
    # Gesamtgröße des Dateisystems
    total = os.statvfs('/')
    total_size = total[0] * total[2]  # Gesamter Flash-Speicher in Bytes

    # Verfügbarer Speicher
    free_size = total[0] * total[3]  # Verfügbarer Speicher in Bytes
    used_size = total_size - free_size  # Genutzter Speicher

    print("Gesamter Speicher:", total_size // 1024, "KB")
    print("Verfügbarer Speicher:", free_size // 1024, "KB")
    print("Genutzter Speicher:", used_size // 1024, "KB")


def test_lights():
    import time
    from Esp32Light import Esp32Light
    from settings import boardname
    from esp32_conf import pinmap
    num_lights = len(pinmap[boardname])
    leds = [Esp32Light(i+1) for i in range(num_lights)]
    print(f"Starte LED-Test: {num_lights} LEDs auf Board '{boardname}'")
    for i, led in enumerate(leds):
        print(f"LED {i+1} AN")
        led.pin.value(1)
        time.sleep(0.3)
        print(f"LED {i+1} AUS")
        led.pin.value(0)
        time.sleep(0.1)
    print("LED-Test abgeschlossen.")

# Speicherverbrauch abfragen
if MICROPYTHON:
    check_memory()
    check_filesystem_usage()

syspath = ['esp32', 'www', 'esp32_http', 'lib', 'conf']
#if MICROPYTHON:
print(sys.path)
"""
for p in syspath:
    slashed_p = p
    abs_path = slashed_p
    # abs_path = cwd + slashed_p
    if abs_path not in sys.path:
        sys.path.append(abs_path)
"""
# Entferne evtl. vorhandene relative Einträge
for p in syspath:
    if p in sys.path:
        sys.path.remove(p)
if MICROPYTHON:
    # MicroPython: Pfade mit führendem Slash
    for p in syspath:
        abs_path = '/' + p if not p.startswith('/') else p
        if abs_path not in sys.path:
            sys.path.append(abs_path)
else:
    # CPython: absolute Pfade
    for p in syspath:
        abs_path = os.path.abspath(os.path.join(cwd, p))
        if abs_path not in sys.path:
            sys.path.append(abs_path)

if MICROPYTHON:
    test_lights()

print(sys.path)
from web import http_server
from pdc import PdcSingleton as PDC
from settings import boardname
from Track import Track

# Immer Esp32Board verwenden!
pdc = PDC()
pdc.init(board_type='esp32')
pdc.board.boardname = boardname
pdc.board.load_py_conf()
pdc.board.init()
pdc.board.track = Track()


def get_time_ms():
    try:
        return time.ticks_ms()
    except:
        return int(time.time() * 1000)


async def run_pdc():
    print("STARTING run_pdc")
    while True:
        if pdc.is_manual_pattern():
            # Nur das gewählte Pattern in Endlosschleife spielen
            print("manual")
            pat_name = pdc.current_pattern
            if pat_name:
                # This block seems to be for a special manual mode.
                # It re-initializes the pattern every time.
                # Let's ensure it uses the correct new method.
                pdc.board.set_pattern(pat_name)
                # The call to subclass_init is now handled inside set_pattern.
                # pdc.board.pattern.subclass_init() # REMOVED

                if hasattr(pdc.board.pattern, 'states_count'):
                    num_steps = pdc.board.pattern.states_count
                else:
                    num_steps = 1 # Default for patterns without a fixed state count

                for i in range(num_steps):
                    start = get_time_ms()
                    pdc.board.pattern.next_state()
                    pdc.board.change_board()
                    elapsed = get_time_ms() - start
                    rest = pdc.sleep_ms - elapsed
                    if rest > 0:
                        await asyncio.sleep(rest / 1000)
            else:
                await asyncio.sleep(0.1)
        else:
            t_init_start = get_time_ms()
            pat_name = pdc.board.track.next_pattern()
            pdc.board.set_pattern(pat_name)
            pdc.set_current_pattern(pat_name)
            # The call to subclass_init is now handled inside set_pattern.
            # pdc.board.pattern.subclass_init() # REMOVED
            repeats = pdc.board.track.get_current_repeats()
            print("repeats", repeats)
            if hasattr(pdc.board.pattern, 'states_count'):
                num_steps = pdc.board.pattern.states_count * repeats
            else:
                # For patterns without a fixed state count, maybe repeat N times?
                num_steps = 30 * repeats # Arbitrary number of steps

            fac = 0.8 # Define the missing factor
            for i in range(num_steps):
                #logger.debug(i)
                start = get_time_ms()
                pdc.board.pattern.next_state()
                pdc.board.change_board()
                elapsed = get_time_ms() - start
                rest = pdc.sleep_ms - elapsed
                if rest > 0:
                    sl = (rest * fac) / 1000
                    await asyncio.sleep(sl)


loop = asyncio.get_event_loop()


PORT = 8080 if MICROPYTHON else 8080

print('in main before connect')
if MICROPYTHON:
    from boot import connect
    # for DEV skip Wifi
    connect()
    print('after connect method')

    wifi_if = network.WLAN(network.STA_IF)
    if wifi_if.isconnected():
        print("WIFI CONNECTED [OK]")
        factory = asyncio.start_server(http_server, '0.0.0.0', PORT)
        server = loop.run_until_complete(factory)
else:
    factory = asyncio.start_server(http_server, '0.0.0.0', PORT)
    server = loop.run_until_complete(factory)


loop.create_task(run_pdc())

loop.run_forever()
