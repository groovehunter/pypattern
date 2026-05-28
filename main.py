### entry point - for ESP32 platforms and others

import sys
if sys.platform != 'esp32':
    print("Dieses Skript ist nur für ESP32/MicroPython vorgesehen. Bitte desktop_main.py für Desktop verwenden.")
    sys.exit(0)

import os
import esp
import network
esp.osdebug(None)
cwd = os.getcwd()
import uasyncio as asyncio
import time
import gc
from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__ + '.log', level='DEBUG')
gc.collect()

def check_memory():
    free = gc.mem_free()
    alloc = gc.mem_alloc()
    print('avail: ', free)
    print('alloc: ', alloc)
    print('total: ', alloc+free)

def check_filesystem_usage():
    total = os.statvfs('/')
    total_size = total[0] * total[2]
    free_size = total[0] * total[3]
    used_size = total_size - free_size
    print("Gesamter Speicher:", total_size // 1024, "KB")
    print("Verfügbarer Speicher:", free_size // 1024, "KB")
    print("Genutzter Speicher:", used_size // 1024, "KB")


syspath = ['esp32', 'www', 'esp32_http', 'lib', 'conf']
# Entferne evtl. vorhandene relative Einträge
for p in syspath:
    if p in sys.path:
        sys.path.remove(p)
# MicroPython: Pfade mit führendem Slash
for p in syspath:
    abs_path = '/' + p if not p.startswith('/') else p
    if abs_path not in sys.path:
        sys.path.append(abs_path)

#print(sys.path)
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
        try:
            if pdc.is_manual_pattern():
                pat_name = pdc.current_pattern
                if pat_name:
                    pdc.board.set_pattern(pat_name)
                    if hasattr(pdc.board.pattern, 'states_count'):
                        num_steps = pdc.board.pattern.states_count
                    else:
                        num_steps = 1
                    for _ in range(num_steps):
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
                repeats = pdc.board.track.get_current_repeats()
                if hasattr(pdc.board.pattern, 'states_count'):
                    num_steps = pdc.board.pattern.states_count * repeats
                else:
                    num_steps = 30 * repeats
                fac = 0.8
                for _ in range(num_steps):
                    start = get_time_ms()
                    pdc.board.pattern.next_state()
                    pdc.board.change_board()
                    elapsed = get_time_ms() - start
                    rest = pdc.sleep_ms - elapsed
                    if rest > 0:
                        sl = (rest * fac) / 1000
                        await asyncio.sleep(sl)
            await asyncio.sleep(0.05)
        except Exception as e:
            logger.error("Exception in run_pdc: %s", e)
            await asyncio.sleep(1)

loop = asyncio.get_event_loop()


PORT = 8080

print('in main before connect')
from boot import connect
# for DEV skip Wifi
connect()
print('after connect method')

wifi_if = network.WLAN(network.STA_IF)
if wifi_if.isconnected():
    print("WIFI CONNECTED [OK]")
    factory = asyncio.start_server(http_server, '192.168.43.10', PORT)
    print(f"[DEBUG] Starte Webserver auf 192.168.43.10:{PORT}")
    server = loop.run_until_complete(factory)
    print(f"[DEBUG] Webserver läuft auf 192.168.43.10:{PORT}")
    print("after start_server")


loop.create_task(run_pdc())

loop.run_forever()
