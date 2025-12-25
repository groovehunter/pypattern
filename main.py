### entry point - only for ESP32 platforms
import sys, os
from settings import boardname
import network
#print(__file__)


mp = False
if sys.platform == 'esp32':  # or sys.implementation[0]=='micropython':
    mp = True

cwd = ''
if sys.platform == 'esp32':
    import esp
    esp.osdebug(None)
    cwd = os.getcwd()
    import uasyncio as asyncio
else:
    print("WARNING: NO esp32 environment !")
    from env import HOME
    cwd = HOME
    sys.exit()

from lib.Track import Track
import gc
gc.collect()

def check_memory():
    free = gc.mem_free()
    alloc = gc.mem_alloc()

    print('avail: ', free)
    print('alloc: ', alloc)
    print('total: ', alloc+free)
          
# Funktion zur Berechnung des Speicherverbrauchs
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

# Speicherverbrauch abfragen
check_memory()
check_filesystem_usage()

syspath = ['esp32', 'www', 'esp32_http', 'lib', 'conf', 'microdot']
if mp:
    for p in syspath:
        slashed_p = '/' + p
        abs_path = cwd + slashed_p
        if abs_path not in sys.path:
            sys.path.append(abs_path)

print(sys.path)

from web import http_server
from pdc import PdcSingleton as PDC

pdc = PDC()
pdc.init()
pdc.board.boardname = boardname
#pdc.boardname = boardname
pdc.board.load_py_conf()
pdc.board.init()
pdc.board.track = Track()

async def run_pdc():
    print("STARTING run_pdc")
    while True:
        #self.timer += 1
        pat_name = pdc.board.track.next_pattern()
        pdc.board.set_pattern(pat_name)
        pdc.board.pattern.subclass_init()
        repeats = pdc.board.track.get_current_repeats()
        num_steps = pdc.board.pattern.states_count * repeats
        print("num_steps: ", num_steps)
        for i in range(num_steps):
            pdc.board.pattern.next_state()
            pdc.board.change_board()
            await asyncio.sleep_ms(pdc.sleep_ms)


loop = asyncio.get_event_loop()
#wifi_if = network.WLAN(network.STA_IF)
wifi_if = network.WLAN(network.AP_IF)
wifi_if.active(True)
wifi_if.config(essid='uvchakras', password='turnaround123')

#if wifi_if.isconnected():
if True:
    factory = asyncio.start_server(http_server, '0.0.0.0', 8080)
    server = loop.run_until_complete(factory)

loop.create_task(run_pdc())
loop.run_forever()
