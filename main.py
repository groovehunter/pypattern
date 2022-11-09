### entry point - only for ESP32 platforms
import sys, os
from settings import boardname
#print(__file__)

mp = False
if sys.platform=='esp32': #or sys.implementation[0]=='micropython':
  mp = True

cwd = ''
if sys.platform=='esp32':
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

syspath = ['esp32', 'www', 'esp32_http', 'lib', 'conf']
if mp:
  for p in syspath:
    slashed_p = '/'+p
    abs_path = cwd + slashed_p 
    if abs_path not in sys.path:
      sys.path.append(abs_path)

print(sys.path)

from web import http_server
from pdc import PdcSingleton as PDC

pdc = PDC()
pdc.init()
pdc.board.boardname = boardname
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
factory = asyncio.start_server(http_server, '0.0.0.0', 80)
server = loop.run_until_complete(factory)

loop.create_task(run_pdc())
loop.run_forever()
