### entry point - only for ESP32 platforms
import esp
esp.osdebug(None)
from lib.Track import Track
import gc
gc.collect()
import sys, os

syspath = ['esp32', 'www', 'esp32_http', 'lib', 'conf']
if sys.platform == 'esp32':
  for p in syspath:
      slashed_p = '/'+p
      abs_path = os.getcwd() + p
      if abs_path not in sys.path:
          sys.path.append(abs_path)

#print(sys.path)

from web import http_server
import uasyncio #as asyncio
from pdc import PdcSingleton as PDC

pdc = PDC()
pdc.init()
pdc.board.boardname = 'hexagon'
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
        pdc.change_board()
        await uasyncio.sleep_ms(pdc.velocity*500)


loop = uasyncio.get_event_loop()
factory = uasyncio.start_server(http_server, '0.0.0.0', 80)
server = loop.run_until_complete(factory)

loop.create_task(run_pdc())
loop.run_forever()
