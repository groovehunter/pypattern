### entry point - only for ESP32 platforms

import esp
esp.osdebug(None)

import gc
gc.collect()
#from time import sleep
import sys, os

syspath = ['esp32', 'www', 'http', 'lib', 'conf']
if sys.platform == 'esp32':
  for p in syspath:
      slashed_p = '/'+p
      abs_path = os.getcwd() + p
      #print(abs_path)
      if abs_path not in sys.path:
          sys.path.append(abs_path)

print(sys.path)

#from Esp32Board import Esp32Board
from web import http_server
#from web.website import web_page
import uasyncio #as asyncio
from pdc import PdcSingleton as PDC

pdc = PDC()
pdc.init()
pdc.board.boardname = 'square'
pdc.board.load_py_conf()
pdc.board.init()
#pat = 'PairedLightsCycling'
pat = 'DarkPanelRotationPanelPattern'
success = pdc.board.set_pattern(pat)


async def run_pdc():
    print("STARTING run_pdc")
    #pdc.board.test_pattern()
    while True:
        pdc.board.pattern.next_state()
        pdc.board.enlighten()
        await uasyncio.sleep_ms(pdc.velocity*100)
        #if pdc.board.pattern.
        if pdc.board.pattern.uptime > 5:
            print('=== NEW PATTERN ====================')
            pdc.board.set_random_pat()
            pdc.board.pattern.reset_uptime()

loop = uasyncio.get_event_loop()
factory = uasyncio.start_server(http_server, '0.0.0.0', 80)
server = loop.run_until_complete(factory)

loop.create_task(run_pdc())
loop.run_forever()
